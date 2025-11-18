from app.tracking.interface import CarrierTracker


class SEURTracker(CarrierTracker):
    """Mock implementation of SEUR carrier tracker."""
    
    def get_status(self, tracking_number: str) -> dict:
        """
        Mock method that returns sample tracking data for SEUR.
        
        Args:
            tracking_number: The tracking number
            
        Returns:
            Sample tracking status dictionary
        """
        return {
            "carrier": "seur",
            "tracking_number": tracking_number,
            "status": "pending",
            "events": [
                {
                    "timestamp": "2025-11-18T08:00:00",
                    "location": "Sevilla",
                    "description": "Package registered"
                }
            ],
            "estimated_delivery": "2025-11-22T18:00:00"
        }
