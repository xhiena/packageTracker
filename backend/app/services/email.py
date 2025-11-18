import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings


class EmailService:
    """Service for sending emails via SMTP."""
    
    @staticmethod
    def send_password_reset_email(to_email: str, reset_token: str) -> bool:
        """Send a password reset email to the user.
        
        Args:
            to_email: Recipient email address
            reset_token: Password reset token
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{settings.APP_NAME} - Password Reset"
            msg['From'] = settings.SMTP_FROM
            msg['To'] = to_email
            
            # Create reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
            
            # Email body
            text = f"""
Hello,

You requested a password reset for your {settings.APP_NAME} account.

Click the link below to reset your password:
{reset_link}

This link will expire in 30 minutes.

If you didn't request this, please ignore this email.

Best regards,
{settings.APP_NAME} Team
            """
            
            html = f"""
<html>
  <body>
    <h2>{settings.APP_NAME} - Password Reset</h2>
    <p>Hello,</p>
    <p>You requested a password reset for your {settings.APP_NAME} account.</p>
    <p><a href="{reset_link}">Click here to reset your password</a></p>
    <p>This link will expire in 30 minutes.</p>
    <p>If you didn't request this, please ignore this email.</p>
    <br>
    <p>Best regards,<br>{settings.APP_NAME} Team</p>
  </body>
</html>
            """
            
            # Attach parts
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
                print("SMTP credentials not configured, skipping email send")
                return False
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
