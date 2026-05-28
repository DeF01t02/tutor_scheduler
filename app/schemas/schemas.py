from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from app.models.models import LessonStatus

# Auth
class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# Students
class StudentCreate(BaseModel):
    name: str
    hourly_rate: float = 0.0
    subject: str = ""

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    hourly_rate: Optional[float] = None
    subject: Optional[str] = None

class StudentOut(BaseModel):
    id: int
    name: str
    hourly_rate: float
    subject: str
    class Config:
        from_attributes = True

# Lessons
class LessonCreate(BaseModel):
    student_id: int
    start_time: datetime
    duration_minutes: int = 60
    status: LessonStatus = LessonStatus.planned
    subject: str = ""
    notes: str = ""

class LessonUpdate(BaseModel):
    start_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[LessonStatus] = None
    subject: Optional[str] = None
    notes: Optional[str] = None

class LessonOut(BaseModel):
    id: int
    student_id: int
    start_time: datetime
    duration_minutes: int
    status: LessonStatus
    subject: str
    notes: str
    student: StudentOut
    class Config:
        from_attributes = True

# Stats
class StatsSummary(BaseModel):
    total_revenue: float
    total_lessons: int
    total_hours: float
    completed_lessons: int
    cancelled_lessons: int
    planned_lessons: int
    by_student: List[dict]
