"""Main FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup: Create database tables
    from app.db.database import engine
    from app.models import user, package
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (if needed in future)


# Initialize FastAPI app
app = FastAPI(
    title="Package Tracker API",
    description="API for tracking shipping packages from various carriers",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Package Tracker API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
