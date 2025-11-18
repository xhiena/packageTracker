"""Package model for tracking shipments."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.database import Base


class Package(Base):
    """Package model for storing tracking information."""
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tracking_number = Column(String, nullable=False, index=True)
    carrier_code = Column(String, nullable=False)  # e.g., 'GLS', 'SEUR'
    nickname = Column(String, nullable=True)
    status_data = Column(JSONB, nullable=True)  # PostgreSQL JSONB for complex JSON responses

    # Relationship to User model
    user = relationship("User", backref="packages")
