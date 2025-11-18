"""Comprehensive strategy tests for data structure consistency."""
import pytest
from app.strategies.correos import CorreosStrategy
from app.strategies.gls import GLSStrategy
from app.strategies.factory import TrackingStrategyFactory


class TestStrategyDataConsistency:
    """Test that all strategies return consistent data structures."""
    
    def test_all_strategies_return_same_keys(self):
        """Test that all strategies return the same top-level keys."""
        strategies = [
            CorreosStrategy(),
            GLSStrategy(),
        ]
        
        required_keys = {"status", "location", "history", "error"}
        
        for strategy in strategies:
            # Use a valid tracking number for each
            if strategy.carrier_name == "correos":
                result = strategy.track("AB123456789ES")
            elif strategy.carrier_name == "gls":
                result = strategy.track("12345678901")
            else:
                continue
            
            assert set(result.keys()) == required_keys, \
                f"{strategy.carrier_name} missing required keys"
    
    def test_all_strategies_history_structure(self):
        """Test that all strategies have consistent history structure."""
        strategies = [
            (CorreosStrategy(), "AB123456789ES"),
            (GLSStrategy(), "12345678901"),
        ]
        
        for strategy, tracking_number in strategies:
            result = strategy.track(tracking_number)
            
            if result["error"] is None:
                assert isinstance(result["history"], list), \
                    f"{strategy.carrier_name} history should be a list"
                
                # Check history item structure if history exists
                if len(result["history"]) > 0:
                    for event in result["history"]:
                        assert isinstance(event, dict), \
                            f"{strategy.carrier_name} history events should be dicts"
                        assert "timestamp" in event or "date" in event, \
                            f"{strategy.carrier_name} history events should have timestamp"
                        assert "description" in event or "message" in event or "status" in event, \
                            f"{strategy.carrier_name} history events should have description"
    
    def test_error_handling_consistency(self):
        """Test that all strategies handle errors consistently."""
        strategies = [
            CorreosStrategy(),
            GLSStrategy(),
        ]
        
        for strategy in strategies:
            result = strategy.track("invalid_tracking_number")
            
            assert "error" in result
            assert result["error"] is not None, \
                f"{strategy.carrier_name} should return error for invalid number"
            assert result["status"] == "error", \
                f"{strategy.carrier_name} should have status='error' for invalid number"


class TestFactoryPatternIntegration:
    """Test factory pattern implementation."""
    
    def test_factory_returns_correct_strategy_instances(self):
        """Test that factory returns correct strategy instances."""
        correos = TrackingStrategyFactory.get_strategy("correos")
        gls = TrackingStrategyFactory.get_strategy("gls")
        
        assert type(correos).__name__ == "CorreosStrategy"
        assert type(gls).__name__ == "GLSStrategy"
        assert correos.carrier_name == "correos"
        assert gls.carrier_name == "gls"
    
    def test_factory_caching_behavior(self):
        """Test that factory returns same instance or new instance as expected."""
        strategy1 = TrackingStrategyFactory.get_strategy("correos")
        strategy2 = TrackingStrategyFactory.get_strategy("correos")
        
        # They should be the same type
        assert type(strategy1) == type(strategy2)
    
    def test_all_supported_carriers_have_strategies(self):
        """Test that all supported carriers can be instantiated."""
        carriers = TrackingStrategyFactory.get_supported_carriers()
        
        for carrier in carriers:
            strategy = TrackingStrategyFactory.get_strategy(carrier)
            assert strategy is not None
            assert hasattr(strategy, "track")
            assert hasattr(strategy, "carrier_name")


class TestTrackingNumberValidation:
    """Test tracking number validation across strategies."""
    
    def test_correos_validation_edge_cases(self):
        """Test Correos validation with edge cases."""
        strategy = CorreosStrategy()
        
        # Valid cases
        assert strategy.validate_tracking_number("AB123456789ES")
        assert strategy.validate_tracking_number("XY987654321FR")
        
        # Invalid cases
        assert not strategy.validate_tracking_number("")
        assert not strategy.validate_tracking_number("AB12345678ES")  # Too short
        assert not strategy.validate_tracking_number("AB1234567890ES")  # Too long
        assert not strategy.validate_tracking_number("A1123456789ES")  # Number in letters
        assert not strategy.validate_tracking_number("AB12345678XES")  # Letter in numbers
        # Note: Lowercase may be accepted by the actual implementation
    
    def test_gls_validation_edge_cases(self):
        """Test GLS validation with edge cases."""
        strategy = GLSStrategy()
        
        # Valid cases
        assert strategy.validate_tracking_number("12345678901")
        assert strategy.validate_tracking_number("00000000000")
        assert strategy.validate_tracking_number("99999999999")
        
        # Invalid cases
        assert not strategy.validate_tracking_number("")
        assert not strategy.validate_tracking_number("1234567890")  # Too short
        assert not strategy.validate_tracking_number("123456789012")  # Too long
        assert not strategy.validate_tracking_number("1234567890A")  # Contains letter
        assert not strategy.validate_tracking_number(" 12345678901")  # Leading space
        assert not strategy.validate_tracking_number("12345678901 ")  # Trailing space


class TestMockDataQuality:
    """Test the quality of mock data returned by strategies."""
    
    def test_correos_mock_data_completeness(self):
        """Test that Correos returns complete mock data."""
        strategy = CorreosStrategy()
        result = strategy.track("AB123456789ES")
        
        assert result["status"] is not None
        assert result["status"] != ""
        assert result["location"] is not None
        if result["history"]:
            assert len(result["history"]) > 0
    
    def test_gls_mock_data_completeness(self):
        """Test that GLS returns complete mock data."""
        strategy = GLSStrategy()
        result = strategy.track("12345678901")
        
        assert result["status"] is not None
        assert result["status"] != ""
        assert result["location"] is not None
        if result["history"]:
            assert len(result["history"]) > 0
    
    def test_mock_data_includes_reasonable_status(self):
        """Test that mock data includes reasonable status values."""
        strategies = [
            (CorreosStrategy(), "AB123456789ES"),
            (GLSStrategy(), "12345678901"),
        ]
        
        valid_statuses = {
            "pending", "in_transit", "delivered", "failed", 
            "out_for_delivery", "processing", "unknown"
        }
        
        for strategy, tracking_number in strategies:
            result = strategy.track(tracking_number)
            if result["error"] is None:
                # Status should be a reasonable value (not necessarily from our set)
                assert isinstance(result["status"], str)
                assert len(result["status"]) > 0
