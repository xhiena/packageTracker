# Authentication & Authorization System

This document describes the authentication and authorization system implemented for the Package Tracker application.

## Overview

The authentication system provides secure user registration, login, password recovery, and password reset functionality using JWT tokens.

## Features

- **User Registration**: Create new user accounts with email and password
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt-based password hashing for security
- **Password Recovery**: Email-based password reset with time-limited tokens
- **Protected Routes**: Dependency injection for route protection

## API Endpoints

### Registration
```
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password123",
    "full_name": "John Doe"
}
```

**Response:** 201 Created
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true
}
```

### Login
```
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure_password123
```

**Response:** 200 OK
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Get Current User
```
GET /auth/me
Authorization: Bearer <access_token>
```

**Response:** 200 OK
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true
}
```

### Forgot Password
```
POST /auth/forgot-password
Content-Type: application/json

{
    "email": "user@example.com"
}
```

**Response:** 200 OK
```json
{
    "message": "If the email exists, a password reset link has been sent"
}
```

### Reset Password
```
POST /auth/reset-password
Content-Type: application/json

{
    "token": "reset_token_here",
    "new_password": "new_secure_password123"
}
```

**Response:** 200 OK
```json
{
    "message": "Password has been reset successfully"
}
```

## Project Structure

```
app/
├── auth/
│   ├── __init__.py
│   ├── router.py           # Authentication endpoints
│   ├── schemas.py          # Pydantic schemas
│   └── security.py         # Security utilities
├── models/
│   ├── __init__.py
│   └── user.py            # Database models
├── utils/
│   ├── __init__.py
│   └── email.py           # Email utility
├── config.py              # Configuration settings
├── database.py            # Database configuration
└── main.py                # FastAPI application

tests/
├── __init__.py
├── test_auth.py           # Authentication endpoint tests
└── test_security.py       # Security utility tests
```

## Security Features

### Password Hashing
- Uses bcrypt algorithm via passlib
- Automatic salt generation
- Configurable work factor

### JWT Tokens
- HS256 algorithm
- Configurable expiration (default: 30 minutes)
- Includes user email in payload

### Password Reset Tokens
- Cryptographically secure random tokens (URL-safe)
- Time-limited (default: 24 hours)
- Single-use tokens (marked as used after consumption)
- Automatic invalidation of previous tokens

## Configuration

Environment variables can be set in `.env` file:

```env
# JWT Settings
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Password Reset
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=24

# Email Settings (optional for development)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@packagetracker.com
SMTP_FROM_NAME=Package Tracker

# Database
DATABASE_URL=sqlite:///./packagetracker.db
```

## Running the Application

### Installation
```bash
pip install -r requirements.txt
```

### Start the Server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Usage Example

### Python Example
```python
import requests

# Register a new user
response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "email": "user@example.com",
        "password": "secure_password123",
        "full_name": "John Doe"
    }
)
print(response.json())

# Login
response = requests.post(
    "http://localhost:8000/auth/token",
    data={
        "username": "user@example.com",
        "password": "secure_password123"
    }
)
token = response.json()["access_token"]

# Access protected route
response = requests.get(
    "http://localhost:8000/auth/me",
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
```

### cURL Example
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure_password123", "full_name": "John Doe"}'

# Login
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secure_password123"

# Get current user (replace TOKEN with actual token)
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer TOKEN"
```

## Protecting Routes

Use the `get_current_user` dependency to protect routes:

```python
from fastapi import APIRouter, Depends
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}"}
```

## Database Models

### User Model
- `id`: Primary key
- `email`: Unique email address
- `full_name`: Optional full name
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account active status
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### PasswordResetToken Model
- `id`: Primary key
- `user_id`: Foreign key to User
- `token`: Unique reset token
- `created_at`: Token creation timestamp
- `expires_at`: Token expiration timestamp
- `is_used`: Token usage status

## Security Considerations

1. **Never expose the SECRET_KEY** - Store it securely and rotate it regularly
2. **Use HTTPS in production** - JWT tokens should never be transmitted over HTTP
3. **Email enumeration protection** - Password reset always returns success message
4. **Token expiration** - Both JWT and password reset tokens have expiration times
5. **Password requirements** - Minimum 8 characters (can be extended with validators)
6. **Single-use reset tokens** - Reset tokens are invalidated after use
7. **Database security** - Use environment variables for database credentials in production

## Future Enhancements

- Email verification on registration
- Two-factor authentication (2FA)
- OAuth2 integration (Google, GitHub, etc.)
- Rate limiting for authentication endpoints
- Account lockout after failed login attempts
- Password strength requirements
- Refresh tokens for longer sessions
