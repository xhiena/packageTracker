from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tracking_number = Column(String, nullable=False)
    carrier_code = Column(String, nullable=False)
    nickname = Column(String, nullable=True)
    status_data = Column(JSON, nullable=True)
