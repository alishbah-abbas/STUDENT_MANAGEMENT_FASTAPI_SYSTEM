from pydantic import BaseModel
from typing import List, Optional, ForwardRef

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True

# Forward reference to avoid circular imports
EnrollmentResponse = ForwardRef('EnrollmentResponse')

class CourseWithEnrollments(Course):
    enrollments: List[EnrollmentResponse] = []
