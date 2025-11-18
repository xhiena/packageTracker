"""
Correos Carrier Implementation

Mock implementation of the CarrierTracker interface for Correos.
"""
from ..interface import CarrierTracker


class CorreosTracker(CarrierTracker):
    """
    Mock implementation for Correos carrier tracking.
    
    Returns simulated tracking data based on the tracking number.
    """
    
    def get_status(self, tracking_number: str) -> dict:
        """
        Retrieve mock tracking status for Correos.
        
        Args:
            tracking_number: The tracking number to query
            
        Returns:
            A dictionary containing mock tracking status information
        """
        return {
            "carrier": "Correos",
            "tracking_number": tracking_number,
            "status": "in_transit",
            "last_update": "2025-11-18T10:30:00Z",
            "location": "Madrid Distribution Center",
            "estimated_delivery": "2025-11-20",
            "events": [
                {
                    "timestamp": "2025-11-18T10:30:00Z",
                    "status": "in_transit",
                    "location": "Madrid Distribution Center",
                    "description": "Package is in transit"
                },
                {
                    "timestamp": "2025-11-17T14:20:00Z",
                    "status": "picked_up",
                    "location": "Barcelona Sorting Center",
                    "description": "Package picked up from sender"
                }
            ]
        }
