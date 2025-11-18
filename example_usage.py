"""Example usage of the send_recovery_email function.

This script demonstrates how to use the email utility to send password recovery emails.
Before running, make sure to set the required environment variables in a .env file or export them.
"""

import os
import smtplib
from app.utils.email import send_recovery_email


def main():
    """Demonstrate email utility usage."""
    # Example 1: Basic usage
    print("Example 1: Sending a password recovery email")
    print("-" * 50)
    
    try:
        # In a real application, you would:
        # 1. Generate a secure token (e.g., using secrets.token_urlsafe())
        # 2. Store the token in your database with an expiration time
        # 3. Send the email with the token
        
        email_address = "user@example.com"
        reset_token = "example_token_abc123"
        
        print(f"Sending recovery email to: {email_address}")
        print(f"Reset token: {reset_token}")
        
        # Uncomment the following line to actually send the email
        # Make sure you have set the required environment variables first!
        # send_recovery_email(email_address, reset_token)
        
        print("✓ Email would be sent successfully!")
        print(f"  Reset link: {os.getenv('FRONTEND_URL', 'https://example.com')}/reset-password?token={reset_token}")
        
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nMake sure you have set all required environment variables:")
        print("  - SMTP_HOST")
        print("  - SMTP_PORT")
        print("  - SMTP_USERNAME")
        print("  - SMTP_PASSWORD")
        print("  - SMTP_FROM_EMAIL")
        print("  - FRONTEND_URL")
        
    except smtplib.SMTPException as e:
        print(f"✗ Failed to send email: {e}")
        print("\nCheck your SMTP configuration and credentials.")
    
    # Example 2: Check environment configuration
    print("\n" + "=" * 50)
    print("Example 2: Checking environment configuration")
    print("-" * 50)
    
    required_vars = [
        'SMTP_HOST',
        'SMTP_PORT',
        'SMTP_USERNAME',
        'SMTP_PASSWORD',
        'SMTP_FROM_EMAIL',
        'FRONTEND_URL'
    ]
    
    print("Environment variable status:")
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var:
                display_value = '***' + value[-3:] if len(value) > 3 else '***'
            else:
                display_value = value
            print(f"  ✓ {var}: {display_value}")
        else:
            print(f"  ✗ {var}: Not set")
            all_set = False
    
    if all_set:
        print("\n✓ All environment variables are set!")
    else:
        print("\n✗ Some environment variables are missing. Please set them before using the email utility.")
        print("\nYou can copy .env.example to .env and fill in your values:")
        print("  cp .env.example .env")


if __name__ == "__main__":
    main()
