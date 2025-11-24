from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


# Package schemas
class PackageCreate(BaseModel):
    tracking_number: str
    carrier: str
    description: Optional[str] = None


class PackageUpdate(BaseModel):
    description: Optional[str] = None
    carrier: Optional[str] = None


class PackageResponse(BaseModel):
    id: int
    tracking_number: str
    carrier: str
    user_id: int
    description: Optional[str]
    status: Optional[str]
    last_location: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TrackingInfo(BaseModel):
    status: Optional[str]
    location: Optional[str]
    history: List[Dict[str, Any]]
    error: Optional[str]
    carrier: Optional[str] = None


class CarrierInfo(BaseModel):
    carriers: List[str]
