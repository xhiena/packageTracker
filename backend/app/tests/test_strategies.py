import pytest
from app.strategies.correos import CorreosStrategy
from app.strategies.gls import GLSStrategy
from app.strategies.factory import TrackingStrategyFactory


class TestCorreosStrategy:
    """Test Correos tracking strategy."""
    
    def test_carrier_name(self):
        """Test carrier name property."""
        strategy = CorreosStrategy()
        assert strategy.carrier_name == "correos"
    
    def test_validate_tracking_number_valid(self):
        """Test validation with valid tracking number."""
        strategy = CorreosStrategy()
        assert strategy.validate_tracking_number("AB123456789ES") is True
        assert strategy.validate_tracking_number("XY987654321FR") is True
    
    def test_validate_tracking_number_invalid(self):
        """Test validation with invalid tracking number."""
        strategy = CorreosStrategy()
        assert strategy.validate_tracking_number("123456789") is False
        assert strategy.validate_tracking_number("AB12345678ES") is False  # Too short
        assert strategy.validate_tracking_number("ABC123456789ES") is False  # Too many letters
        assert strategy.validate_tracking_number("AB12345678XES") is False  # Letter in number part
    
    def test_track_valid_number(self):
        """Test tracking with valid number."""
        strategy = CorreosStrategy()
        result = strategy.track("AB123456789ES")
        
        assert result["error"] is None
        assert "status" in result
        assert "location" in result
        assert "history" in result
        assert isinstance(result["history"], list)
    
    def test_track_invalid_number(self):
        """Test tracking with invalid number."""
        strategy = CorreosStrategy()
        result = strategy.track("invalid123")
        
        assert result["error"] is not None
        assert result["status"] == "error"


class TestGLSStrategy:
    """Test GLS tracking strategy."""
    
    def test_carrier_name(self):
        """Test carrier name property."""
        strategy = GLSStrategy()
        assert strategy.carrier_name == "gls"
    
    def test_validate_tracking_number_valid(self):
        """Test validation with valid tracking number."""
        strategy = GLSStrategy()
        assert strategy.validate_tracking_number("12345678901") is True
        assert strategy.validate_tracking_number("98765432109") is True
    
    def test_validate_tracking_number_invalid(self):
        """Test validation with invalid tracking number."""
        strategy = GLSStrategy()
        assert strategy.validate_tracking_number("123456789") is False  # Too short
        assert strategy.validate_tracking_number("123456789012") is False  # Too long
        assert strategy.validate_tracking_number("1234567890A") is False  # Contains letter
    
    def test_track_valid_number(self):
        """Test tracking with valid number."""
        strategy = GLSStrategy()
        result = strategy.track("12345678901")
        
        assert result["error"] is None
        assert "status" in result
        assert "location" in result
        assert "history" in result
        assert isinstance(result["history"], list)
    
    def test_track_invalid_number(self):
        """Test tracking with invalid number."""
        strategy = GLSStrategy()
        result = strategy.track("invalid")
        
        assert result["error"] is not None
        assert result["status"] == "error"


class TestTrackingStrategyFactory:
    """Test the tracking strategy factory."""
    
    def test_get_supported_carriers(self):
        """Test getting list of supported carriers."""
        carriers = TrackingStrategyFactory.get_supported_carriers()
        assert isinstance(carriers, list)
        assert "correos" in carriers
        assert "gls" in carriers
    
    def test_get_strategy_correos(self):
        """Test getting Correos strategy."""
        strategy = TrackingStrategyFactory.get_strategy("correos")
        assert isinstance(strategy, CorreosStrategy)
        assert strategy.carrier_name == "correos"
    
    def test_get_strategy_gls(self):
        """Test getting GLS strategy."""
        strategy = TrackingStrategyFactory.get_strategy("gls")
        assert isinstance(strategy, GLSStrategy)
        assert strategy.carrier_name == "gls"
    
    def test_get_strategy_case_insensitive(self):
        """Test that carrier names are case-insensitive."""
        strategy1 = TrackingStrategyFactory.get_strategy("CORREOS")
        strategy2 = TrackingStrategyFactory.get_strategy("Correos")
        assert isinstance(strategy1, CorreosStrategy)
        assert isinstance(strategy2, CorreosStrategy)
    
    def test_get_strategy_unsupported(self):
        """Test getting strategy for unsupported carrier."""
        with pytest.raises(ValueError, match="Unsupported carrier"):
            TrackingStrategyFactory.get_strategy("unsupported")
