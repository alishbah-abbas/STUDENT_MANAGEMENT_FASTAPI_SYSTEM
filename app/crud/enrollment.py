
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course
from app.schemas.enrollment import EnrollmentCreate

def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    # Check if student and course exist
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    
    if not student:
        raise ValueError(f"Student with id {enrollment.student_id} not found")
    if not course:
        raise ValueError(f"Course with id {enrollment.course_id} not found")
    
    # Check if enrollment already exists
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()
    
    if existing:
        raise ValueError(f"Student {enrollment.student_id} is already enrolled in course {enrollment.course_id}")
    
    db_enrollment = Enrollment(student_id=enrollment.student_id, course_id=enrollment.course_id)
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Enrollment).offset(skip).limit(limit).all()

def get_enrollment(db: Session, enrollment_id: int):
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

def get_enrollments_by_student(db: Session, student_id: int):
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).all()

def get_enrollments_by_course(db: Session, course_id: int):
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()

def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if db_enrollment:
        db.delete(db_enrollment)
        db.commit()
    return db_enrollment