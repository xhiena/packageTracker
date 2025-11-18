import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_recovery_email(email: str, token: str):
    """
    Send a password recovery email to the user.
    
    Args:
        email: The recipient's email address
        token: The password reset token
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    email_from = os.getenv("EMAIL_FROM", smtp_user)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = email_from
    message["To"] = email
    
    # Create reset link
    reset_link = f"{frontend_url}/reset-password?token={token}"
    
    # Email body
    text = f"""
    Hello,
    
    You have requested to reset your password. Please click the link below to reset your password:
    
    {reset_link}
    
    If you did not request this, please ignore this email.
    
    This link will expire in 1 hour.
    
    Best regards,
    Package Tracker Team
    """
    
    html = f"""
    <html>
      <body>
        <p>Hello,</p>
        <p>You have requested to reset your password. Please click the link below to reset your password:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>If you did not request this, please ignore this email.</p>
        <p>This link will expire in 1 hour.</p>
        <p>Best regards,<br>Package Tracker Team</p>
      </body>
    </html>
    """
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    message.attach(part1)
    message.attach(part2)
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_from, email, message.as_string())
