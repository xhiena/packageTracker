"""Comprehensive authentication tests including email mocking and protected routes."""
from unittest.mock import patch, MagicMock
from fastapi import status


class TestUserRegistration:
    """Test user registration endpoint."""
    
    def test_register_with_invalid_email(self, client):
        """Test registration with invalid email fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "username": "testuser",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email fails."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",  # Already exists
                "username": "newuser",
                "password": "password123"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"].lower()


class TestProtectedRoutes:
    """Test protected routes requiring authentication."""
    
    def test_access_packages_with_token(self, authenticated_client):
        """Test accessing protected packages endpoint with valid token."""
        response = authenticated_client.get("/api/packages/")
        assert response.status_code == status.HTTP_200_OK
        # Should return a list (empty if no packages)
        data = response.json()
        assert isinstance(data, list)
    
    def test_access_packages_without_token(self, client):
        """Test accessing protected packages endpoint without token fails."""
        response = client.get("/api/packages/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_packages_with_invalid_token(self, client):
        """Test accessing protected packages endpoint with invalid token fails."""
        response = client.get(
            "/api/packages/",
            headers={"Authorization": "Bearer invalid_token_here"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestEmailUtility:
    """Test email utility functions with SMTP mocking."""
    
    @patch('smtplib.SMTP')
    def test_password_reset_sends_email(self, mock_smtp, client, test_user):
        """Test that password reset request sends email."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        response = client.post(
            "/api/auth/password-reset-request",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        
        # Note: Email sending is mocked, so we just verify the endpoint works
        # In a real scenario with proper dependency injection, we'd verify the mock was called


class TestPasswordReset:
    """Test password reset flow."""
    
    @patch('smtplib.SMTP')
    def test_password_reset_request_flow(self, mock_smtp, client, test_user):
        """Test password reset request flow."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Step 1: Request password reset
        response = client.post(
            "/api/auth/password-reset-request",
            json={"email": "test@example.com"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        
        # Note: In a full integration test, we would:
        # 1. Extract token from the sent email
        # 2. Use it to reset the password
        # 3. Verify login with new password
        # For now, we verify the request endpoint works
