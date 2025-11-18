from app.tracking.interface import CarrierTracker


class GLSTracker(CarrierTracker):
    """Mock implementation of GLS carrier tracker."""
    
    def get_status(self, tracking_number: str) -> dict:
        """
        Mock method that returns sample tracking data for GLS.
        
        Args:
            tracking_number: The tracking number
            
        Returns:
            Sample tracking status dictionary
        """
        return {
            "carrier": "gls",
            "tracking_number": tracking_number,
            "status": "delivered",
            "events": [
                {
                    "timestamp": "2025-11-17T09:00:00",
                    "location": "Valencia",
                    "description": "Package received at depot"
                },
                {
                    "timestamp": "2025-11-17T15:00:00",
                    "location": "Valencia",
                    "description": "Out for delivery"
                },
                {
                    "timestamp": "2025-11-17T17:30:00",
                    "location": "Valencia",
                    "description": "Delivered"
                }
            ],
            "estimated_delivery": "2025-11-17T17:30:00"
        }
