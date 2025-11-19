from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)
from datetime import timedelta


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    # Hash should be different from password
    assert hashed != password
    
    # Verification should work
    assert verify_password(password, hashed) is True
    
    # Wrong password should fail
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_decode_token():
    """Test JWT token creation and decoding."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
    
    # Decode token
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


def test_create_token_with_expiration():
    """Test token creation with custom expiration."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=5)
    token = create_access_token(data, expires_delta)
    
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "testuser"


def test_decode_invalid_token():
    """Test decoding invalid token."""
    invalid_token = "invalid.token.here"
    decoded = decode_access_token(invalid_token)
    assert decoded is None
