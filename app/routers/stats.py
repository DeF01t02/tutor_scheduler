from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Lesson, Student, LessonStatus, User
from app.schemas.schemas import StatsSummary

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/summary", response_model=StatsSummary)
def get_stats(
    period: str = Query("month", enum=["week", "month", "year", "all"]),
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.utcnow()
    if start and end:
        date_from, date_to = start, end
    elif period == "week":
        date_from = now - timedelta(days=7)
        date_to = now
    elif period == "month":
        date_from = now.replace(day=1, hour=0, minute=0, second=0)
        date_to = now
    elif period == "year":
        date_from = now.replace(month=1, day=1, hour=0, minute=0, second=0)
        date_to = now
    else:
        date_from, date_to = None, None

    q = db.query(Lesson).join(Student).filter(Student.owner_id == current_user.id)
    if date_from:
        q = q.filter(Lesson.start_time >= date_from)
    if date_to:
        q = q.filter(Lesson.start_time <= date_to)

    lessons = q.all()
    completed = [l for l in lessons if l.status == LessonStatus.completed]

    total_revenue = sum(
        (l.duration_minutes / 60) * l.student.hourly_rate for l in completed
    )
    total_hours = sum(l.duration_minutes / 60 for l in completed)

    # By student
    by_student = {}
    for l in completed:
        sid = l.student_id
        if sid not in by_student:
            by_student[sid] = {"name": l.student.name, "lessons": 0, "hours": 0.0, "revenue": 0.0}
        by_student[sid]["lessons"] += 1
        hours = l.duration_minutes / 60
        by_student[sid]["hours"] += hours
        by_student[sid]["revenue"] += hours * l.student.hourly_rate

    return StatsSummary(
        total_revenue=round(total_revenue, 2),
        total_lessons=len(lessons),
        total_hours=round(total_hours, 2),
        completed_lessons=len(completed),
        cancelled_lessons=sum(1 for l in lessons if l.status == LessonStatus.cancelled),
        planned_lessons=sum(1 for l in lessons if l.status == LessonStatus.planned),
        by_student=list(by_student.values())
    )
