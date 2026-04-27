from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.project import Project
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectWithOwner,
)
from app.core.security import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/projects", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    project = Project(
        owner_id=user_id,
        title=project_data.title,
        description=project_data.description,
        required_skills=project_data.required_skills,
        budget=project_data.budget,
        status=project_data.status,
    )

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects", response_model=List[ProjectWithOwner])
def get_projects(db: Session = Depends(get_db)):
    results = db.query(Project, User).join(User, Project.owner_id == User.id).all()

    response = []
    for project, user in results:
        response.append(
            ProjectWithOwner(
                id=project.id,
                owner_id=project.owner_id,
                owner_name=user.full_name,
                title=project.title,
                description=project.description,
                required_skills=project.required_skills,
                budget=project.budget,
                status=project.status,
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
        )

    return response


@router.get("/projects/{project_id}", response_model=ProjectWithOwner)
def get_project(project_id: str, db: Session = Depends(get_db)):
    result = (
        db.query(Project, User)
        .join(User, Project.owner_id == User.id)
        .filter(Project.id == project_id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Project not found")

    project, user = result
    return ProjectWithOwner(
        id=project.id,
        owner_id=project.owner_id,
        owner_name=user.full_name,
        title=project.title,
        description=project.description,
        required_skills=project.required_skills,
        budget=project.budget,
        status=project.status,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this project"
        )

    if project_data.title is not None:
        project.title = project_data.title
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.required_skills is not None:
        project.required_skills = project_data.required_skills
    if project_data.budget is not None:
        project.budget = project_data.budget
    if project_data.status is not None:
        project.status = project_data.status

    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}")
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this project"
        )

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}


@router.get("/users/{user_id}/projects", response_model=List[ProjectResponse])
def get_user_projects(user_id: str, db: Session = Depends(get_db)):
    projects = db.query(Project).filter(Project.owner_id == user_id).all()
    return projects
