from fastapi import FastAPI
from app.package.router import router as package_router

app = FastAPI(
    title="Package Tracker API",
    description="Universal Package Tracker with support for multiple carriers",
    version="1.0.0"
)

# Include routers
app.include_router(package_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Package Tracker API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
