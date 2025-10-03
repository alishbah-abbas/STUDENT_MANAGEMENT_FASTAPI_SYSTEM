from pydantic import BaseModel
from datetime import datetime
from typing import Optional, ForwardRef

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    enrollment_date: datetime

    class Config:
        from_attributes = True

# Forward references to avoid circular imports
Student = ForwardRef('Student')
Course = ForwardRef('Course')

class EnrollmentResponse(Enrollment):
    student: Optional[Student] = None
    course: Optional[Course] = None
