from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.course import Course, CourseCreate
from app.crud import course as crud_course

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return crud_course.create_course(db=db, course=course)

@router.get("/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud_course.get_courses(db, skip=skip, limit=limit)
    return courses

@router.get("/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.delete("/{course_id}", response_model=Course)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud_course.delete_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course
