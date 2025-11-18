import pytest
from app.tracking.carriers.correos import CorreosTracker
from app.tracking.carriers.gls import GLSTracker
from app.tracking.carriers.seur import SEURTracker
from app.tracking.service import TrackingService


class TestCorreosCarrier:
    """Test Correos carrier implementation."""
    
    def test_correos_returns_expected_structure(self):
        """Test that Correos carrier returns expected data structure."""
        tracker = CorreosTracker()
        result = tracker.get_status("TEST123456")
        
        # Verify structure
        assert isinstance(result, dict)
        assert "carrier" in result
        assert "tracking_number" in result
        assert "status" in result
        assert "events" in result
        assert "estimated_delivery" in result
        
        # Verify values
        assert result["carrier"] == "correos"
        assert result["tracking_number"] == "TEST123456"
        assert isinstance(result["events"], list)
        assert len(result["events"]) > 0
    
    def test_correos_events_have_required_fields(self):
        """Test that Correos events contain required fields."""
        tracker = CorreosTracker()
        result = tracker.get_status("TEST123456")
        
        for event in result["events"]:
            assert "timestamp" in event
            assert "location" in event
            assert "description" in event
            assert isinstance(event["timestamp"], str)
            assert isinstance(event["location"], str)
            assert isinstance(event["description"], str)
    
    def test_correos_with_different_tracking_numbers(self):
        """Test Correos with different tracking numbers."""
        tracker = CorreosTracker()
        result1 = tracker.get_status("ABC123")
        result2 = tracker.get_status("XYZ789")
        
        assert result1["tracking_number"] == "ABC123"
        assert result2["tracking_number"] == "XYZ789"
        assert result1["carrier"] == "correos"
        assert result2["carrier"] == "correos"


class TestGLSCarrier:
    """Test GLS carrier implementation."""
    
    def test_gls_returns_expected_structure(self):
        """Test that GLS carrier returns expected data structure."""
        tracker = GLSTracker()
        result = tracker.get_status("GLS456789")
        
        # Verify structure
        assert isinstance(result, dict)
        assert "carrier" in result
        assert "tracking_number" in result
        assert "status" in result
        assert "events" in result
        assert "estimated_delivery" in result
        
        # Verify values
        assert result["carrier"] == "gls"
        assert result["tracking_number"] == "GLS456789"
        assert isinstance(result["events"], list)
        assert len(result["events"]) > 0
    
    def test_gls_events_have_required_fields(self):
        """Test that GLS events contain required fields."""
        tracker = GLSTracker()
        result = tracker.get_status("GLS456789")
        
        for event in result["events"]:
            assert "timestamp" in event
            assert "location" in event
            assert "description" in event
    
    def test_gls_status_values(self):
        """Test GLS status contains valid values."""
        tracker = GLSTracker()
        result = tracker.get_status("GLS123")
        
        assert result["status"] in ["pending", "in_transit", "delivered", "failed"]


class TestSEURCarrier:
    """Test SEUR carrier implementation."""
    
    def test_seur_returns_expected_structure(self):
        """Test that SEUR carrier returns expected data structure."""
        tracker = SEURTracker()
        result = tracker.get_status("SEUR789")
        
        # Verify structure
        assert isinstance(result, dict)
        assert "carrier" in result
        assert "tracking_number" in result
        assert "status" in result
        assert "events" in result
        assert "estimated_delivery" in result
        
        # Verify values
        assert result["carrier"] == "seur"
        assert result["tracking_number"] == "SEUR789"
        assert isinstance(result["events"], list)
    
    def test_seur_events_structure(self):
        """Test SEUR events have proper structure."""
        tracker = SEURTracker()
        result = tracker.get_status("SEUR789")
        
        assert len(result["events"]) > 0
        for event in result["events"]:
            assert "timestamp" in event
            assert "location" in event
            assert "description" in event


class TestTrackingService:
    """Test the tracking service factory."""
    
    def test_get_tracker_correos(self):
        """Test getting Correos tracker from service."""
        tracker = TrackingService.get_tracker("correos")
        assert isinstance(tracker, CorreosTracker)
    
    def test_get_tracker_gls(self):
        """Test getting GLS tracker from service."""
        tracker = TrackingService.get_tracker("gls")
        assert isinstance(tracker, GLSTracker)
    
    def test_get_tracker_seur(self):
        """Test getting SEUR tracker from service."""
        tracker = TrackingService.get_tracker("seur")
        assert isinstance(tracker, SEURTracker)
    
    def test_get_tracker_case_insensitive(self):
        """Test that carrier codes are case insensitive."""
        tracker1 = TrackingService.get_tracker("CORREOS")
        tracker2 = TrackingService.get_tracker("Correos")
        tracker3 = TrackingService.get_tracker("correos")
        
        assert isinstance(tracker1, CorreosTracker)
        assert isinstance(tracker2, CorreosTracker)
        assert isinstance(tracker3, CorreosTracker)
    
    def test_get_tracker_unsupported_carrier(self):
        """Test that unsupported carrier raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            TrackingService.get_tracker("unsupported_carrier")
        
        assert "unsupported" in str(excinfo.value).lower()
    
    def test_track_package_end_to_end(self):
        """Test tracking a package end-to-end."""
        result = TrackingService.track_package("correos", "TEST123")
        
        assert result["carrier"] == "correos"
        assert result["tracking_number"] == "TEST123"
        assert "status" in result
        assert "events" in result
    
    def test_track_package_different_carriers(self):
        """Test tracking packages with different carriers."""
        correos_result = TrackingService.track_package("correos", "C123")
        gls_result = TrackingService.track_package("gls", "G123")
        seur_result = TrackingService.track_package("seur", "S123")
        
        assert correos_result["carrier"] == "correos"
        assert gls_result["carrier"] == "gls"
        assert seur_result["carrier"] == "seur"
        
        assert correos_result["tracking_number"] == "C123"
        assert gls_result["tracking_number"] == "G123"
        assert seur_result["tracking_number"] == "S123"


class TestCarrierDataConsistency:
    """Test that all carriers return consistent data structures."""
    
    def test_all_carriers_return_same_structure(self):
        """Test that all carriers return the same data structure."""
        carriers = [
            ("correos", CorreosTracker()),
            ("gls", GLSTracker()),
            ("seur", SEURTracker()),
        ]
        
        required_keys = {"carrier", "tracking_number", "status", "events", "estimated_delivery"}
        
        for carrier_name, tracker in carriers:
            result = tracker.get_status("TEST123")
            
            # Check all required keys are present
            assert set(result.keys()) == required_keys, f"{carrier_name} missing required keys"
            
            # Check types
            assert isinstance(result["carrier"], str)
            assert isinstance(result["tracking_number"], str)
            assert isinstance(result["status"], str)
            assert isinstance(result["events"], list)
            assert isinstance(result["estimated_delivery"], str)
    
    def test_all_carriers_event_structure(self):
        """Test that all carriers have consistent event structure."""
        carriers = [
            CorreosTracker(),
            GLSTracker(),
            SEURTracker(),
        ]
        
        required_event_keys = {"timestamp", "location", "description"}
        
        for tracker in carriers:
            result = tracker.get_status("TEST123")
            
            for event in result["events"]:
                assert set(event.keys()) == required_event_keys
                assert isinstance(event["timestamp"], str)
                assert isinstance(event["location"], str)
                assert isinstance(event["description"], str)
