from app.tracking.interface import CarrierTracker
from app.tracking.carriers.correos import CorreosTracker
from app.tracking.carriers.gls import GLSTracker
from app.tracking.carriers.seur import SEURTracker


class TrackingService:
    """
    Service layer that manages carrier tracking implementations.
    Uses a factory pattern to select the correct tracker based on carrier code.
    """
    
    _trackers = {
        "correos": CorreosTracker(),
        "gls": GLSTracker(),
        "seur": SEURTracker(),
    }
    
    @classmethod
    def get_tracker(cls, carrier_code: str) -> CarrierTracker:
        """
        Get the appropriate tracker for a carrier code.
        
        Args:
            carrier_code: The carrier code (e.g., 'correos', 'gls', 'seur')
            
        Returns:
            The carrier tracker implementation
            
        Raises:
            ValueError: If carrier code is not supported
        """
        carrier_code = carrier_code.lower()
        tracker = cls._trackers.get(carrier_code)
        if not tracker:
            raise ValueError(f"Unsupported carrier: {carrier_code}")
        return tracker
    
    @classmethod
    def track_package(cls, carrier_code: str, tracking_number: str) -> dict:
        """
        Track a package using the appropriate carrier.
        
        Args:
            carrier_code: The carrier code
            tracking_number: The tracking number
            
        Returns:
            The tracking status dictionary
        """
        tracker = cls.get_tracker(carrier_code)
        return tracker.get_status(tracking_number)
