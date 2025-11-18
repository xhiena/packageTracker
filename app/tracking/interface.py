"""
Tracking Interface Module

Defines the abstract base class for carrier tracking implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict


class CarrierTracker(ABC):
    """
    Abstract base class for carrier tracking implementations.
    
    All carrier-specific tracking implementations must inherit from this class
    and implement the get_status method.
    """
    
    @abstractmethod
    def get_status(self, tracking_number: str) -> dict:
        """
        Retrieve the tracking status for a given tracking number.
        
        Args:
            tracking_number: The tracking number to query
            
        Returns:
            A dictionary containing the tracking status information
        """
        pass
