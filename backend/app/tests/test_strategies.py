import pytest
from unittest.mock import patch, MagicMock
from app.strategies import keydelivery
from app.data.carriers import CARRIERS


class TestKeyDeliveryService:
    """Test KeyDelivery tracking service."""
    
    def test_validate_tracking_number(self):
        """Test validation."""
        assert keydelivery.validate_tracking_number("AB123456789ES") is True
        assert keydelivery.validate_tracking_number("12345") is True
        assert keydelivery.validate_tracking_number("") is False
        assert keydelivery.validate_tracking_number("123") is False
    
    @patch("app.strategies.keydelivery.settings")
    @patch("app.strategies.keydelivery.requests.post")
    def test_detect_carrier_single(self, mock_post, mock_settings):
        """Test carrier detection with single result."""
        mock_settings.KD100_APIKEY = "test_key"
        mock_settings.KD100_SECRET = "test_secret"
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 200,
            "message": "OK",
            "data": [{"carrier_id": "dhl", "carrier_name": "DHL"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        carriers = keydelivery.detect_carrier("123456789")
        
        assert len(carriers) == 1
        assert carriers[0]["carrier_id"] == "dhl"
    
    @patch("app.strategies.keydelivery.settings")
    @patch("app.strategies.keydelivery.requests.post")
    def test_track_success(self, mock_post, mock_settings):
        """Test tracking with valid response."""
        mock_settings.KD100_APIKEY = "test_key"
        mock_settings.KD100_SECRET = "test_secret"
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 200,
            "message": "OK",
            "data": {
                "carrier_id": "dhl",
                "order_status_code": 4,
                "items": [
                    {
                        "context": "Delivered",
                        "time": "2023-01-01 12:00:00",
                        "order_status_description": "Delivered",
                        "location": "Madrid"
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = keydelivery.track("123456789", "dhl")
        
        assert result["error"] is None
        assert result["status"] == "Delivered"
        assert len(result["history"]) == 1
    
    @patch("app.strategies.keydelivery.settings")
    @patch("app.strategies.keydelivery.requests.post")
    def test_track_api_error(self, mock_post, mock_settings):
        """Test tracking with API error."""
        mock_settings.KD100_APIKEY = "test_key"
        mock_settings.KD100_SECRET = "test_secret"
        
        mock_post.side_effect = Exception("API Error")
        
        result = keydelivery.track("123456789", "dhl")
        
        assert result["error"] is not None
        assert result["status"] == "error"


class TestSupportedCarriers:
    """Test supported carriers list."""
    
    def test_carriers_list(self):
        """Test that carriers list is available and contains expected carriers."""
        carrier_ids = [carrier_id for carrier_id, _ in CARRIERS]
        assert isinstance(carrier_ids, list)
        assert "spain_correos_es" in carrier_ids
        assert "gls" in carrier_ids
        assert "seur" in carrier_ids
        assert "dhlen" in carrier_ids
        assert "ups" in carrier_ids
        assert "fedex" in carrier_ids
