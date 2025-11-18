"""
SEUR Carrier Implementation

Mock implementation of the CarrierTracker interface for SEUR.
"""
from ..interface import CarrierTracker


class SEURTracker(CarrierTracker):
    """
    Mock implementation for SEUR carrier tracking.
    
    Returns simulated tracking data based on the tracking number.
    """
    
    def get_status(self, tracking_number: str) -> dict:
        """
        Retrieve mock tracking status for SEUR.
        
        Args:
            tracking_number: The tracking number to query
            
        Returns:
            A dictionary containing mock tracking status information
        """
        return {
            "carrier": "SEUR",
            "tracking_number": tracking_number,
            "status": "delivered",
            "last_update": "2025-11-17T16:45:00Z",
            "location": "Recipient Address - Sevilla",
            "estimated_delivery": "2025-11-17",
            "delivered_at": "2025-11-17T16:45:00Z",
            "signed_by": "Customer",
            "events": [
                {
                    "timestamp": "2025-11-17T16:45:00Z",
                    "status": "delivered",
                    "location": "Recipient Address - Sevilla",
                    "description": "Package delivered successfully"
                },
                {
                    "timestamp": "2025-11-17T14:30:00Z",
                    "status": "out_for_delivery",
                    "location": "Sevilla Distribution Center",
                    "description": "Out for delivery"
                },
                {
                    "timestamp": "2025-11-17T08:00:00Z",
                    "status": "arrived_at_depot",
                    "location": "Sevilla Distribution Center",
                    "description": "Arrived at distribution center"
                }
            ]
        }
