from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.student import Student, StudentCreate
from app.crud import student as crud_student

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    print(f"DEBUG: Creating student with name='{student.name}', email='{student.email}'")
    
    # Check if student with email already exists
    db_student = crud_student.get_student_by_email(db, email=student.email)
    if db_student:
        print(f"DEBUG: Student with email {student.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the student
    created_student = crud_student.create_student(db=db, student=student)
    print(f"DEBUG: Student created successfully with ID: {created_student.id}")
    
    # Verify it was saved
    all_students = crud_student.get_students(db)
    print(f"DEBUG: Total students in database: {len(all_students)}")
    
    return created_student

@router.get("/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud_student.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud_student.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/{student_id}", response_model=Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud_student.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student
