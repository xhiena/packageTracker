# packageTracker
A simple shipping package tracker with modular carrier support.

## Phase 4: Modular Tracking Service (Strategy Pattern) ✓

This project implements a flexible tracking service using the Strategy Pattern to support multiple shipping carriers.

### Features

- **Abstract Interface**: `CarrierTracker` base class for carrier implementations
- **Multiple Carriers**: Support for Correos, GLS, and SEUR carriers
- **Factory Pattern**: `TrackingService` for easy carrier selection
- **Mock Data**: All carriers return realistic mock tracking data
- **Comprehensive Tests**: 18 unit tests covering all functionality
- **Well Documented**: Complete API documentation and usage examples

### Quick Start

```python
from app.tracking.service import TrackingService

# Get tracking status
status = TrackingService.get_status("correos", "PK123456789ES")
print(f"Status: {status['status']}")
print(f"Location: {status['location']}")

# List available carriers
carriers = TrackingService.get_available_carriers()
print(f"Available carriers: {carriers}")
```

### Project Structure

```
packageTracker/
├── app/
│   └── tracking/
│       ├── interface.py          # CarrierTracker ABC
│       ├── service.py            # TrackingService factory
│       ├── carriers/             # Carrier implementations
│       │   ├── correos.py
│       │   ├── gls.py
│       │   └── seur.py
│       └── README.md             # Detailed documentation
├── tests/
│   └── test_tracking.py          # Test suite (18 tests)
└── demo.py                       # Demo script
```

### Running Tests

```bash
python -m unittest tests.test_tracking -v
```

### Demo

```bash
python demo.py
```

See [app/tracking/README.md](app/tracking/README.md) for detailed documentation.
