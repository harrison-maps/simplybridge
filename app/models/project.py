from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import uuid
import enum


class ProjectStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(String, nullable=True)
    budget = Column(String, nullable=True)
    status = Column(String, nullable=False, default=ProjectStatus.OPEN.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
