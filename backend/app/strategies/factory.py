from typing import Dict, Type
from app.strategies.base import TrackingStrategy
from app.strategies.correos import CorreosStrategy
from app.strategies.gls import GLSStrategy
from app.strategies.seur import SEURStrategy


class TrackingStrategyFactory:
    """Factory class to get the appropriate tracking strategy for a carrier.
    
    This is part of the Strategy Pattern implementation.
    """
    
    _strategies: Dict[str, Type[TrackingStrategy]] = {
        "correos": CorreosStrategy,
        "gls": GLSStrategy,
        "seur": SEURStrategy,
    }
    
    @classmethod
    def get_strategy(cls, carrier: str) -> TrackingStrategy:
        """Get a tracking strategy instance for the specified carrier.
        
        Args:
            carrier: The carrier name (e.g., 'correos', 'gls')
            
        Returns:
            An instance of the appropriate TrackingStrategy
            
        Raises:
            ValueError: If the carrier is not supported
        """
        carrier_lower = carrier.lower()
        strategy_class = cls._strategies.get(carrier_lower)
        
        if not strategy_class:
            raise ValueError(f"Unsupported carrier: {carrier}")
        
        return strategy_class()
    
    @classmethod
    def get_supported_carriers(cls) -> list:
        """Get list of supported carriers.
        
        Returns:
            List of supported carrier names
        """
        return list(cls._strategies.keys())
