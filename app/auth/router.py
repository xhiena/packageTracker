"""Authentication router with all auth endpoints."""
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, PasswordResetToken
from app.auth.schemas import (
    UserCreate,
    UserResponse,
    Token,
    ForgotPasswordRequest,
    PasswordResetRequest,
)
from app.auth.security import (
    hash_password,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.utils.email import send_password_reset_email
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user information
        
    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint to obtain JWT access token.
    
    OAuth2 compatible token login using username (email) and password.
    
    Args:
        form_data: OAuth2 form with username (email) and password
        db: Database session
        
    Returns:
        JWT access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Request a password reset link.
    
    Generates a unique, time-limited token and sends it via email.
    
    Args:
        request: Forgot password request with email
        db: Database session
        
    Returns:
        Success message (same response regardless of whether email exists for security)
    """
    # Always return success message to prevent email enumeration
    response_message = {
        "message": "If the email exists, a password reset link has been sent"
    }
    
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Return success anyway to prevent email enumeration
        return response_message
    
    # Generate secure random token
    reset_token = secrets.token_urlsafe(32)
    
    # Calculate expiration time
    expires_at = datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    
    # Invalidate any existing tokens for this user
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.is_used == False
    ).update({"is_used": True})
    
    # Create new password reset token
    password_reset_token = PasswordResetToken(
        user_id=user.id,
        token=reset_token,
        expires_at=expires_at,
        is_used=False,
    )
    
    db.add(password_reset_token)
    db.commit()
    
    # Send email with reset link
    await send_password_reset_email(user.email, reset_token)
    
    return response_message


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using a valid reset token.
    
    Args:
        request: Password reset request with token and new password
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If token is invalid, expired, or already used
    """
    # Find the token
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token,
        PasswordResetToken.is_used == False
    ).first()
    
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already used token"
        )
    
    # Check if token has expired
    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired"
        )
    
    # Get the user
    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user's password
    user.hashed_password = hash_password(request.new_password)
    user.updated_at = datetime.utcnow()
    
    # Mark token as used
    token_record.is_used = True
    
    db.commit()
    
    return {"message": "Password has been reset successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Protected route that requires valid JWT token.
    
    Args:
        current_user: Current authenticated user from JWT token
        
    Returns:
        Current user information
    """
    return current_user
