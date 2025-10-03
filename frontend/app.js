// Student Management System Frontend JavaScript
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Global variables to store data
let students = [];
let courses = [];
let enrollments = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkApiStatus();
    loadStudents();
    loadCourses();
    loadEnrollments();
    
    // Set up form event listeners
    setupEventListeners();
    
    // Check API status every 30 seconds
    setInterval(checkApiStatus, 30000);
});

// Setup event listeners
function setupEventListeners() {
    // Student form
    document.getElementById('student-form').addEventListener('submit', handleStudentSubmit);
    
    // Course form
    document.getElementById('course-form').addEventListener('submit', handleCourseSubmit);
    
    // Enrollment form
    document.getElementById('enrollment-form').addEventListener('submit', handleEnrollmentSubmit);
}

// Check API status
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/debug/db-status`);
        const data = await response.json();
        
        if (response.ok) {
            updateApiStatus(true, `Connected - ${data.counts.students} students, ${data.counts.courses} courses`);
        } else {
            updateApiStatus(false, 'API Error');
        }
    } catch (error) {
        updateApiStatus(false, 'API Offline');
    }
}

// Update API status indicator
function updateApiStatus(isOnline, message) {
    const statusIndicator = document.getElementById('api-status');
    const statusText = document.getElementById('api-status-text');
    
    if (isOnline) {
        statusIndicator.className = 'status-indicator status-online';
        statusText.textContent = message;
        statusText.className = 'text-success';
    } else {
        statusIndicator.className = 'status-indicator status-offline';
        statusText.textContent = message;
        statusText.className = 'text-danger';
    }
}

// Show toast notification
function showToast(title, message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');
    
    // Set icon and color based on type
    const icons = {
        success: 'fas fa-check-circle text-success',
        error: 'fas fa-exclamation-circle text-danger',
        warning: 'fas fa-exclamation-triangle text-warning',
        info: 'fas fa-info-circle text-primary'
    };
    
    toastIcon.className = icons[type] || icons.info;
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// API request helper
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Load students
async function loadStudents() {
    try {
        students = await apiRequest('/students/');
        renderStudents();
        updateStudentSelect();
    } catch (error) {
        document.getElementById('students-list').innerHTML = 
            '<div class="alert alert-danger">Failed to load students: ' + error.message + '</div>';
    }
}

// Load courses
async function loadCourses() {
    try {
        courses = await apiRequest('/courses/');
        renderCourses();
        updateCourseSelect();
    } catch (error) {
        document.getElementById('courses-list').innerHTML = 
            '<div class="alert alert-danger">Failed to load courses: ' + error.message + '</div>';
    }
}

// Load enrollments
async function loadEnrollments() {
    try {
        enrollments = await apiRequest('/enrollments/');
        renderEnrollments();
    } catch (error) {
        document.getElementById('enrollments-list').innerHTML = 
            '<div class="alert alert-danger">Failed to load enrollments: ' + error.message + '</div>';
    }
}

// Render students
function renderStudents() {
    const container = document.getElementById('students-list');
    
    if (students.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No students found. Add some students to get started!</div>';
        return;
    }
    
    const html = students.map(student => `
        <div class="card mb-2">
            <div class="card-body py-2">
                <div class="row align-items-center">
                    <div class="col">
                        <h6 class="mb-0">${student.name}</h6>
                        <small class="text-muted">${student.email}</small>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteStudent(${student.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// Render courses
function renderCourses() {
    const container = document.getElementById('courses-list');
    
    if (courses.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No courses found. Add some courses to get started!</div>';
        return;
    }
    
    const html = courses.map(course => `
        <div class="card mb-2">
            <div class="card-body py-2">
                <div class="row align-items-center">
                    <div class="col">
                        <h6 class="mb-0">${course.title}</h6>
                        <small class="text-muted">${course.description || 'No description'}</small>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteCourse(${course.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// Render enrollments
function renderEnrollments() {
    const container = document.getElementById('enrollments-list');
    
    if (enrollments.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No enrollments found.</div>';
        return;
    }
    
    const html = enrollments.map(enrollment => {
        const student = students.find(s => s.id === enrollment.student_id);
        const course = courses.find(c => c.id === enrollment.course_id);
        
        return `
            <div class="card mb-2">
                <div class="card-body py-2">
                    <div class="row align-items-center">
                        <div class="col">
                            <strong>${student ? student.name : 'Unknown Student'}</strong> 
                            enrolled in 
                            <strong>${course ? course.title : 'Unknown Course'}</strong>
                            <br>
                            <small class="text-muted">
                                Enrolled: ${new Date(enrollment.enrollment_date).toLocaleDateString()}
                            </small>
                        </div>
                        <div class="col-auto">
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteEnrollment(${enrollment.id})">
                                <i class="fas fa-unlink"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

// Update student select dropdown
function updateStudentSelect() {
    const select = document.getElementById('enrollment-student');
    select.innerHTML = '<option value="">Choose student...</option>';
    
    students.forEach(student => {
        const option = document.createElement('option');
        option.value = student.id;
        option.textContent = student.name;
        select.appendChild(option);
    });
}

// Update course select dropdown
function updateCourseSelect() {
    const select = document.getElementById('enrollment-course');
    select.innerHTML = '<option value="">Choose course...</option>';
    
    courses.forEach(course => {
        const option = document.createElement('option');
        option.value = course.id;
        option.textContent = course.title;
        select.appendChild(option);
    });
}

// Handle student form submission
async function handleStudentSubmit(event) {
    event.preventDefault();
    
    const name = document.getElementById('student-name').value;
    const email = document.getElementById('student-email').value;
    
    try {
        await apiRequest('/students/', {
            method: 'POST',
            body: JSON.stringify({ name, email })
        });
        
        showToast('Success', 'Student added successfully!', 'success');
        document.getElementById('student-form').reset();
        loadStudents();
    } catch (error) {
        showToast('Error', 'Failed to add student: ' + error.message, 'error');
    }
}

// Handle course form submission
async function handleCourseSubmit(event) {
    event.preventDefault();
    
    const title = document.getElementById('course-title').value;
    const description = document.getElementById('course-description').value;
    
    try {
        await apiRequest('/courses/', {
            method: 'POST',
            body: JSON.stringify({ title, description })
        });
        
        showToast('Success', 'Course added successfully!', 'success');
        document.getElementById('course-form').reset();
        loadCourses();
    } catch (error) {
        showToast('Error', 'Failed to add course: ' + error.message, 'error');
    }
}

// Handle enrollment form submission
async function handleEnrollmentSubmit(event) {
    event.preventDefault();
    
    const studentId = parseInt(document.getElementById('enrollment-student').value);
    const courseId = parseInt(document.getElementById('enrollment-course').value);
    
    try {
        await apiRequest('/enrollments/', {
            method: 'POST',
            body: JSON.stringify({ student_id: studentId, course_id: courseId })
        });
        
        showToast('Success', 'Student enrolled successfully!', 'success');
        document.getElementById('enrollment-form').reset();
        loadEnrollments();
    } catch (error) {
        showToast('Error', 'Failed to enroll student: ' + error.message, 'error');
    }
}

// Delete student
async function deleteStudent(studentId) {
    if (!confirm('Are you sure you want to delete this student?')) return;
    
    try {
        await apiRequest(`/students/${studentId}`, { method: 'DELETE' });
        showToast('Success', 'Student deleted successfully!', 'success');
        loadStudents();
        loadEnrollments(); // Refresh enrollments as they might be affected
    } catch (error) {
        showToast('Error', 'Failed to delete student: ' + error.message, 'error');
    }
}

// Delete course
async function deleteCourse(courseId) {
    if (!confirm('Are you sure you want to delete this course?')) return;
    
    try {
        await apiRequest(`/courses/${courseId}`, { method: 'DELETE' });
        showToast('Success', 'Course deleted successfully!', 'success');
        loadCourses();
        loadEnrollments(); // Refresh enrollments as they might be affected
    } catch (error) {
        showToast('Error', 'Failed to delete course: ' + error.message, 'error');
    }
}

// Delete enrollment
async function deleteEnrollment(enrollmentId) {
    if (!confirm('Are you sure you want to remove this enrollment?')) return;
    
    try {
        await apiRequest(`/enrollments/${enrollmentId}`, { method: 'DELETE' });
        showToast('Success', 'Enrollment removed successfully!', 'success');
        loadEnrollments();
    } catch (error) {
        showToast('Error', 'Failed to remove enrollment: ' + error.message, 'error');
    }
}
