# Package Tracker API

A simple shipping package tracker built with FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- **User Authentication**: JWT-based authentication to secure API endpoints
- **Package Management**: Create, list, and track packages from multiple carriers
- **Multi-Carrier Support**: Supports Correos, GLS, and SEUR carriers (mock implementations)
- **Status Tracking**: Real-time package status updates from carrier APIs

## Phase 5: Package API Endpoints

This implementation includes the following endpoints:

### POST /packages
Add a new package for the authenticated user.
- Requires authentication via JWT token
- Accepts `tracking_number`, `carrier_code`, and optional `nickname`
- Calls the Tracking Service to get initial status
- Saves package details and initial status to the database

### GET /packages
List all packages for the authenticated user.
- Requires authentication
- Returns all packages belonging to the current user

### GET /packages/{package_id}/status
Fetch the latest status for a specific package.
- Requires authentication
- Calls the Tracking Service to check the external API
- Updates the `status_data` in the database
- Returns both package details and current status

## Installation

1. Clone the repository:
```bash
git clone https://github.com/xhiena/packageTracker.git
cd packageTracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
uvicorn main:app --reload --port 8000
```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
packageTracker/
├── app/
│   ├── auth/              # Authentication utilities and schemas
│   │   ├── security.py    # JWT and password hashing
│   │   └── schemas.py     # Auth-related Pydantic models
│   ├── db/                # Database configuration
│   │   └── database.py    # SQLAlchemy setup
│   ├── models/            # Database models
│   │   ├── user.py        # User model
│   │   └── package.py     # Package model
│   ├── package/           # Package endpoints (Phase 5)
│   │   ├── router.py      # Package API endpoints
│   │   └── schemas.py     # Package-related Pydantic models
│   └── tracking/          # Tracking service (Phase 4)
│       ├── interface.py   # CarrierTracker interface
│       ├── service.py     # Tracking service layer
│       └── carriers/      # Carrier implementations
│           ├── correos.py # Correos tracker
│           ├── gls.py     # GLS tracker
│           └── seur.py    # SEUR tracker
├── tests/                 # Test suite
│   └── test_package_api.py
├── main.py                # FastAPI application entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Supported Carriers

- **CORREOS**: Spanish postal service
- **GLS**: General Logistics Systems
- **SEUR**: Spanish courier service

Note: Current implementations are mocked for demonstration purposes.
