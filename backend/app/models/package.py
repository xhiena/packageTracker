from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Package(Base):
    """Package tracking model."""
    
    __tablename__ = "packages"
    
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(255), nullable=False)
    carrier = Column(String(50), nullable=False)  # correos, gls, etc.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(100), nullable=True)
    last_location = Column(String(255), nullable=True)
    # Use JSON.with_variant to support both PostgreSQL (JSONB) and SQLite (JSON)
    tracking_data = Column(JSON().with_variant(JSONB(), "postgresql"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to User model
    user = relationship("User", backref="packages")
    
    # Composite index for better query performance
    __table_args__ = (
        Index('idx_user_tracking', 'user_id', 'tracking_number'),
    )
