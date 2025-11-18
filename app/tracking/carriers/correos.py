from app.tracking.interface import CarrierTracker


class CorreosTracker(CarrierTracker):
    """Mock implementation of Correos carrier tracker."""
    
    def get_status(self, tracking_number: str) -> dict:
        """
        Mock method that returns sample tracking data for Correos.
        
        Args:
            tracking_number: The tracking number
            
        Returns:
            Sample tracking status dictionary
        """
        return {
            "carrier": "correos",
            "tracking_number": tracking_number,
            "status": "in_transit",
            "events": [
                {
                    "timestamp": "2025-11-18T10:00:00",
                    "location": "Madrid",
                    "description": "Package picked up"
                },
                {
                    "timestamp": "2025-11-18T14:30:00",
                    "location": "Barcelona",
                    "description": "In transit"
                }
            ],
            "estimated_delivery": "2025-11-20T18:00:00"
        }
