import re
from typing import Dict, Any
from app.strategies.base import TrackingStrategy


class GLSStrategy(TrackingStrategy):
    """Tracking strategy for GLS (General Logistics Systems)."""
    
    @property
    def carrier_name(self) -> str:
        return "gls"
    
    def validate_tracking_number(self, tracking_number: str) -> bool:
        """Validate GLS tracking number format.
        
        GLS tracking numbers are typically 11 digits.
        """
        pattern = r'^\d{11}$'
        return bool(re.match(pattern, tracking_number))
    
    def track(self, tracking_number: str) -> Dict[str, Any]:
        """Track a GLS package.
        
        Note: This is a mock implementation. In production, this would
        integrate with the actual GLS API or scrape their website.
        """
        if not self.validate_tracking_number(tracking_number):
            return {
                "status": "error",
                "location": None,
                "history": [],
                "error": "Invalid GLS tracking number format"
            }
        
        # Mock tracking data
        # In production, this would make real API calls or web scraping
        return {
            "status": "Out for Delivery",
            "location": "Local Delivery Depot",
            "history": [
                {
                    "timestamp": "2024-01-14T14:20:00",
                    "status": "Package received at depot",
                    "location": "Regional Hub"
                },
                {
                    "timestamp": "2024-01-15T09:45:00",
                    "status": "In transit",
                    "location": "Distribution Center"
                },
                {
                    "timestamp": "2024-01-16T07:30:00",
                    "status": "Out for delivery",
                    "location": "Local Delivery Depot"
                }
            ],
            "error": None
        }
