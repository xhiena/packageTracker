"""
Tracking Service Module

Provides a central factory for selecting and using carrier-specific tracking implementations.
"""
from typing import Optional
from .interface import CarrierTracker
from .carriers.correos import CorreosTracker
from .carriers.gls import GLSTracker
from .carriers.seur import SEURTracker


class TrackingService:
    """
    Central service for managing carrier tracking implementations.
    
    Provides a factory method to select the appropriate CarrierTracker
    based on the carrier code.
    """
    
    # Mapping of carrier codes to their respective tracker implementations
    _carriers = {
        "correos": CorreosTracker,
        "gls": GLSTracker,
        "seur": SEURTracker,
    }
    
    @classmethod
    def get_tracker(cls, carrier_code: str) -> Optional[CarrierTracker]:
        """
        Get a tracker instance for the specified carrier.
        
        Args:
            carrier_code: The carrier code (e.g., 'correos', 'gls', 'seur')
            
        Returns:
            An instance of CarrierTracker for the specified carrier, or None if not found
        """
        carrier_code_lower = carrier_code.lower()
        tracker_class = cls._carriers.get(carrier_code_lower)
        
        if tracker_class:
            return tracker_class()
        return None
    
    @classmethod
    def get_status(cls, carrier_code: str, tracking_number: str) -> dict:
        """
        Convenience method to get tracking status directly.
        
        Args:
            carrier_code: The carrier code (e.g., 'correos', 'gls', 'seur')
            tracking_number: The tracking number to query
            
        Returns:
            A dictionary containing the tracking status, or an error message
        """
        tracker = cls.get_tracker(carrier_code)
        
        if tracker:
            return tracker.get_status(tracking_number)
        else:
            return {
                "error": "Carrier not found",
                "carrier_code": carrier_code,
                "available_carriers": list(cls._carriers.keys())
            }
    
    @classmethod
    def get_available_carriers(cls) -> list:
        """
        Get a list of all available carrier codes.
        
        Returns:
            A list of carrier codes that are supported
        """
        return list(cls._carriers.keys())
