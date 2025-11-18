# Tracking Module

This module implements a modular tracking service using the Strategy Pattern to support multiple shipping carriers.

## Architecture

### Strategy Pattern Implementation

The module follows the Strategy Pattern to allow flexible carrier-specific tracking implementations:

```
app/tracking/
├── interface.py          # Abstract base class (CarrierTracker)
├── service.py            # Factory service for carrier selection
└── carriers/             # Carrier-specific implementations
    ├── correos.py        # Correos carrier tracker
    ├── gls.py            # GLS carrier tracker
    └── seur.py           # SEUR carrier tracker
```

## Components

### 1. CarrierTracker Interface (`interface.py`)

Abstract base class defining the contract for all carrier implementations:

```python
from abc import ABC, abstractmethod

class CarrierTracker(ABC):
    @abstractmethod
    def get_status(self, tracking_number: str) -> dict:
        """Retrieve tracking status for a given tracking number."""
        pass
```

### 2. Carrier Implementations (`carriers/`)

Each carrier has its own implementation file that inherits from `CarrierTracker`:

- **correos.py**: Correos (Spanish postal service) tracker
- **gls.py**: GLS (General Logistics Systems) tracker
- **seur.py**: SEUR carrier tracker

All implementations currently return **mock data** simulating successful API responses.

### 3. TrackingService (`service.py`)

Factory service that manages carrier selection and provides convenience methods:

```python
from app.tracking.service import TrackingService

# Get a specific tracker
tracker = TrackingService.get_tracker("correos")
status = tracker.get_status("PK123456789ES")

# Or use the convenience method
status = TrackingService.get_status("correos", "PK123456789ES")

# List available carriers
carriers = TrackingService.get_available_carriers()
# Returns: ['correos', 'gls', 'seur']
```

## Usage Examples

### Basic Usage

```python
from app.tracking.service import TrackingService

# Track a package with Correos
result = TrackingService.get_status("correos", "PK123456789ES")
print(f"Status: {result['status']}")
print(f"Location: {result['location']}")
```

### Direct Tracker Usage

```python
from app.tracking.carriers.gls import GLSTracker

tracker = GLSTracker()
status = tracker.get_status("GLS987654321")
```

### Error Handling

```python
result = TrackingService.get_status("unknown_carrier", "TEST123")
if "error" in result:
    print(f"Error: {result['error']}")
    print(f"Available carriers: {result['available_carriers']}")
```

## Response Format

All carriers return a dictionary with the following structure:

```python
{
    "carrier": "Correos",                    # Carrier name
    "tracking_number": "PK123456789ES",      # Tracking number queried
    "status": "in_transit",                  # Current status
    "last_update": "2025-11-18T10:30:00Z",  # Last update timestamp
    "location": "Madrid Distribution Center", # Current location
    "estimated_delivery": "2025-11-20",      # Estimated delivery date
    "events": [                              # Tracking history
        {
            "timestamp": "2025-11-18T10:30:00Z",
            "status": "in_transit",
            "location": "Madrid Distribution Center",
            "description": "Package is in transit"
        },
        # ... more events
    ]
}
```

### Status Values

Common status values include:
- `picked_up`: Package picked up from sender
- `in_transit`: Package in transit
- `arrived_at_depot`: Package at distribution center
- `out_for_delivery`: Out for delivery
- `delivered`: Package delivered

## Adding New Carriers

To add a new carrier:

1. Create a new file in `app/tracking/carriers/` (e.g., `newcarrier.py`)
2. Implement the `CarrierTracker` interface:

```python
from ..interface import CarrierTracker

class NewCarrierTracker(CarrierTracker):
    def get_status(self, tracking_number: str) -> dict:
        # Implement your tracking logic here
        return {
            "carrier": "NewCarrier",
            "tracking_number": tracking_number,
            # ... other fields
        }
```

3. Register in `service.py`:

```python
from .carriers.newcarrier import NewCarrierTracker

class TrackingService:
    _carriers = {
        # ... existing carriers
        "newcarrier": NewCarrierTracker,
    }
```

## Testing

Run the test suite:

```bash
python -m unittest tests.test_tracking -v
```

Run the demo script:

```bash
python demo.py
```

## Notes

- All current implementations return **mock data** for demonstration purposes
- In production, replace mock implementations with actual API calls
- Carrier codes are case-insensitive (`"correos"`, `"CORREOS"`, `"Correos"` all work)
- Unknown carrier codes return an error dict with available carriers list
