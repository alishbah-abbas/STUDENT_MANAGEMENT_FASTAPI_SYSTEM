from pydantic import BaseModel
from typing import List, Optional, ForwardRef
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    
    class Config:
        from_attributes = True

# Forward reference to avoid circular imports
EnrollmentResponse = ForwardRef('EnrollmentResponse')

class StudentWithEnrollments(Student):
    enrollments: List[EnrollmentResponse] = []