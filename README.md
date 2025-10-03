# Student Management API

A simple FastAPI application for managing students, courses, and enrollments.

## Features

- **Students**: Create, read, update, and delete student records
- **Courses**: Manage course information
- **Enrollments**: Handle student enrollments in courses with validation
- **SQLite Database**: Simple file-based database for easy development
- **Automatic API Documentation**: Swagger UI and ReDoc available

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API**
   - API Documentation (Swagger): http://localhost:8000/docs
   - Alternative Documentation (ReDoc): http://localhost:8000/redoc
   - API Base URL: http://localhost:8000/api/v1

## API Endpoints

### Students
- `POST /api/v1/students/` - Create a new student
- `GET /api/v1/students/` - List all students
- `GET /api/v1/students/{student_id}` - Get student details with enrollments
- `DELETE /api/v1/students/{student_id}` - Delete a student

### Courses
- `POST /api/v1/courses/` - Create a new course
- `GET /api/v1/courses/` - List all courses
- `GET /api/v1/courses/{course_id}` - Get course details with enrollments
- `DELETE /api/v1/courses/{course_id}` - Delete a course

### Enrollments
- `POST /api/v1/enrollments/` - Enroll a student in a course
- `GET /api/v1/enrollments/` - List all enrollments
- `GET /api/v1/enrollments/{enrollment_id}` - Get enrollment details
- `GET /api/v1/enrollments/student/{student_id}` - Get all enrollments for a student
- `GET /api/v1/enrollments/course/{course_id}` - Get all enrollments for a course
- `DELETE /api/v1/enrollments/{enrollment_id}` - Delete an enrollment

## Data Models

### Student
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Course
```json
{
  "title": "Introduction to Python",
  "description": "Learn Python programming basics"
}
```

### Enrollment
```json
{
  "student_id": 1,
  "course_id": 1
}
```

## Database

The application uses SQLite for simplicity. The database file (`student_management.db`) will be created automatically when you first run the application.

## Project Structure

```
app/
├── api/v1/          # API route handlers
├── crud/            # Database operations
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── core/            # Configuration
├── db/              # Database session management
├── database.py      # Database setup
└── main.py          # FastAPI application
```

## Development

The application is set up for easy development with:
- Hot reload enabled
- Comprehensive error handling
- Input validation
- Automatic API documentation
- Clean separation of concerns

## Notes

- Students cannot be enrolled in the same course twice
- Email addresses must be unique for students
- Deleting a student or course will automatically delete related enrollments
- All endpoints include proper error handling and validation
