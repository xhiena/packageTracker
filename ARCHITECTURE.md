# Package Tracker Architecture

## Overview

This document describes the architecture and design patterns used in the Universal Package Tracker application.

## System Architecture

```
┌─────────────────┐
│   React Frontend│
│   (Port 3000)   │
└────────┬────────┘
         │
         │ HTTP/REST
         │
┌────────▼────────┐
│  FastAPI Backend│
│   (Port 8000)   │
└────────┬────────┘
         │
         │ SQLAlchemy ORM
         │
┌────────▼────────┐
│   PostgreSQL    │
│   (Port 5432)   │
└─────────────────┘
```

## Backend Architecture

### Layer Structure

```
backend/
├── app/
│   ├── api/           # API endpoints and routing
│   ├── core/          # Core configuration and security
│   ├── data/          # Static data (supported carriers)
│   ├── db/            # Database connection and session management
│   ├── models/        # SQLAlchemy database models
│   ├── services/      # Business logic services
│   ├── strategies/    # KeyDelivery API integration
│   └── tests/         # Unit and integration tests
```

### Design Patterns

#### 1. KeyDelivery API Integration

The application uses KeyDelivery API for universal carrier tracking:

```python
# KeyDelivery Service Module
keydelivery
├── detect_carrier(tracking_number) -> List[Dict]
├── validate_tracking_number(tracking_number) -> bool
└── track(tracking_number, carrier_code) -> Dict

# Supported Carriers
CARRIERS = [
    ("dhl", "DHL"),
    ("ups", "UPS"),
    ("fedex", "FedEx"),
    ("correos", "Correos"),
    ("gls", "GLS"),
    # ... 20+ carriers total
]
```

**Benefits:**
- Single API for all carriers - no need to implement tracking logic per carrier
- Automatic carrier detection
- Consistent response format across all carriers
- Easy to add new carriers - just update the CARRIERS list

#### 2. Repository Pattern (Implicit)

SQLAlchemy ORM acts as a repository layer, abstracting database operations:

```python
# Database models act as entities
User, Package

# Session management through dependency injection
def get_db() -> Session:
    ...
```

#### 3. Dependency Injection

FastAPI's built-in dependency injection is used throughout:

```python
# Database session injection
def endpoint(db: Session = Depends(get_db)):
    ...

# Authentication injection
def endpoint(current_user: User = Depends(get_current_active_user)):
    ...
```

### Security Architecture

#### Authentication Flow

```
1. User Registration
   POST /api/auth/register
   ├── Validate input
   ├── Hash password (bcrypt)
   ├── Store in database
   └── Return user data

2. User Login
   POST /api/auth/login
   ├── Validate credentials
   ├── Verify password hash
   ├── Generate JWT token
   └── Return token

3. Protected Endpoints
   GET /api/packages/
   ├── Extract JWT from Authorization header
   ├── Validate and decode token
   ├── Load user from database
   └── Process request
```

#### Password Recovery Flow

```
1. Request Reset
   POST /api/auth/password-reset-request
   ├── Find user by email
   ├── Generate reset token (JWT with 30min expiry)
   ├── Send email with reset link
   └── Return generic success message

2. Reset Password
   POST /api/auth/password-reset
   ├── Validate reset token
   ├── Verify token type and expiration
   ├── Hash new password
   ├── Update user password
   └── Return success
```

### API Design

RESTful API following standard conventions:

```
Authentication:
POST   /api/auth/register              - Register new user
POST   /api/auth/login                 - Login and get token
POST   /api/auth/password-reset-request - Request password reset
POST   /api/auth/password-reset        - Reset password with token

Packages:
GET    /api/packages/carriers          - List supported carriers
POST   /api/packages/                  - Create package
GET    /api/packages/                  - List user's packages
GET    /api/packages/{id}              - Get package details
PUT    /api/packages/{id}              - Update package
DELETE /api/packages/{id}              - Delete package
GET    /api/packages/{id}/track        - Get tracking info
```

