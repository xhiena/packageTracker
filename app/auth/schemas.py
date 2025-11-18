"""Pydantic schemas for authentication."""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")
    full_name: Optional[str] = Field(None, description="User's full name")


class UserResponse(BaseModel):
    """Schema for user response (without password)."""
    
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    
    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Schema for JWT token response."""
    
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    
    email: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    
    email: EmailStr = Field(..., description="User's email address to send recovery link")


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")
