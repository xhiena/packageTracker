"""Tests for email utility functions."""

import os
import unittest
from unittest.mock import MagicMock, patch, call
import smtplib

from app.utils.email import send_recovery_email


class TestSendRecoveryEmail(unittest.TestCase):
    """Test cases for the send_recovery_email function."""
    
    def setUp(self):
        """Set up test environment variables."""
        self.env_vars = {
            'SMTP_HOST': 'smtp.example.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': 'test@example.com',
            'SMTP_PASSWORD': 'test_password',
            'SMTP_FROM_EMAIL': 'noreply@example.com',
            'FRONTEND_URL': 'https://example.com'
        }
        # Store original environment
        self.original_env = os.environ.copy()
        
    def tearDown(self):
        """Restore original environment."""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def _set_env_vars(self, **overrides):
        """Helper to set environment variables with optional overrides."""
        env = self.env_vars.copy()
        env.update(overrides)
        for key, value in env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_success(self, mock_smtp_class):
        """Test successful email sending."""
        self._set_env_vars()
        
        # Create mock SMTP instance
        mock_smtp = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        # Call the function
        email = 'user@example.com'
        token = 'test_token_123'
        send_recovery_email(email, token)
        
        # Verify SMTP connection was made with correct parameters
        mock_smtp_class.assert_called_once_with('smtp.example.com', 587)
        
        # Verify TLS was enabled
        mock_smtp.starttls.assert_called_once()
        
        # Verify login was called
        mock_smtp.login.assert_called_once_with('test@example.com', 'test_password')
        
        # Verify sendmail was called
        self.assertEqual(mock_smtp.sendmail.call_count, 1)
        call_args = mock_smtp.sendmail.call_args[0]
        self.assertEqual(call_args[0], 'noreply@example.com')  # from
        self.assertEqual(call_args[1], 'user@example.com')  # to
        
        # Verify the email content contains the reset link
        email_content = call_args[2]
        self.assertIn('https://example.com/reset-password?token=test_token_123', email_content)
        self.assertIn('Password Reset Request', email_content)
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_with_special_characters_in_token(self, mock_smtp_class):
        """Test email sending with special characters in token."""
        self._set_env_vars()
        
        mock_smtp = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        # Token with special characters
        email = 'user@example.com'
        token = 'abc123_XYZ-456.789'
        send_recovery_email(email, token)
        
        # Verify sendmail was called
        call_args = mock_smtp.sendmail.call_args[0]
        email_content = call_args[2]
        self.assertIn(f'https://example.com/reset-password?token={token}', email_content)
    
    def test_send_recovery_email_missing_smtp_host(self):
        """Test error when SMTP_HOST is missing."""
        self._set_env_vars(SMTP_HOST=None)
        
        with self.assertRaises(ValueError) as context:
            send_recovery_email('user@example.com', 'token123')
        
        self.assertIn('SMTP_HOST', str(context.exception))
    
    def test_send_recovery_email_missing_smtp_port(self):
        """Test error when SMTP_PORT is missing."""
        self._set_env_vars(SMTP_PORT=None)
        
        with self.assertRaises(ValueError) as context:
            send_recovery_email('user@example.com', 'token123')
        
        self.assertIn('SMTP_PORT', str(context.exception))
    
    def test_send_recovery_email_missing_smtp_username(self):
        """Test error when SMTP_USERNAME is missing."""
        self._set_env_vars(SMTP_USERNAME=None)
        
        with self.assertRaises(ValueError) as context:
            send_recovery_email('user@example.com', 'token123')
        
        self.assertIn('SMTP_USERNAME', str(context.exception))
    
    def test_send_recovery_email_missing_smtp_password(self):
        """Test error when SMTP_PASSWORD is missing."""
        self._set_env_vars(SMTP_PASSWORD=None)
        
        with self.assertRaises(ValueError) as context:
            send_recovery_email('user@example.com', 'token123')
        
        self.assertIn('SMTP_PASSWORD', str(context.exception))
    
    def test_send_recovery_email_missing_smtp_from_email(self):
        """Test error when SMTP_FROM_EMAIL is missing."""
        self._set_env_vars(SMTP_FROM_EMAIL=None)
        
        with self.assertRaises(ValueError) as context:
            send_recovery_email('user@example.com', 'token123')
        
        self.assertIn('SMTP_FROM_EMAIL', str(context.exception))
    
    def test_send_recovery_email_missing_frontend_url(self):
        """Test error when FRONTEND_URL is missing."""
        self._set_env_vars(FRONTEND_URL=None)
        
        with self.assertRaises(ValueError) as context:
            send_recovery_email('user@example.com', 'token123')
        
        self.assertIn('FRONTEND_URL', str(context.exception))
    
    def test_send_recovery_email_missing_multiple_vars(self):
        """Test error message includes all missing variables."""
        self._set_env_vars(SMTP_HOST=None, SMTP_PORT=None, FRONTEND_URL=None)
        
        with self.assertRaises(ValueError) as context:
            send_recovery_email('user@example.com', 'token123')
        
        error_msg = str(context.exception)
        self.assertIn('SMTP_HOST', error_msg)
        self.assertIn('SMTP_PORT', error_msg)
        self.assertIn('FRONTEND_URL', error_msg)
    
    def test_send_recovery_email_invalid_port(self):
        """Test error when SMTP_PORT is not a valid integer."""
        self._set_env_vars(SMTP_PORT='invalid')
        
        with patch('app.utils.email.smtplib.SMTP'):
            with self.assertRaises(ValueError) as context:
                send_recovery_email('user@example.com', 'token123')
            
            self.assertIn('Invalid SMTP_PORT', str(context.exception))
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_smtp_connection_error(self, mock_smtp_class):
        """Test handling of SMTP connection errors."""
        self._set_env_vars()
        
        # Simulate SMTP connection error
        mock_smtp_class.side_effect = smtplib.SMTPConnectError(421, 'Cannot connect')
        
        with self.assertRaises(smtplib.SMTPException):
            send_recovery_email('user@example.com', 'token123')
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_smtp_auth_error(self, mock_smtp_class):
        """Test handling of SMTP authentication errors."""
        self._set_env_vars()
        
        mock_smtp = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        mock_smtp.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Authentication failed')
        
        with self.assertRaises(smtplib.SMTPException):
            send_recovery_email('user@example.com', 'token123')
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_includes_plain_text(self, mock_smtp_class):
        """Test that email includes plain text version."""
        self._set_env_vars()
        
        mock_smtp = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        send_recovery_email('user@example.com', 'token123')
        
        call_args = mock_smtp.sendmail.call_args[0]
        email_content = call_args[2]
        
        # Check for plain text markers
        self.assertIn('Content-Type: text/plain', email_content)
    
    @patch('app.utils.email.smtplib.SMTP')
    def test_send_recovery_email_includes_html(self, mock_smtp_class):
        """Test that email includes HTML version."""
        self._set_env_vars()
        
        mock_smtp = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        send_recovery_email('user@example.com', 'token123')
        
        call_args = mock_smtp.sendmail.call_args[0]
        email_content = call_args[2]
        
        # Check for HTML markers
        self.assertIn('Content-Type: text/html', email_content)
        self.assertIn('<html>', email_content)
        self.assertIn('<a href=', email_content)


if __name__ == '__main__':
    unittest.main()
