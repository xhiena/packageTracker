import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from app.models.user import User
from app.models.package import Package
from app.auth.security import get_password_hash, create_access_token
from main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def test_user(test_db):
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}

def test_create_package(client, auth_headers):
    """Test creating a new package"""
    response = client.post(
        "/packages",
        json={
            "tracking_number": "TEST123456",
            "carrier_code": "CORREOS",
            "nickname": "My Package"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["tracking_number"] == "TEST123456"
    assert data["carrier_code"] == "CORREOS"
    assert data["nickname"] == "My Package"
    assert data["status_data"] is not None
    assert data["status_data"]["carrier"] == "Correos"

def test_create_package_without_auth(client):
    """Test that creating a package requires authentication"""
    response = client.post(
        "/packages",
        json={
            "tracking_number": "TEST123456",
            "carrier_code": "CORREOS"
        }
    )
    assert response.status_code == 401

def test_create_package_unsupported_carrier(client, auth_headers):
    """Test creating a package with an unsupported carrier"""
    response = client.post(
        "/packages",
        json={
            "tracking_number": "TEST123456",
            "carrier_code": "UNSUPPORTED"
        },
        headers=auth_headers
    )
    assert response.status_code == 400

def test_list_packages(client, auth_headers, test_user):
    """Test listing all packages for a user"""
    # Create a package first
    client.post(
        "/packages",
        json={
            "tracking_number": "TEST123456",
            "carrier_code": "GLS"
        },
        headers=auth_headers
    )
    
    # List packages
    response = client.get("/packages", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["tracking_number"] == "TEST123456"

def test_list_packages_without_auth(client):
    """Test that listing packages requires authentication"""
    response = client.get("/packages")
    assert response.status_code == 401

def test_get_package_status(client, auth_headers):
    """Test getting package status"""
    # Create a package first
    create_response = client.post(
        "/packages",
        json={
            "tracking_number": "TEST789",
            "carrier_code": "SEUR"
        },
        headers=auth_headers
    )
    package_id = create_response.json()["id"]
    
    # Get status
    response = client.get(f"/packages/{package_id}/status", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "package" in data
    assert "current_status" in data
    assert data["current_status"]["carrier"] == "SEUR"
    assert data["current_status"]["tracking_number"] == "TEST789"

def test_get_package_status_not_found(client, auth_headers):
    """Test getting status for a non-existent package"""
    response = client.get("/packages/99999/status", headers=auth_headers)
    assert response.status_code == 404

def test_get_package_status_without_auth(client):
    """Test that getting package status requires authentication"""
    response = client.get("/packages/1/status")
    assert response.status_code == 401
