"""Email utility functions for sending password recovery emails."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


def send_recovery_email(email: str, token: str) -> None:
    """
    Send a password recovery email to the specified email address.
    
    Args:
        email: The recipient's email address
        token: The password reset token to include in the reset link
        
    Raises:
        ValueError: If required environment variables are not set
        smtplib.SMTPException: If there's an error sending the email
    """
    # Get SMTP configuration from environment variables
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_port = os.environ.get('SMTP_PORT')
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    smtp_from_email = os.environ.get('SMTP_FROM_EMAIL')
    frontend_url = os.environ.get('FRONTEND_URL')
    
    # Validate required environment variables
    if not all([smtp_host, smtp_port, smtp_username, smtp_password, smtp_from_email, frontend_url]):
        missing_vars = []
        if not smtp_host:
            missing_vars.append('SMTP_HOST')
        if not smtp_port:
            missing_vars.append('SMTP_PORT')
        if not smtp_username:
            missing_vars.append('SMTP_USERNAME')
        if not smtp_password:
            missing_vars.append('SMTP_PASSWORD')
        if not smtp_from_email:
            missing_vars.append('SMTP_FROM_EMAIL')
        if not frontend_url:
            missing_vars.append('FRONTEND_URL')
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Construct the password reset link
    reset_link = f"{frontend_url}/reset-password?token={token}"
    
    # Create the email message
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Password Reset Request'
    message['From'] = smtp_from_email
    message['To'] = email
    
    # Create plain text and HTML versions of the email
    text_body = f"""
Hello,

You have requested to reset your password. Please click the link below to reset your password:

{reset_link}

If you did not request this password reset, please ignore this email.

Best regards,
Package Tracker Team
"""
    
    html_body = f"""
<html>
  <body>
    <p>Hello,</p>
    <p>You have requested to reset your password. Please click the link below to reset your password:</p>
    <p><a href="{reset_link}">Reset Password</a></p>
    <p>Or copy and paste this URL into your browser:</p>
    <p>{reset_link}</p>
    <p>If you did not request this password reset, please ignore this email.</p>
    <p>Best regards,<br>Package Tracker Team</p>
  </body>
</html>
"""
    
    # Attach both plain text and HTML versions
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    message.attach(part1)
    message.attach(part2)
    
    # Send the email using SMTP
    try:
        # Convert port to integer
        port = int(smtp_port)
        
        # Create SMTP connection
        with smtplib.SMTP(smtp_host, port) as server:
            # Enable TLS encryption
            server.starttls()
            # Login to the SMTP server
            server.login(smtp_username, smtp_password)
            # Send the email
            server.sendmail(smtp_from_email, email, message.as_string())
    except ValueError as e:
        raise ValueError(f"Invalid SMTP_PORT value: {smtp_port}") from e
    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(f"Failed to send email: {str(e)}") from e
