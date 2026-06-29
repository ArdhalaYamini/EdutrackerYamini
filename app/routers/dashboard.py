from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/users", tags=["Dashboard"])

@router.post(
    "",
    response_model=schemas.UserOut,
    status_code=201,
)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(models.User).where(models.User.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")
    user = models.User(name=payload.name, email=payload.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get(
    "/{user_id}/dashboard",
    response_model=schemas.DashboardOut,
)
def get_user_dashboard(user_id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found.")

    active_enrollments = db.scalars(
        select(models.Enrollment).where(
            models.Enrollment.user_id == user_id,
            models.Enrollment.status == models.EnrollmentStatus.active,
        )
    ).all()

    active_courses = []
    for enr in active_enrollments:
        total = enr.course.total_lessons
        completed = enr.completed_lessons_count
        progress = round((completed / total) * 100, 2) if total > 0 else 0.0
        active_courses.append(
            schemas.ActiveCourseProgress(
                enrollment_id=enr.id,
                course=enr.course,
                completed_lessons=completed,
                progress_percent=progress,
            )
        )

    achievements = db.scalars(
        select(models.Achievement).where(models.Achievement.user_id == user_id)
    ).all()

    return schemas.DashboardOut(
        user=user,
        active_courses=active_courses,
        achievements=achievements,
    )
