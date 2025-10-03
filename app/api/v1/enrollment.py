from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.enrollment import Enrollment, EnrollmentCreate
from app.crud import enrollment as crud_enrollment

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

@router.post("/", response_model=Enrollment)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        return crud_enrollment.create_enrollment(db=db, enrollment=enrollment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[Enrollment])
def read_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = crud_enrollment.get_enrollments(db, skip=skip, limit=limit)
    return enrollments

@router.get("/{enrollment_id}", response_model=Enrollment)
def read_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = crud_enrollment.get_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment

@router.get("/student/{student_id}", response_model=List[Enrollment])
def read_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    enrollments = crud_enrollment.get_enrollments_by_student(db, student_id=student_id)
    return enrollments

@router.get("/course/{course_id}", response_model=List[Enrollment])
def read_course_enrollments(course_id: int, db: Session = Depends(get_db)):
    enrollments = crud_enrollment.get_enrollments_by_course(db, course_id=course_id)
    return enrollments

@router.delete("/{enrollment_id}", response_model=Enrollment)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = crud_enrollment.delete_enrollment(db, enrollment_id=enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment
