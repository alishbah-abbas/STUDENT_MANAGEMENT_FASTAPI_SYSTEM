from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate

def create_course(db: Session, course: CourseCreate):
    db_course = Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def delete_course(db: Session, course_id: int):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
    return db_course
