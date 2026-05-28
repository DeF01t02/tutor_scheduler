from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_
from app.core.database import get_db
from app.models.models import User, Lesson, LessonStatus
from app.core.security import get_current_user_with_scope

router = APIRouter(prefix="/master", tags=["master"])

@router.get("/subordinates")
def list_subordinates(current=Depends(get_current_user_with_scope), db: Session = Depends(get_db)):
    if not current["is_master"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return current["user"].subordinates

@router.get("/stats/aggregate")
def aggregate_stats(
    period: str = "month",  # week/month/year/all
    current=Depends(get_current_user_with_scope),
    db: Session = Depends(get_db)
):
    if not current["is_master"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user_ids = current["accessible_user_ids"]
    
    # Пример: общее количество уроков и доход
    query = db.query(
        func.count(Lesson.id).label("total_lessons"),
        func.sum(Lesson.duration_minutes).label("total_minutes"),
    ).filter(
        Lesson.student_id.in_(
            db.query(Student.id).filter(Student.owner_id.in_(user_ids))
        ),
        Lesson.status == LessonStatus.completed
    )
    
    # 🔹 Добавьте фильтрацию по периоду при необходимости
    # if period != "all":
    #     ... добавить условие по start_time
    
    result = query.first()
    return {
        "total_lessons": result.total_lessons or 0,
        "total_minutes": result.total_minutes or 0,
        "estimated_revenue": (result.total_minutes or 0) / 60 * 1000  # пример расчёта
    }