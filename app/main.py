from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import student, course, enrollment
from app.database import engine
from app.models import base, student as student_model, course as course_model, enrollment as enrollment_model

# Create database tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="A simple API for managing students, courses, and enrollments",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(student.router, prefix="/api/v1")
app.include_router(course.router, prefix="/api/v1")
app.include_router(enrollment.router, prefix="/api/v1")

# Root route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Student Management API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Debug endpoint to check database status
@app.get("/debug/db-status")
def check_db_status():
    from app.db.session import get_db
    from app.models.student import Student
    from app.models.course import Course
    from app.models.enrollment import Enrollment
    
    db = next(get_db())
    try:
        student_count = db.query(Student).count()
        course_count = db.query(Course).count()
        enrollment_count = db.query(Enrollment).count()
        
        # Get all students with details
        students = db.query(Student).all()
        student_list = [{"id": s.id, "name": s.name, "email": s.email} for s in students]
        
        return {
            "database_status": "connected",
            "counts": {
                "students": student_count,
                "courses": course_count,
                "enrollments": enrollment_count
            },
            "students": student_list
        }
    except Exception as e:
        return {
            "database_status": "error",
            "error": str(e)
        }
    finally:
        db.close()
