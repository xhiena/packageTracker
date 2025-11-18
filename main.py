"""Main FastAPI application entry point."""
from fastapi import FastAPI
from app.db.database import Base
from app.models import user, package

# Initialize FastAPI app
app = FastAPI(
    title="Package Tracker API",
    description="API for tracking shipping packages from various carriers",
    version="0.1.0"
)


@app.on_event("startup")
async def startup_event():
    """Create database tables on application startup."""
    from app.db.database import engine
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Package Tracker API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
