from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    # Relationship with enrollments
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
