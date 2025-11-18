import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert data["is_active"] is True


def test_register_duplicate_user(client, test_user):
    """Test registration with existing username."""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "another@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"]


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/api/auth/login",
        data={"username": "nonexistent", "password": "password123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_password_reset_request(client, test_user):
    """Test password reset request."""
    response = client.post(
        "/api/auth/password-reset-request",
        json={"email": "test@example.com"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()


def test_password_reset_request_nonexistent_email(client):
    """Test password reset request with non-existent email."""
    response = client.post(
        "/api/auth/password-reset-request",
        json={"email": "nonexistent@example.com"}
    )
    # Should still return 200 to not reveal if email exists
    assert response.status_code == status.HTTP_200_OK
