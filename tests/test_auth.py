"""Tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import tempfile

from app.main import app
from app.database import get_db
from app.models.user import Base, User, PasswordResetToken


# Create a temporary database for testing
@pytest.fixture(scope="function")
def test_db():
    """Create a test database."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client."""
    return TestClient(app)


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "testpassword123",
            "full_name": "New User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert data["is_active"] is True
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    """Test registering with duplicate email."""
    # Register first user
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "full_name": "First User"
        }
    )
    
    # Try to register with same email
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password456",
            "full_name": "Second User"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email(client):
    """Test registration with invalid email."""
    response = client.post(
        "/auth/register",
        json={
            "email": "invalid-email",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_register_short_password(client):
    """Test registration with short password."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "short",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_login_success(client):
    """Test successful login."""
    # Register a user first
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "loginpass123",
            "full_name": "Login User"
        }
    )
    
    # Login
    response = client.post(
        "/auth/token",
        data={
            "username": "login@example.com",
            "password": "loginpass123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Test login with wrong password."""
    # Register a user first
    client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "correctpass123",
            "full_name": "Test User"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/auth/token",
        data={
            "username": "wrongpass@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/auth/token",
        data={
            "username": "nonexistent@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401


def test_get_current_user(client):
    """Test getting current user information."""
    # Register and login
    client.post(
        "/auth/register",
        json={
            "email": "current@example.com",
            "password": "password123",
            "full_name": "Current User"
        }
    )
    
    login_response = client.post(
        "/auth/token",
        data={
            "username": "current@example.com",
            "password": "password123"
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current@example.com"
    assert data["full_name"] == "Current User"


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401


def test_get_current_user_no_token(client):
    """Test getting current user without token."""
    response = client.get("/auth/me")
    
    assert response.status_code == 401


def test_forgot_password(client, test_db):
    """Test forgot password endpoint."""
    # Register a user first
    client.post(
        "/auth/register",
        json={
            "email": "forgot@example.com",
            "password": "oldpassword123",
            "full_name": "Forgot User"
        }
    )
    
    # Request password reset
    response = client.post(
        "/auth/forgot-password",
        json={"email": "forgot@example.com"}
    )
    
    assert response.status_code == 200
    assert "email exists" in response.json()["message"].lower()
    
    # Check that a token was created
    db = test_db()
    try:
        token = db.query(PasswordResetToken).filter(
            PasswordResetToken.is_used == False
        ).first()
        assert token is not None
    finally:
        db.close()


def test_forgot_password_nonexistent_email(client):
    """Test forgot password with non-existent email."""
    response = client.post(
        "/auth/forgot-password",
        json={"email": "nonexistent@example.com"}
    )
    
    # Should still return success to prevent email enumeration
    assert response.status_code == 200
    assert "email exists" in response.json()["message"].lower()


def test_reset_password_success(client, test_db):
    """Test successful password reset."""
    # Register a user
    client.post(
        "/auth/register",
        json={
            "email": "reset@example.com",
            "password": "oldpassword123",
            "full_name": "Reset User"
        }
    )
    
    # Request password reset
    client.post(
        "/auth/forgot-password",
        json={"email": "reset@example.com"}
    )
    
    # Get the token from database
    db = test_db()
    try:
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.is_used == False
        ).first()
        reset_token = token_record.token
    finally:
        db.close()
    
    # Reset password
    response = client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "newpassword123"
        }
    )
    
    assert response.status_code == 200
    assert "reset successfully" in response.json()["message"].lower()
    
    # Test login with new password
    login_response = client.post(
        "/auth/token",
        data={
            "username": "reset@example.com",
            "password": "newpassword123"
        }
    )
    assert login_response.status_code == 200


def test_reset_password_invalid_token(client):
    """Test password reset with invalid token."""
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid_token_12345",
            "new_password": "newpassword123"
        }
    )
    
    assert response.status_code == 400
    assert "invalid" in response.json()["detail"].lower()


def test_reset_password_used_token(client, test_db):
    """Test password reset with already used token."""
    # Register a user
    client.post(
        "/auth/register",
        json={
            "email": "usedtoken@example.com",
            "password": "oldpassword123",
            "full_name": "Used Token User"
        }
    )
    
    # Request password reset
    client.post(
        "/auth/forgot-password",
        json={"email": "usedtoken@example.com"}
    )
    
    # Get the token from database
    db = test_db()
    try:
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.is_used == False
        ).first()
        reset_token = token_record.token
    finally:
        db.close()
    
    # Use the token once
    client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "newpassword123"
        }
    )
    
    # Try to use the same token again
    response = client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "anotherpassword123"
        }
    )
    
    assert response.status_code == 400
    assert "already used" in response.json()["detail"].lower()
