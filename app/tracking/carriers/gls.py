from app.tracking.interface import CarrierTracker
from datetime import datetime

class GLSTracker(CarrierTracker):
    def get_status(self, tracking_number: str) -> dict:
        """Mock implementation of GLS tracking"""
        return {
            "carrier": "GLS",
            "tracking_number": tracking_number,
            "status": "Out for Delivery",
            "location": "Local Delivery Hub",
            "estimated_delivery": "2025-11-19",
            "last_update": datetime.utcnow().isoformat(),
            "events": [
                {
                    "timestamp": "2025-11-17T08:00:00",
                    "location": "Origin Facility",
                    "description": "Package received"
                },
                {
                    "timestamp": "2025-11-18T06:00:00",
                    "location": "Local Delivery Hub",
                    "description": "Out for delivery"
                }
            ]
        }
