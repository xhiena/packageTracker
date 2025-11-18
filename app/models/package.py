"""Package model for tracking shipments."""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.database import Base


class Package(Base):
    """Package model for storing tracking information."""
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tracking_number = Column(String, nullable=False)
    carrier_code = Column(String(50), nullable=False)  # e.g., 'GLS', 'SEUR'
    nickname = Column(String(255), nullable=True)
    status_data = Column(JSONB, nullable=True)  # PostgreSQL JSONB for complex JSON responses

    # Relationship to User model
    user = relationship("User", backref="packages")

    # Composite index for user_id and tracking_number
    __table_args__ = (
        Index('idx_user_tracking', 'user_id', 'tracking_number'),
    )