## Frontend Architecture

### Component Structure

```
frontend/src/
├── components/        # Reusable UI components
├── pages/            # Page components
│   ├── Login.js      - Login page
│   ├── Register.js   - Registration page
│   ├── PasswordReset.js - Password recovery
│   └── Dashboard.js  - Main application dashboard
├── services/         # API communication
│   └── api.js        - Axios-based API client
├── App.js            # Main application component
└── index.js          # Application entry point
```

### State Management

- Local component state using React hooks (useState, useEffect)
- Token storage in localStorage
- No external state management library (keeping it simple)

### Routing

React Router v6 for client-side routing:

```
/                      -> Redirect to /dashboard
/login                 -> Login page
/register              -> Registration page
/reset-password        -> Password reset (request or actual reset based on token)
/dashboard             -> Protected main dashboard
```

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### Packages Table

```sql
CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    tracking_number VARCHAR NOT NULL,
    carrier VARCHAR NOT NULL,
    user_id INTEGER REFERENCES users(id),
    description VARCHAR,
    status VARCHAR,
    last_location VARCHAR,
    tracking_data TEXT,  -- JSON string
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

## Testing Strategy

### Test Coverage Requirements

- **Minimum: 80%** ✅ Currently: 94%
- Focus on critical paths: authentication, tracking strategies, API endpoints

### Test Structure

```
backend/app/tests/
├── test_auth.py                   # Authentication endpoint tests
├── test_packages.py               # Package management endpoint tests
├── test_security.py               # Security utilities tests
├── test_strategies.py             # KeyDelivery service tests
└── test_keydelivery_manual.py    # Manual KeyDelivery integration tests
```

### Test Database

- SQLite in-memory database for tests
- Fresh database for each test function
- No external dependencies required

## Deployment Architecture

### Docker Compose Setup

```yaml
services:
  db:         # PostgreSQL database
  backend:    # FastAPI application
  frontend:   # React application
```

### Environment Configuration

- Secrets managed via environment variables
- `.env` file for local development
- Environment-specific configurations

## Extensibility

### Adding a New Carrier

1. Add carrier to `backend/app/data/carriers.py`:
   ```python
   CARRIERS = [
       # ... existing carriers
       ("new_carrier", "New Carrier Name"),
   ]
   ```
2. Carrier is automatically available through KeyDelivery API
3. No code changes needed - KeyDelivery handles all tracking logic

### Adding New Features

1. **New API Endpoint:**
   - Add route in appropriate router (auth.py or packages.py)
   - Add schema in schemas.py
   - Add tests

2. **New Service:**
   - Create in services/ directory
   - Use dependency injection
   - Add tests

## Security Considerations

- **Password Storage:** bcrypt hashing (cost factor 12)
- **JWT Tokens:** HS256 algorithm, 30-minute expiration
- **CORS:** Configured to allow only specific origins
- **Input Validation:** Pydantic models for all inputs
- **SQL Injection:** Protected by SQLAlchemy ORM
- **Password Reset:** Time-limited tokens, email verification

## Performance Considerations

- Database indexing on frequently queried fields (email, username, tracking_number)
- Connection pooling via SQLAlchemy
- Async-capable with FastAPI (ready for scaling)
- Stateless authentication (JWT) for horizontal scaling

## Monitoring and Logging

- FastAPI automatic OpenAPI documentation at `/docs`
- Health check endpoint at `/health`
- Console logging for development
- Ready for production logging integration

## Future Enhancements

1. **Caching:** Redis for tracking data cache
2. **Background Jobs:** Celery for periodic tracking updates
3. **Real-time Updates:** WebSocket support for live tracking
4. **API Rate Limiting:** Protect against abuse
5. **Admin Panel:** User and package management
6. **Analytics:** Tracking statistics dashboard
7. **Notifications:** Email/SMS notifications for package updates
