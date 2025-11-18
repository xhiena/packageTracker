"""Email utility for sending emails."""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.config import settings


async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    Send an email using SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text content (optional)
        
    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add plain text version if provided
        if text_content:
            part1 = MIMEText(text_content, "plain")
            message.attach(part1)
        
        # Add HTML version
        part2 = MIMEText(html_content, "html")
        message.attach(part2)
        
        # Send email
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            # Use authenticated SMTP
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True,
            )
        else:
            # For development/testing without SMTP credentials, just log
            print(f"[EMAIL] To: {to_email}")
            print(f"[EMAIL] Subject: {subject}")
            print(f"[EMAIL] Content: {html_content[:100]}...")
            
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


async def send_password_reset_email(email: str, token: str) -> bool:
    """
    Send password reset email with token.
    
    Args:
        email: User's email address
        token: Password reset token
        
    Returns:
        True if email was sent successfully
    """
    subject = f"{settings.APP_NAME} - Password Reset Request"
    
    # Create reset link (in production, this would be your frontend URL)
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background-color: #f9f9f9; }}
            .button {{ 
                display: inline-block; 
                padding: 12px 24px; 
                background-color: #4CAF50; 
                color: white; 
                text-decoration: none; 
                border-radius: 4px;
                margin: 20px 0;
            }}
            .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{settings.APP_NAME}</h1>
            </div>
            <div class="content">
                <h2>Password Reset Request</h2>
                <p>Hello,</p>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background-color: #fff; padding: 10px; border: 1px solid #ddd;">
                    {reset_link}
                </p>
                <p><strong>This link will expire in {settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hours.</strong></p>
                <p>If you didn't request a password reset, you can safely ignore this email.</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 {settings.APP_NAME}. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    {settings.APP_NAME} - Password Reset Request
    
    Hello,
    
    We received a request to reset your password. Visit the following link to create a new password:
    
    {reset_link}
    
    This link will expire in {settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hours.
    
    If you didn't request a password reset, you can safely ignore this email.
    
    © 2025 {settings.APP_NAME}. All rights reserved.
    """
    
    return await send_email(email, subject, html_content, text_content)
