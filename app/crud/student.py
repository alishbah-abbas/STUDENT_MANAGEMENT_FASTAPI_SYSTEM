from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate

def create_student(db: Session, student: StudentCreate):
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student
