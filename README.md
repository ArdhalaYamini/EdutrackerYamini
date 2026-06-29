## EduTracker API
A micro-learning progress tracking and analytics REST API built with FastAPI and SQLite.

## What was done in this project
A backend service for a mobile micro-learning platform that:
-Tracks user progress through short courses
-Manages achievements automatically
-Provides analytics for a student dashboard

## Tech stack
- **Framework:** FastAPI (Python 3.10+)
- **Database:** SQLite (file-based, no installation needed)
- **ORM:** SQLAlchemy
- **Validation:** Pydantic

## Project Structure
Edutracker/

├── app/
│   ├── init.py
│   ├── main.py             → App entry point + DB seeding
│   ├── database.py         → SQLAlchemy engine and session
│   ├── models.py           → Database tables (User, Course, Enrollment, Achievement)
│   ├── schemas.py          → Pydantic request/response shapes
│   └── routers/
│       ├── init.py
│       ├── enrollments.py  → Enrollment and lesson completion logic
│       ├── dashboard.py    → User creation and dashboard
│       └── analytics.py    → Leaderboard
├── requirements.txt
├── README.md
└── edutrack.db             → Auto created on first run

## Setup Instructions
-Step 1 __ Make sure Python is installed (Python 3.10+)
-Step2 __ Create virtual environment and install dependencies from requirments.txt file
-Step 3 __ Run the server (```bash uvicorn app.main:app --reload ```)

On first startup:
- `edutrack.db` is created automatically
- 3 sample courses are seeded automatically:
  - Python Basics (5 lessons)
  - Intro to FastAPI (3 lessons)
  - SQL 101 (10 lessons)

Server runs at: `http://127.0.0.1:8000`

Interactive API docs: `http://127.0.0.1:8000/docs`

## API Endpoints
1. User Endpoints
POST__'/users'__Create a new user
GET __'/user/{user_id}/dashboard'__Get User dashboard with progress and achievements
2. Enrollments Endpoints
POST__'/enrollments'__Enroll a user in a course
POST__'/enrollments/{enrollments_id}/complete-lesson'__Mark next lesson as complete
3. Analytics
GET___'/analytics/leaderboard'__Top 5 users by total lessons completes

## Sample Requests
1. Create User
```json
POST /users
{
    "name":"Yamini",
    "email":"email@example.com"
}
```

2. Enroll in a course
```json
POST /enrollments
{
  "user_id": 1,
  "course_id": 3
}
```

3. Complete a lesson
```json
POST /enrollments/1/complete-lesson
No request body needed.
```

4. Get Dashboard
```json
GET /users/1/dashboard
```

5. Get LeaderBoard
```json
GET /analytics/leaderboard
```

## Achievement System
**Fast Starter** - User completes their first ever course
**Deep Diver** - User completess a course that has 10 or more lessons

Achievements are awarded automatically no manual trigger needed.
