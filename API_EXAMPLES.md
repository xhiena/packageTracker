# Package Tracker API Examples

This document provides examples of how to use the Package Tracker API endpoints.

## Prerequisites

1. Start the server:
```bash
uvicorn main:app --reload --port 8000
```

2. You need a valid JWT token. For testing, you can create a user and login through the authentication endpoints (not implemented in this phase).

## Example Requests

### 1. Create a Package (POST /packages)

Create a new package for tracking:

```bash
curl -X POST "http://localhost:8000/packages" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tracking_number": "ES123456789",
    "carrier_code": "CORREOS",
    "nickname": "Birthday Gift"
  }'
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "tracking_number": "ES123456789",
  "carrier_code": "CORREOS",
  "nickname": "Birthday Gift",
  "status_data": {
    "carrier": "Correos",
    "tracking_number": "ES123456789",
    "status": "In Transit",
    "location": "Madrid Distribution Center",
    "estimated_delivery": "2025-11-20",
    "last_update": "2025-11-18T08:30:00",
    "events": [
      {
        "timestamp": "2025-11-18T10:00:00",
        "location": "Barcelona",
        "description": "Package picked up"
      }
    ]
  }
}
```

### 2. List All Packages (GET /packages)

Get all packages for the authenticated user:

```bash
curl -X GET "http://localhost:8000/packages" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "tracking_number": "ES123456789",
    "carrier_code": "CORREOS",
    "nickname": "Birthday Gift",
    "status_data": { ... }
  },
  {
    "id": 2,
    "user_id": 1,
    "tracking_number": "GLS987654321",
    "carrier_code": "GLS",
    "nickname": "Electronics Order",
    "status_data": { ... }
  }
]
```

### 3. Get Package Status (GET /packages/{package_id}/status)

Get the latest tracking status for a specific package:

```bash
curl -X GET "http://localhost:8000/packages/1/status" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "package": {
    "id": 1,
    "user_id": 1,
    "tracking_number": "ES123456789",
    "carrier_code": "CORREOS",
    "nickname": "Birthday Gift",
    "status_data": { ... }
  },
  "current_status": {
    "carrier": "Correos",
    "tracking_number": "ES123456789",
    "status": "In Transit",
    "location": "Madrid Distribution Center",
    "estimated_delivery": "2025-11-20",
    "last_update": "2025-11-18T08:30:00",
    "events": [
      {
        "timestamp": "2025-11-18T10:00:00",
        "location": "Barcelona",
        "description": "Package picked up"
      },
      {
        "timestamp": "2025-11-18T14:30:00",
        "location": "Madrid Distribution Center",
        "description": "In transit"
      }
    ]
  }
}
```

## Supported Carriers

The following carrier codes are supported:
- `CORREOS` - Spanish postal service
- `GLS` - General Logistics Systems
- `SEUR` - Spanish courier service

## Error Responses

### 401 Unauthorized
When the JWT token is missing or invalid:
```json
{
  "detail": "Not authenticated"
}
```

### 400 Bad Request
When using an unsupported carrier:
```json
{
  "detail": "Unsupported carrier: UNSUPPORTED. Supported carriers: CORREOS, GLS, SEUR"
}
```

### 404 Not Found
When requesting a package that doesn't exist:
```json
{
  "detail": "Package not found"
}
```

## Interactive Documentation

For interactive API documentation and testing, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
