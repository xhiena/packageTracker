# Package Tracker

A Universal Package Tracker built with FastAPI, React, and PostgreSQL. Features secure JWT user authentication (including SMTP password recovery) and modular tracking logic using a Strategy Pattern for carriers (Correos, GLS, etc.).

## 🚀 Features

- **Secure JWT Authentication**: User registration, login, and password recovery via SMTP
- **Multi-Carrier Support**: Extensible tracking system using Strategy Pattern
  - Correos (Spanish Postal Service)
  - GLS (General Logistics Systems)
- **RESTful API**: Built with FastAPI with automatic OpenAPI documentation
- **Modern Frontend**: React-based user interface with responsive design
- **Dockerized**: Fully containerized application stack
- **80%+ Test Coverage**: Comprehensive unit tests for backend

## 🏗️ Architecture

### Backend (FastAPI)
- **Security**: JWT tokens, bcrypt password hashing, secure password reset flow
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Modular Design**: Strategy Pattern for carrier-specific tracking logic
- **API Documentation**: Auto-generated at `/docs`

### Frontend (React)
- **Authentication**: Login, registration, password reset
- **Dashboard**: Add, view, and track packages
- **API Integration**: Axios-based API client

### Database (PostgreSQL)
- User management
- Package tracking storage

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Python 3.11
- **Frontend**: React 18, React Router, Axios
- **Authentication**: JWT (python-jose), bcrypt (passlib)
- **Email**: SMTP for password recovery
- **Testing**: pytest, pytest-cov
- **Containerization**: Docker, Docker Compose

## 📦 Getting Started

### Prerequisites

- Docker and Docker Compose
- (Optional) Python 3.11+ for local development
- (Optional) Node.js 18+ for local frontend development

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/xhiena/packageTracker.git
cd packageTracker
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
```

3. Configure SMTP settings in `backend/.env` (optional, for password recovery):
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
```

4. Start the application:
```bash
docker-compose up -d
```

5. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database and run
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## 🧪 Testing

The backend includes comprehensive unit tests with 80%+ coverage:

```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

View coverage report in `backend/htmlcov/index.html`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/password-reset-request` - Request password reset
- `POST /api/auth/password-reset` - Reset password with token

### Packages
- `GET /api/packages/carriers` - Get supported carriers
- `POST /api/packages/` - Add a new package
- `GET /api/packages/` - List all user packages
- `GET /api/packages/{id}` - Get package details
- `PUT /api/packages/{id}` - Update package
- `DELETE /api/packages/{id}` - Delete package
- `GET /api/packages/{id}/track` - Get real-time tracking info

## 🔧 Environment Variables

### Backend Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `SECRET_KEY` | JWT secret key | Change in production! |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `30` |
| `SMTP_HOST` | SMTP server host | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | SMTP username | - |
| `SMTP_PASSWORD` | SMTP password | - |
| `SMTP_FROM` | From email address | - |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` |

## 🎯 Strategy Pattern Implementation

The package tracking system uses the Strategy Pattern for extensibility:

```python
# Base strategy interface
class TrackingStrategy(ABC):
    @abstractmethod
    def track(self, tracking_number: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_tracking_number(self, tracking_number: str) -> bool:
        pass

# Carrier-specific implementations
class CorreosStrategy(TrackingStrategy):
    # Correos-specific tracking logic
    pass

class GLSStrategy(TrackingStrategy):
    # GLS-specific tracking logic
    pass

# Factory to get appropriate strategy
strategy = TrackingStrategyFactory.get_strategy("correos")
tracking_info = strategy.track(tracking_number)
```

## 🔐 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with expiration
- **SMTP Password Recovery**: Secure password reset flow
- **Input Validation**: Pydantic models for request validation
- **CORS Configuration**: Controlled cross-origin access
- **Environment Variables**: Sensitive data stored securely

## 🚦 Development Workflow

1. Make changes to code
2. Run tests: `pytest`
3. Check coverage: `pytest --cov=app`
4. Build and test with Docker: `docker-compose up --build`
5. Commit and push changes

## 📝 Adding a New Carrier

To add support for a new carrier:

1. Create a new strategy class in `backend/app/strategies/`:
```python
class NewCarrierStrategy(TrackingStrategy):
    @property
    def carrier_name(self) -> str:
        return "newcarrier"
    
    def validate_tracking_number(self, tracking_number: str) -> bool:
        # Implement validation logic
        pass
    
    def track(self, tracking_number: str) -> Dict[str, Any]:
        # Implement tracking logic
        pass
```

2. Register it in the factory (`backend/app/strategies/factory.py`):
```python
_strategies = {
    "correos": CorreosStrategy,
    "gls": GLSStrategy,
    "newcarrier": NewCarrierStrategy,  # Add here
}
```

3. Add tests in `backend/app/tests/test_strategies.py`

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Tests pass and coverage remains above 80%
- Code follows existing patterns
- New carriers use the Strategy Pattern

## 📄 License

This project is open source and available under the MIT License.

## 👥 Authors

- xhiena

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React for the frontend library
- PostgreSQL for reliable data storage
