import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from app.strategies import keydelivery
from app.data.carriers import CARRIERS

class TestKeyDelivery(unittest.TestCase):
    def setUp(self):
        os.environ["KEYDELIVERY_API_KEY"] = "test_key"

    @patch("app.strategies.keydelivery.settings")
    @patch("app.strategies.keydelivery.requests.post")
    def test_track_success(self, mock_post, mock_settings):
        # Mock settings
        mock_settings.KD100_APIKEY = "test_key"
        mock_settings.KD100_SECRET = "test_secret"
        
        # Mock response with correct format
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 200,
            "message": "ok",
            "data": {
                "order_status_code": 4,  # Delivered
                "items": [
                    {
                        "order_status_description": "Delivered to recipient",
                        "time": "2023-01-01 12:00:00",
                        "location": "Madrid",
                        "context": "Delivered"
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = keydelivery.track("123456789", "spain_correos_es")

        self.assertEqual(result["status"], "Delivered")
        self.assertEqual(result["location"], "Madrid")
        self.assertEqual(len(result["history"]), 1)
        self.assertIsNone(result["error"])

    def test_carriers_list(self):
        """Test that supported carriers are available."""
        carrier_ids = [carrier_id for carrier_id, _ in CARRIERS]
        self.assertIsInstance(carrier_ids, list)
        self.assertIn("spain_correos_es", carrier_ids)

if __name__ == "__main__":
    unittest.main()
