# packageTracker
A simple shipping package tracker built with FastAPI and PostgreSQL.

## Features

- Track packages from multiple carriers (GLS, SEUR, etc.)
- User authentication and management
- Store tracking data with flexible JSONB format for carrier-specific responses

## Phase 2: Core Backend Implementation ✓

### Project Structure

```
packageTracker/
├── app/
│   ├── auth/         # Authentication modules (to be implemented)
│   ├── db/           # Database connection and setup
│   │   └── database.py
│   ├── models/       # SQLAlchemy models
│   │   ├── user.py
│   │   └── package.py
│   ├── tracking/     # Package tracking logic (to be implemented)
│   └── utils/        # Utility functions (to be implemented)
├── main.py           # FastAPI application entry point
├── requirements.txt  # Python dependencies
└── .env.example      # Example environment configuration
```

### Database Models

#### User Model
- `id`: Integer (Primary Key)
- `email`: String (Unique, Not Null)
- `hashed_password`: String (Not Null)
- `full_name`: String (Nullable)

#### Package Model
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key to User)
- `tracking_number`: String (Not Null)
- `carrier_code`: String (Not Null) - e.g., 'GLS', 'SEUR'
- `nickname`: String (Nullable) - User-defined package name
- `status_data`: JSONB (Nullable) - Stores complex JSON responses from carrier APIs

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database:**
   ```bash
   cp .env.example .env
   # Edit .env and set your PostgreSQL connection string
   ```

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database with JSONB support
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server
