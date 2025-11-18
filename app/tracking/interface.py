from abc import ABC, abstractmethod

class CarrierTracker(ABC):
    @abstractmethod
    def get_status(self, tracking_number: str) -> dict:
        """
        Fetch tracking status for the given tracking number.
        
        Args:
            tracking_number: The package tracking number
            
        Returns:
            dict: A dictionary containing tracking status information
        """
        pass
