from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.auth.router import router as auth_router
from app.package.router import router as package_router
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed


app = FastAPI(title="Package Tracker API", version="1.0.0", lifespan=lifespan)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(package_router, prefix="/api", tags=["packages"])


@app.get("/")
def root():
    return {"message": "Welcome to Package Tracker API"}
