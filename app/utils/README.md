# Email Utility

This module provides utility functions for sending emails, specifically for password recovery.

## Functions

### `send_recovery_email(email: str, token: str) -> None`

Sends a password recovery email to the specified email address with a password reset link.

**Parameters:**
- `email` (str): The recipient's email address
- `token` (str): The password reset token to include in the reset link

**Raises:**
- `ValueError`: If required environment variables are not set or if SMTP_PORT is invalid
- `smtplib.SMTPException`: If there's an error sending the email

**Required Environment Variables:**
- `SMTP_HOST`: SMTP server hostname (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (e.g., 587 for TLS)
- `SMTP_USERNAME`: SMTP authentication username
- `SMTP_PASSWORD`: SMTP authentication password
- `SMTP_FROM_EMAIL`: Email address to use in the "From" field
- `FRONTEND_URL`: Base URL of the frontend application

**Example Usage:**

```python
from app.utils.email import send_recovery_email

# Send a password recovery email
try:
    send_recovery_email('user@example.com', 'abc123token')
    print("Recovery email sent successfully!")
except ValueError as e:
    print(f"Configuration error: {e}")
except smtplib.SMTPException as e:
    print(f"Failed to send email: {e}")
```

**Email Content:**

The function sends a multipart email with both plain text and HTML versions. The email includes:
- Subject: "Password Reset Request"
- A password reset link in the format: `{FRONTEND_URL}/reset-password?token={token}`
- Instructions for the user
- A note to ignore the email if they didn't request a password reset

**Security Considerations:**

1. Store SMTP credentials securely using environment variables
2. Never commit `.env` files with real credentials to version control
3. Use app-specific passwords when using services like Gmail
4. The function uses STARTTLS for encrypted communication with the SMTP server
5. Tokens should be securely generated and have expiration times (handled by the calling code)
