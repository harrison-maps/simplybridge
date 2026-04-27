from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class DeveloperProfile(Base):
    __tablename__ = "developer_profiles"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(String, nullable=True)
    skills = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())