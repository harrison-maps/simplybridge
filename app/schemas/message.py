from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageCreate(BaseModel):
    recipient_id: str
    sender_name: str
    sender_email: str
    project_scope: Optional[str] = None
    message: str


class MessageResponse(BaseModel):
    id: str
    recipient_id: str
    sender_name: str
    sender_email: str
    project_scope: Optional[str] = None
    message: str
    is_read: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
