from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Student, User
from app.schemas.schemas import StudentCreate, StudentUpdate, StudentOut

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=List[StudentOut])
def get_students(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Student).filter(Student.owner_id == current_user.id).all()

@router.post("/", response_model=StudentOut)
def create_student(data: StudentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = Student(**data.dict(), owner_id=current_user.id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.put("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id, Student.owner_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for k, v in data.dict(exclude_none=True).items():
        setattr(student, k, v)
    db.commit()
    db.refresh(student)
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id, Student.owner_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"ok": True}
