import pytest
from unittest.mock import patch, MagicMock
from app.models.user import User


class TestUserRegistration:
    """Test user registration endpoint."""
    
    def test_register_new_user(self, client, db_session):
        """Test successful user registration."""
        response = client.post(
            "/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "full_name": "New User"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data
        
        # Verify user exists in database
        user = db_session.query(User).filter(User.email == "newuser@example.com").first()
        assert user is not None
        assert user.full_name == "New User"
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email fails."""
        response = client.post(
            "/auth/register",
            json={
                "email": "testuser@example.com",  # Already exists
                "password": "password123",
                "full_name": "Another User"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email fails."""
        response = client.post(
            "/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
                "full_name": "Test User"
            }
        )
        
        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Test user login endpoint."""
    
    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            "/auth/token",
            data={
                "username": "testuser@example.com",
                "password": "testpassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password fails."""
        response = client.post(
            "/auth/token",
            data={
                "username": "testuser@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user fails."""
        response = client.post(
            "/auth/token",
            data={
                "username": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401


class TestProtectedRoutes:
    """Test protected routes requiring authentication."""
    
    def test_access_protected_route_with_token(self, authenticated_client):
        """Test accessing protected route with valid token."""
        response = authenticated_client.get("/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "testuser@example.com"
        assert data["full_name"] == "Test User"
    
    def test_access_protected_route_without_token(self, client):
        """Test accessing protected route without token fails."""
        response = client.get("/auth/me")
        
        assert response.status_code == 401
    
    def test_access_protected_route_with_invalid_token(self, client):
        """Test accessing protected route with invalid token fails."""
        client.headers = {
            **client.headers,
            "Authorization": "Bearer invalid_token_here"
        }
        response = client.get("/auth/me")
        
        assert response.status_code == 401


class TestPasswordRecovery:
    """Test password recovery functionality."""
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_forgot_password_sends_email(self, mock_smtp, client, test_user):
        """Test that forgot password endpoint sends recovery email."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        response = client.post(
            "/auth/forgot-password",
            json={"email": "testuser@example.com"}
        )
        
        assert response.status_code == 200
        assert "sent" in response.json()["message"].lower()
        
        # Verify SMTP was called
        assert mock_smtp.called
        assert mock_server.starttls.called
        assert mock_server.login.called
        assert mock_server.sendmail.called
        
        # Check sendmail arguments
        call_args = mock_server.sendmail.call_args
        assert call_args is not None
        assert "testuser@example.com" in call_args[0]  # Recipient email
    
    def test_forgot_password_nonexistent_email(self, client):
        """Test forgot password with nonexistent email doesn't reveal it."""
        response = client.post(
            "/auth/forgot-password",
            json={"email": "nonexistent@example.com"}
        )
        
        # Should still return 200 to not reveal if email exists
        assert response.status_code == 200
        assert "sent" in response.json()["message"].lower()
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_reset_password_with_valid_token(self, mock_smtp, client, test_user, db_session):
        """Test password reset with valid token."""
        # First, trigger forgot password to generate token
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        forgot_response = client.post(
            "/auth/forgot-password",
            json={"email": "testuser@example.com"}
        )
        assert forgot_response.status_code == 200
        
        # Get the token from the reset_tokens (we need to access it from router)
        from app.auth.router import reset_tokens
        token = list(reset_tokens.keys())[0] if reset_tokens else None
        assert token is not None
        
        # Now reset the password
        response = client.post(
            "/auth/reset-password",
            json={
                "token": token,
                "new_password": "newpassword123"
            }
        )
        
        assert response.status_code == 200
        assert "reset" in response.json()["message"].lower()
        
        # Verify we can login with new password
        login_response = client.post(
            "/auth/token",
            data={
                "username": "testuser@example.com",
                "password": "newpassword123"
            }
        )
        assert login_response.status_code == 200
    
    def test_reset_password_with_invalid_token(self, client):
        """Test password reset with invalid token fails."""
        response = client.post(
            "/auth/reset-password",
            json={
                "token": "invalid_token",
                "new_password": "newpassword123"
            }
        )
        
        assert response.status_code == 400
        assert "invalid" in response.json()["detail"].lower()


class TestEmailUtility:
    """Test email utility functions."""
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_smtp_call(self, mock_smtp):
        """Test that send_recovery_email calls SMTP correctly."""
        from app.utils.email import send_recovery_email
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Call the function
        send_recovery_email("test@example.com", "test_token_123")
        
        # Verify SMTP connection was made
        assert mock_smtp.called
        
        # Verify starttls was called
        assert mock_server.starttls.called
        
        # Verify login was called
        assert mock_server.login.called
        
        # Verify sendmail was called with correct arguments
        assert mock_server.sendmail.called
        call_args = mock_server.sendmail.call_args[0]
        
        # Check recipient
        recipient = call_args[1]
        assert recipient == "test@example.com"
        
        # Check message contains token
        message = call_args[2]
        assert "test_token_123" in message
        assert "reset-password" in message.lower()
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_with_env_vars(self, mock_smtp, monkeypatch):
        """Test that send_recovery_email uses environment variables."""
        from app.utils.email import send_recovery_email
        
        # Set environment variables
        monkeypatch.setenv("SMTP_SERVER", "smtp.test.com")
        monkeypatch.setenv("SMTP_PORT", "465")
        monkeypatch.setenv("SMTP_USER", "testuser")
        monkeypatch.setenv("SMTP_PASSWORD", "testpass")
        monkeypatch.setenv("FRONTEND_URL", "https://frontend.test.com")
        
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Call the function
        send_recovery_email("test@example.com", "token123")
        
        # Verify SMTP was called with correct server and port
        mock_smtp.assert_called_with("smtp.test.com", 465)
        
        # Verify login was called with correct credentials
        mock_server.login.assert_called_with("testuser", "testpass")
        
        # Verify message contains correct frontend URL
        message = mock_server.sendmail.call_args[0][2]
        assert "https://frontend.test.com/reset-password?token=token123" in message
