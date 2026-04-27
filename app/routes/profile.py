from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from typing import List
from app.models.developer_profile import DeveloperProfile
from app.models.user import User
from app.schemas.profile import ProfileCreate, DeveloperProfileWithUser
from app.core.security import get_current_user
import uuid
import json

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/profile")
def create_or_update_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "developer":
        raise HTTPException(
            status_code=403, detail="Only developers can create profiles"
        )

    skills_json = json.dumps(profile_data.skills) if profile_data.skills else None

    existing = (
        db.query(DeveloperProfile).filter(DeveloperProfile.user_id == user_id).first()
    )
    if existing:
        existing.bio = profile_data.bio
        existing.skills = skills_json
        existing.portfolio_url = profile_data.portfolio_url
        existing.location = profile_data.location
        db.commit()
        db.refresh(existing)
        return {"message": "Profile updated successfully", "profile_id": existing.id}

    profile = DeveloperProfile(
        id=str(uuid.uuid4()),
        user_id=user_id,
        bio=profile_data.bio,
        skills=skills_json,
        portfolio_url=profile_data.portfolio_url,
        location=profile_data.location,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {"message": "Profile created successfully", "profile_id": profile.id}


@router.get("/profile/{user_id}", response_model=DeveloperProfileWithUser)
def get_profile(user_id: str, db: Session = Depends(get_db)):
    result = (
        db.query(DeveloperProfile, User)
        .join(User, DeveloperProfile.user_id == User.id)
        .filter(DeveloperProfile.user_id == user_id)
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile, user = result
    skills_list = None
    if profile.skills:
        try:
            skills_list = json.loads(profile.skills)
        except json.JSONDecodeError:
            skills_list = [s.strip() for s in profile.skills.split(",")]
    return DeveloperProfileWithUser(
        id=profile.id,
        user_id=profile.user_id,
        full_name=user.full_name,
        email=user.email,
        bio=profile.bio,
        skills=skills_list,
        portfolio_url=profile.portfolio_url,
        location=profile.location,
        created_at=profile.created_at,
    )


@router.get("/developers", response_model=List[DeveloperProfileWithUser])
def get_developers(db: Session = Depends(get_db)):
    results = (
        db.query(DeveloperProfile, User)
        .join(User, DeveloperProfile.user_id == User.id)
        .all()
    )

    response = []
    for profile, user in results:
        skills_list = None
        if profile.skills:
            try:
                skills_list = json.loads(profile.skills)
            except json.JSONDecodeError:
                skills_list = [s.strip() for s in profile.skills.split(",")]
        data = {
            "id": profile.id,
            "user_id": profile.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "bio": profile.bio,
            "skills": skills_list,
            "portfolio_url": profile.portfolio_url,
            "location": profile.location,
            "created_at": profile.created_at,
        }
        response.append(DeveloperProfileWithUser(**data))

    return response
