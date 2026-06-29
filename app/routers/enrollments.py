from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


def _award_achievement_if_new(db, user_id, title, newly_unlocked):
    exists = db.scalar(
        select(func.count(models.Achievement.id)).where(
            models.Achievement.user_id == user_id,
            models.Achievement.title == title,
        )
    )
    if not exists:
        achievement = models.Achievement(user_id=user_id, title=title)
        db.add(achievement)
        db.flush()
        newly_unlocked.append(achievement)


@router.post(
    "",
    response_model=schemas.EnrollmentOut,
    status_code=status.HTTP_201_CREATED,
)
def enroll_user(payload: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    user = db.get(models.User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {payload.user_id} not found.")

    course = db.get(models.Course, payload.course_id)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {payload.course_id} not found.")

    existing = db.scalar(
        select(models.Enrollment).where(
            models.Enrollment.user_id == payload.user_id,
            models.Enrollment.course_id == payload.course_id,
            models.Enrollment.status == models.EnrollmentStatus.active,
        )
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already has an active enrollment in this course.",
        )

    enrollment = models.Enrollment(user_id=payload.user_id, course_id=payload.course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.post(
    "/{enrollment_id}/complete-lesson",
    response_model=schemas.CompleteLessonOut,
)
def complete_lesson(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.get(models.Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail=f"Enrollment {enrollment_id} not found.")

    if enrollment.status == models.EnrollmentStatus.completed:
        raise HTTPException(
            status_code=400,
            detail="Cannot complete a lesson on an already-finished course.",
        )

    course = enrollment.course
    enrollment.completed_lessons_count += 1
    newly_unlocked = []

    if enrollment.completed_lessons_count >= course.total_lessons:
        enrollment.status = models.EnrollmentStatus.completed
        enrollment.completed_at = datetime.now(timezone.utc)

        db.flush()

        completed_count = db.scalar(
            select(func.count(models.Enrollment.id)).where(
                models.Enrollment.user_id == enrollment.user_id,
                models.Enrollment.status == models.EnrollmentStatus.completed,
            )
        )

        if completed_count == 1:
            _award_achievement_if_new(db, enrollment.user_id, "Fast Starter", newly_unlocked)

        if course.total_lessons >= 10:
            _award_achievement_if_new(db, enrollment.user_id, "Deep Diver", newly_unlocked)

    db.commit()
    db.refresh(enrollment)
    for ach in newly_unlocked:
        db.refresh(ach)

    return schemas.CompleteLessonOut(
        enrollment=enrollment,
        newly_unlocked_achievements=newly_unlocked,
    )
