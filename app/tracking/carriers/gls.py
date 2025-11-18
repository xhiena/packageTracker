"""
GLS Carrier Implementation

Mock implementation of the CarrierTracker interface for GLS.
"""
from ..interface import CarrierTracker


class GLSTracker(CarrierTracker):
    """
    Mock implementation for GLS carrier tracking.
    
    Returns simulated tracking data based on the tracking number.
    """
    
    def get_status(self, tracking_number: str) -> dict:
        """
        Retrieve mock tracking status for GLS.
        
        Args:
            tracking_number: The tracking number to query
            
        Returns:
            A dictionary containing mock tracking status information
        """
        return {
            "carrier": "GLS",
            "tracking_number": tracking_number,
            "status": "out_for_delivery",
            "last_update": "2025-11-18T08:00:00Z",
            "location": "Local Depot - Valencia",
            "estimated_delivery": "2025-11-18",
            "events": [
                {
                    "timestamp": "2025-11-18T08:00:00Z",
                    "status": "out_for_delivery",
                    "location": "Local Depot - Valencia",
                    "description": "Out for delivery"
                },
                {
                    "timestamp": "2025-11-17T22:45:00Z",
                    "status": "arrived_at_depot",
                    "location": "Valencia Hub",
                    "description": "Arrived at local depot"
                },
                {
                    "timestamp": "2025-11-17T16:30:00Z",
                    "status": "in_transit",
                    "location": "Regional Sorting Center",
                    "description": "Package in transit"
                }
            ]
        }
