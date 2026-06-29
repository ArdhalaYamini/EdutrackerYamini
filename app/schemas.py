from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models import EnrollmentStatus

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    created_at: datetime

class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    total_lessons: int

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    course_id: int
    completed_lessons_count: int
    status: EnrollmentStatus
    started_at: datetime
    completed_at: datetime | None

class AchievementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    unlocked_at: datetime

class ActiveCourseProgress(BaseModel):
    enrollment_id: int
    course: CourseOut
    completed_lessons: int
    progress_percent: float

class DashboardOut(BaseModel):
    user: UserOut
    active_courses: list[ActiveCourseProgress]
    achievements: list[AchievementOut]

class LeaderboardEntry(BaseModel):
    user_id: int
    name: str
    total_lessons_completed: int

class LeaderboardOut(BaseModel):
    leaderboard: list[LeaderboardEntry]

class CompleteLessonOut(BaseModel):
    enrollment: EnrollmentOut
    newly_unlocked_achievements: list[AchievementOut]
