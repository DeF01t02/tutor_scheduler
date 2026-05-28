from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class LessonStatus(str, enum.Enum):
    planned = "planned"
    completed = "completed"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # 🔹 Новые поля для мастер-аккаунта
    is_master = Column(Boolean, default=False)  # Флаг мастер-аккаунта
    master_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Ссылка на мастера
    
    # 🔹 Отношения
    students = relationship("Student", back_populates="owner", cascade="all, delete-orphan")
    # Подчинённые аккаунты (если это мастер)
    subordinates = relationship("User", backref="master", remote_side=[id])

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    hourly_rate = Column(Float, default=0.0)
    subject = Column(String, default="")
    owner = relationship("User", back_populates="students")
    lessons = relationship("Lesson", back_populates="student", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(Enum(LessonStatus), default=LessonStatus.planned)
    subject = Column(String, default="")
    notes = Column(String, default="")
    student = relationship("Student", back_populates="lessons")
