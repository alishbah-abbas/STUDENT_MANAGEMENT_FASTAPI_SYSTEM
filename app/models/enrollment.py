from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    # Ensure a student can't enroll in the same course twice
    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='unique_student_course'),)
