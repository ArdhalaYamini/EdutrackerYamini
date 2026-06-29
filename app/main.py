from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app import models
from app.routers import dashboard, enrollments, analytics

SEED_COURSES = [
    {"title": "Python Basics","description":"Learn Python from scratch.", "total_lessons": 5},
    {"title": "Intro to FastAPI", "description": "Build REST APIs with FastAPI.", "total_lessons": 3},
    {"title": "SQL 101", "description": "Relational databases and SQL fundamentals.", "total_lessons": 10},
]

def seed_database(db: Session) -> None:
    existing_titles = {c.title for c in db.query(models.Course).all()}
    for course_data in SEED_COURSES:
        if course_data["title"] not in existing_titles:
            db.add(models.Course(**course_data))
    db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="EduTrack API",
    description="Micro-learning progress tracking and analytics backend.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(dashboard.router)
app.include_router(enrollments.router)
app.include_router(analytics.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "EduTrack API is running."}
