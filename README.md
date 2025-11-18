# packageTracker
a simple shipping package tracker

## Features

### Email Utility

The application includes an email utility for sending password recovery emails. The utility is located in `app/utils/email.py` and provides the following functionality:

- **Password Recovery Emails**: Send secure password reset links to users via email
- **SMTP Support**: Uses Python's standard library `smtplib` for reliable email delivery
- **Multipart Emails**: Sends both plain text and HTML versions for better compatibility
- **Secure Communication**: Uses STARTTLS for encrypted communication with SMTP servers

## Setup

### Environment Configuration

Copy the example environment file and configure your SMTP settings:

```bash
cp .env.example .env
```

Edit the `.env` file and set the following variables:

- `SMTP_HOST`: Your SMTP server hostname (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (usually 587 for TLS)
- `SMTP_USERNAME`: Your SMTP username
- `SMTP_PASSWORD`: Your SMTP password
- `SMTP_FROM_EMAIL`: Email address to use in the "From" field
- `FRONTEND_URL`: Base URL of your frontend application

### Usage Example

```python
from app.utils.email import send_recovery_email

# Send a password recovery email
try:
    send_recovery_email('user@example.com', 'secure_token_here')
    print("Recovery email sent successfully!")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Failed to send email: {e}")
```

For more examples, see `example_usage.py`.

## Testing

Run the tests using Python's unittest:

```bash
python -m unittest tests.test_email -v
```

## Documentation

- [Email Utility Documentation](app/utils/README.md)
