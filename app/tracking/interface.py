from abc import ABC, abstractmethod


class CarrierTracker(ABC):
    """
    Abstract base class for carrier tracking implementations.
    All carrier implementations must implement the get_status method.
    """
    
    @abstractmethod
    def get_status(self, tracking_number: str) -> dict:
        """
        Get the tracking status for a package.
        
        Args:
            tracking_number: The tracking number of the package
            
        Returns:
            A dictionary containing the tracking status information
        """
        pass
