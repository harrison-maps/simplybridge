from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    recipient_id = Column(String, nullable=False)
    sender_name = Column(String, nullable=False)
    sender_email = Column(String, nullable=False)
    project_scope = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(String, default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
