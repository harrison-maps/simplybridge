from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProfileCreate(BaseModel):
    bio: Optional[str] = None
    skills: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    location: Optional[str] = None


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    bio: Optional[str] = None
    skills: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    location: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DeveloperProfileWithUser(BaseModel):
    id: str
    user_id: str
    full_name: str
    email: str
    bio: Optional[str] = None
    skills: Optional[List[str]] = None
    portfolio_url: Optional[str] = None
    location: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
