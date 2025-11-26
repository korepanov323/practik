from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    tablename = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), nullable=False)  # 'student', 'teacher', 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    enrollments = relationship("Enrollment", back_populates="user")
    created_courses = relationship("Course", back_populates="author")

class Course(Base):
    tablename = 'courses'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0.0)
    is_published = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    author = relationship("User", back_populates="created_courses")
    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course")

class Lesson(Base):
    tablename = 'lessons'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)  # Текст урока или ссылка на видео
    order_number = Column(Integer)  # Порядок урока в курсе
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    # Связи
    course = relationship("Course", back_populates="lessons")

class Enrollment(Base):
    tablename = 'enrollments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Float, default=0.0)  # % завершения курса
    
    # Связи
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

# Инициализация базы данных
engine = create_engine('sqlite:///courses.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)