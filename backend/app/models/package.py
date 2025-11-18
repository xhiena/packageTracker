from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.database import Base


class Package(Base):
    """Package tracking model."""
    
    __tablename__ = "packages"
    
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, index=True, nullable=False)
    carrier = Column(String, nullable=False)  # correos, gls, etc.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=True)
    last_location = Column(String, nullable=True)
    tracking_data = Column(Text, nullable=True)  # JSON string for full tracking history
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
