from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class TrackingStrategy(ABC):
    """Base class for package tracking strategies.
    
    This implements the Strategy Pattern for different carrier tracking logic.
    """
    
    @abstractmethod
    def track(self, tracking_number: str) -> Dict[str, Any]:
        """Track a package by its tracking number.
        
        Args:
            tracking_number: The package tracking number
            
        Returns:
            Dictionary containing tracking information with keys:
            - status: Current status of the package
            - location: Current or last known location
            - history: List of tracking events
            - error: Error message if tracking failed
        """
        pass
    
    @abstractmethod
    def validate_tracking_number(self, tracking_number: str) -> bool:
        """Validate if a tracking number format is correct for this carrier.
        
        Args:
            tracking_number: The tracking number to validate
            
        Returns:
            True if the format is valid, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def carrier_name(self) -> str:
        """Return the name of the carrier."""
        pass
