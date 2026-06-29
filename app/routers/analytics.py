from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get(
    "/leaderboard",
    response_model = schemas.LeaderboardOut,
)
def get_leaderboard(db: Session = Depends(get_db)):
    rows = db.execute(
        select(
            models.User.id.label("user_id"),
            models.User.name.label("name"),
            func.sum(models.Enrollment.completed_lessons_count).label("total_lessons_completed"),
        )
        .join(models.Enrollment, models.User.id == models.Enrollment.user_id)
        .group_by(models.User.id)
        .order_by(func.sum(models.Enrollment.completed_lessons_count).desc())
        .limit(5)
    ).all()

    leaderboard = [
        schemas.LeaderboardEntry(
            user_id=row.user_id,
            name=row.name,
            total_lessons_completed=row.total_lessons_completed,
        )
        for row in rows
    ]

    return schemas.LeaderboardOut(leaderboard=leaderboard)
