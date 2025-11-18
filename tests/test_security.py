"""Tests for security utilities."""
import pytest
from datetime import timedelta

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_hash_password():
    """Test password hashing."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0
    assert hashed.startswith("$2b$")  # bcrypt prefix


def test_verify_password_correct():
    """Test password verification with correct password."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert len(token) > 0
    assert isinstance(token, str)


def test_create_access_token_with_expiry():
    """Test JWT token creation with custom expiry."""
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    
    assert token is not None
    assert len(token) > 0


def test_decode_access_token_valid():
    """Test decoding a valid JWT token."""
    email = "test@example.com"
    data = {"sub": email}
    token = create_access_token(data)
    
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert decoded.email == email


def test_decode_access_token_invalid():
    """Test decoding an invalid JWT token."""
    decoded = decode_access_token("invalid.token.here")
    
    assert decoded is None


def test_decode_access_token_missing_sub():
    """Test decoding a token without 'sub' claim."""
    from jose import jwt
    from app.config import settings
    
    # Create a token without 'sub'
    token = jwt.encode({"some": "data"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    decoded = decode_access_token(token)
    
    assert decoded is None


def test_password_hash_unique():
    """Test that same password generates different hashes (due to salt)."""
    password = "testpassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
