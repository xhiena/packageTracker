from app.tracking.interface import CarrierTracker
from app.tracking.carriers.correos import CorreosTracker
from app.tracking.carriers.gls import GLSTracker
from app.tracking.carriers.seur import SEURTracker
from fastapi import HTTPException, status

class TrackingService:
    def __init__(self):
        self.carriers = {
            "CORREOS": CorreosTracker(),
            "GLS": GLSTracker(),
            "SEUR": SEURTracker(),
        }
    
    def get_tracker(self, carrier_code: str) -> CarrierTracker:
        """Get the appropriate tracker for the given carrier code"""
        carrier_code = carrier_code.upper()
        if carrier_code not in self.carriers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported carrier: {carrier_code}. Supported carriers: {', '.join(self.carriers.keys())}"
            )
        return self.carriers[carrier_code]
    
    def get_status(self, carrier_code: str, tracking_number: str) -> dict:
        """Get tracking status for a package"""
        tracker = self.get_tracker(carrier_code)
        return tracker.get_status(tracking_number)
    
    def get_supported_carriers(self) -> list:
        """Get list of supported carriers"""
        return list(self.carriers.keys())

tracking_service = TrackingService()
