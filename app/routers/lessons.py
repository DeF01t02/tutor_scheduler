from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Lesson, Student, User
from app.schemas.schemas import LessonCreate, LessonUpdate, LessonOut

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/", response_model=List[LessonOut])
def get_lessons(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    student_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(Lesson).join(Student).filter(Student.owner_id == current_user.id).options(joinedload(Lesson.student))
    if start:
        q = q.filter(Lesson.start_time >= start)
    if end:
        q = q.filter(Lesson.start_time <= end)
    if student_id:
        q = q.filter(Lesson.student_id == student_id)
    return q.order_by(Lesson.start_time).all()

@router.post("/", response_model=LessonOut)
def create_lesson(data: LessonCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == data.student_id, Student.owner_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    lesson = Lesson(**data.dict())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return db.query(Lesson).options(joinedload(Lesson.student)).filter(Lesson.id == lesson.id).first()

@router.put("/{lesson_id}", response_model=LessonOut)
def update_lesson(lesson_id: int, data: LessonUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).join(Student).filter(Lesson.id == lesson_id, Student.owner_id == current_user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for k, v in data.dict(exclude_none=True).items():
        setattr(lesson, k, v)
    db.commit()
    db.refresh(lesson)
    return db.query(Lesson).options(joinedload(Lesson.student)).filter(Lesson.id == lesson.id).first()

@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lesson = db.query(Lesson).join(Student).filter(Lesson.id == lesson_id, Student.owner_id == current_user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"ok": True}
