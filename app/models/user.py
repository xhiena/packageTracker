"""User model for authentication and user management."""
from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):
    """User model with authentication fields."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
