# Project: Universal Package Tracker (FastAPI + React)

Goal: Create a secure, modular, and containerized package tracking application using Python (FastAPI) and a decoupled React frontend with PostgreSQL persistence.

## Phase 1: Environment & Database Setup
1. Setup (docker-compose.yml): Create a docker-compose.yml file defining three services: db (PostgreSQL), backend (FastAPI), and frontend (React/Node).
  * db: Use postgres:latest image.
  * backend: Build from Dockerfile.backend.
  * frontend: Build from Dockerfile.frontend.
2. Backend Dockerfile (`Dockerfile.backend`): Set up a Python environment (e.g., `python:3.11-slim`), install dependencies (`requirements.txt`), and expose port 8000.
3. Database and SMTP Configuration (`.env`): Create a basic `.env` file for database secrets (e.g., `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) and SMTP configuration for password recovery (e.g., `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`, `FRONTEND_URL` for the reset link).
4. Dependencies (`requirements.txt`): Include `fastapi`, `uvicorn`, `SQLAlchemy`, `psycopg2-binary`, `python-jose[cryptography]` (for JWT), `passlib[bcrypt]`, `httpx`, and `python-dotenv` (for loading environment variables), `pytest` with `pytest-cov`.

## Phase 2: Core Backend (FastAPI & Database Models)
1. FastAPI App Structure: Create a main file (`main.py`) and directories for `app/auth`, `app/db`, `app/models`, `app/tracking`, and `app/utils`.
2. Database Connection: In `app/db/database.py`, set up the connection engine and a Base for declarative models using SQLAlchemy.
3. User Model (`app/models/user.py`): Define a `User` model with fields for `id`, `email` (unique), `hashed_password`, and `full_name`.
4. Tracking Model (`app/models/package.py`): Define a `Package` model with fields for:
  * `id`
  * `user_id` (Foreign Key to User)
  * `tracking_number` (string)
  * `carrier_code` (string, e.g., 'GLS', 'SEUR')
  * `nickname` (string, user-defined name)
  * `status_data` (PostgreSQL JSONB type to store the complex/varying JSON response from the carrier API).
    
## Phase 3: Authentication & Authorization
1. Security Utilities (`app/auth/security.py`): Implement functions for password hashing/verification, JWT token creation/decoding, and a dependency (`get_current_user`) to protect API routes.
2. Auth Router (`app/auth/router.py`):
  * Implement Registration endpoint (POST `/register`).
  * Implement Login endpoint (POST `/token`) that returns a JWT access token.
  * Implement a Password Recovery endpoint (POST `/forgot-password`). This endpoint must generate a unique, time-limited token and use the new Email Utility to send the recovery email.
  * Implement a Password Reset endpoint (POST `/reset-password`).
  * Include Pydantic schemas for request/response bodies (e.g., `UserCreate`, `Token`, `ForgotPasswordRequest`, `PasswordResetRequest`).
3. Email Utility (`app/utils/email.py`): Implement a utility function `send_recovery_email(email: str, token: str)` that uses the SMTP configuration from the environment variables to send an email containing a password reset link (e.g., `FRONTEND_URL/reset-password?token={token}`). Use the Python standard library's `smtplib` for email sending.

## Phase 4: Modular Tracking Service (Strategy Pattern)
1. Tracking Interface (`app/tracking/interface.py`): Define a Python `abstract base class` (ABC) named `CarrierTracker` with a single abstract method: `get_status(tracking_number: str) -> dict`.
2. Carrier Implementations (`app/tracking/carriers/`): Create separate Python files for the requested carriers: `correos.py`, `gls.py`, `seur.py`, etc.
  * Each file must implement the `CarrierTracker` interface.
  * Crucial: These methods must be MOCKED. They should return a sample dictionary structure (representing the tracking status) based on the input tracking number, simulating a successful API call.
3. Service Layer (`app/tracking/service.py`): Implement a central factory or mapping that selects the correct `CarrierTracker` implementation based on the `carrier_code`.

## Phase 5: Package API Endpoints
1. Package Router (`app/package/router.py`):
  * POST `/packages`: Add a new package. Requires authentication. Accepts `tracking_number` and `carrier_code`. Calls the Tracking Service. Saves package details (and initial status) to the DB.
  * GET `/packages`: List all packages for the authenticated user.
  * GET `/packages/{package_id}/status`: Fetch the latest status. Calls the Tracking Service to check the external API and updates the `status_data` in the DB.

## Phase 6: Unit Tests (Minimum 80% Coverage)
1. Test Setup (`tests/conftest.py`): Set up fixtures for a test database connection (e.g., SQLite in memory for speed) and an authenticated test client.
2. Tests (`tests/`): Create test files for:
  * `test_auth.py`: Test user registration, login, protected routes, and the email utility (mocking the SMTP library to check function call arguments).
  * `test_carriers.py`: Test that the mock carrier services return expected data structures.
  * `test_package_api.py`: Test adding a package and retrieving its status (ensuring correct DB interaction).

## Phase 7: Frontend Interface (React)
1. Setup: Create a simple React application structure using Vite or Create-React-App within the `frontend/` directory. Use Tailwind CSS.
2. App Component (`App.jsx`): Implement basic state management (e.g., using React hooks).
3. Pages/Views:
  * Auth View: A single view for Registration/Login, Forgot Password, and Reset Password (using form inputs and connecting to the FastAPI endpoints).
  * Dashboard View: A view to display the list of tracked packages (showing nickname, tracking number, and latest status summary).
  * Add Package Modal/Form: A modal/form to input a new tracking number and select a carrier from a dropdown (using the supported carriers).
4. API Interaction: Use `fetch` or `axios` to interact with the FastAPI backend on port 8000. Ensure the JWT token is sent in the `Authorization` header for protected routes.
