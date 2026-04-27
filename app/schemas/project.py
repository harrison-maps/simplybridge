from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    title: str
    description: str
    required_skills: Optional[str] = None
    budget: Optional[str] = None
    status: str = "open"


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[str] = None
    budget: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    owner_id: str
    title: str
    description: str
    required_skills: Optional[str] = None
    budget: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectWithOwner(BaseModel):
    id: str
    owner_id: str
    owner_name: str
    title: str
    description: str
    required_skills: Optional[str] = None
    budget: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
