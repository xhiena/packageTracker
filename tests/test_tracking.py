"""
Tests for the tracking module.

Tests the interface, carrier implementations, and service layer.
"""
import unittest
from app.tracking.interface import CarrierTracker
from app.tracking.carriers.correos import CorreosTracker
from app.tracking.carriers.gls import GLSTracker
from app.tracking.carriers.seur import SEURTracker
from app.tracking.service import TrackingService


class TestCarrierInterface(unittest.TestCase):
    """Test the CarrierTracker interface."""
    
    def test_correos_implements_interface(self):
        """Test that CorreosTracker implements CarrierTracker."""
        self.assertTrue(issubclass(CorreosTracker, CarrierTracker))
        
    def test_gls_implements_interface(self):
        """Test that GLSTracker implements CarrierTracker."""
        self.assertTrue(issubclass(GLSTracker, CarrierTracker))
        
    def test_seur_implements_interface(self):
        """Test that SEURTracker implements CarrierTracker."""
        self.assertTrue(issubclass(SEURTracker, CarrierTracker))


class TestCorreosTracker(unittest.TestCase):
    """Test the Correos carrier implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = CorreosTracker()
        
    def test_get_status_returns_dict(self):
        """Test that get_status returns a dictionary."""
        result = self.tracker.get_status("TEST123456")
        self.assertIsInstance(result, dict)
        
    def test_get_status_contains_required_fields(self):
        """Test that the status dict contains required fields."""
        result = self.tracker.get_status("TEST123456")
        self.assertIn("carrier", result)
        self.assertIn("tracking_number", result)
        self.assertIn("status", result)
        self.assertEqual(result["carrier"], "Correos")
        self.assertEqual(result["tracking_number"], "TEST123456")
        
    def test_get_status_includes_events(self):
        """Test that the status includes tracking events."""
        result = self.tracker.get_status("TEST123456")
        self.assertIn("events", result)
        self.assertIsInstance(result["events"], list)
        self.assertGreater(len(result["events"]), 0)


class TestGLSTracker(unittest.TestCase):
    """Test the GLS carrier implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = GLSTracker()
        
    def test_get_status_returns_dict(self):
        """Test that get_status returns a dictionary."""
        result = self.tracker.get_status("GLS789012")
        self.assertIsInstance(result, dict)
        
    def test_get_status_contains_required_fields(self):
        """Test that the status dict contains required fields."""
        result = self.tracker.get_status("GLS789012")
        self.assertIn("carrier", result)
        self.assertIn("tracking_number", result)
        self.assertIn("status", result)
        self.assertEqual(result["carrier"], "GLS")
        self.assertEqual(result["tracking_number"], "GLS789012")


class TestSEURTracker(unittest.TestCase):
    """Test the SEUR carrier implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = SEURTracker()
        
    def test_get_status_returns_dict(self):
        """Test that get_status returns a dictionary."""
        result = self.tracker.get_status("SEUR345678")
        self.assertIsInstance(result, dict)
        
    def test_get_status_contains_required_fields(self):
        """Test that the status dict contains required fields."""
        result = self.tracker.get_status("SEUR345678")
        self.assertIn("carrier", result)
        self.assertIn("tracking_number", result)
        self.assertIn("status", result)
        self.assertEqual(result["carrier"], "SEUR")
        self.assertEqual(result["tracking_number"], "SEUR345678")


class TestTrackingService(unittest.TestCase):
    """Test the TrackingService factory."""
    
    def test_get_tracker_correos(self):
        """Test getting a Correos tracker."""
        tracker = TrackingService.get_tracker("correos")
        self.assertIsInstance(tracker, CorreosTracker)
        
    def test_get_tracker_gls(self):
        """Test getting a GLS tracker."""
        tracker = TrackingService.get_tracker("gls")
        self.assertIsInstance(tracker, GLSTracker)
        
    def test_get_tracker_seur(self):
        """Test getting a SEUR tracker."""
        tracker = TrackingService.get_tracker("seur")
        self.assertIsInstance(tracker, SEURTracker)
        
    def test_get_tracker_case_insensitive(self):
        """Test that carrier code is case insensitive."""
        tracker_lower = TrackingService.get_tracker("correos")
        tracker_upper = TrackingService.get_tracker("CORREOS")
        tracker_mixed = TrackingService.get_tracker("Correos")
        
        self.assertIsInstance(tracker_lower, CorreosTracker)
        self.assertIsInstance(tracker_upper, CorreosTracker)
        self.assertIsInstance(tracker_mixed, CorreosTracker)
        
    def test_get_tracker_unknown_carrier(self):
        """Test getting a tracker for an unknown carrier."""
        tracker = TrackingService.get_tracker("unknown")
        self.assertIsNone(tracker)
        
    def test_get_status_via_service(self):
        """Test getting status directly via service."""
        result = TrackingService.get_status("correos", "TEST123")
        self.assertIsInstance(result, dict)
        self.assertIn("carrier", result)
        self.assertEqual(result["carrier"], "Correos")
        self.assertEqual(result["tracking_number"], "TEST123")
        
    def test_get_status_unknown_carrier(self):
        """Test getting status for unknown carrier."""
        result = TrackingService.get_status("unknown", "TEST123")
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("available_carriers", result)
        
    def test_get_available_carriers(self):
        """Test getting list of available carriers."""
        carriers = TrackingService.get_available_carriers()
        self.assertIsInstance(carriers, list)
        self.assertIn("correos", carriers)
        self.assertIn("gls", carriers)
        self.assertIn("seur", carriers)


if __name__ == "__main__":
    unittest.main()
