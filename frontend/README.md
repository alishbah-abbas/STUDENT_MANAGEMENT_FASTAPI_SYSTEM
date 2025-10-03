# Student Management System - Frontend

A simple, modern web interface for testing the Student Management API.

## Features

- ✅ **Add Students** - Create new student records
- ✅ **Add Courses** - Create new courses  
- ✅ **Enroll Students** - Enroll students in courses
- ✅ **View All Data** - See students, courses, and enrollments
- ✅ **Delete Records** - Remove students, courses, or enrollments
- ✅ **Real-time API Status** - Shows if backend is running
- ✅ **Responsive Design** - Works on desktop and mobile

## How to Use

### Step 1: Start Your Backend
Make sure your FastAPI backend is running:
```bash
cd "C:\Users\Vertex\Desktop\demo project"
python run.py
```

### Step 2: Open Frontend
Simply open `index.html` in your web browser:
- **Option 1**: Double-click `index.html`
- **Option 2**: Right-click → "Open with" → Your browser
- **Option 3**: Drag `index.html` to your browser

### Step 3: Test the API
The frontend will automatically connect to `http://127.0.0.1:8000`

## API Status Indicator

- 🟢 **Green dot**: Backend is running and connected
- 🔴 **Red dot**: Backend is offline or not accessible

## What You Can Test

1. **Create Students**: Add students with name and email
2. **Create Courses**: Add courses with title and description  
3. **Enroll Students**: Link students to courses
4. **View Data**: See all records in real-time
5. **Delete Records**: Remove any student, course, or enrollment

## Files in This Frontend

- `index.html` - Main interface
- `app.js` - JavaScript functionality
- `README.md` - This documentation

## Easy Removal

To remove this frontend completely:
```bash
# Just delete the entire frontend folder
rmdir /s frontend
```

This will not affect your backend API at all!

## Browser Compatibility

Works with all modern browsers:
- Chrome, Firefox, Safari, Edge
- No additional software needed
- Uses Bootstrap 5 and Font Awesome (loaded from CDN)

## Troubleshooting

**Frontend shows "API Offline":**
1. Make sure backend is running (`python run.py`)
2. Check that backend is on `http://127.0.0.1:8000`
3. Check browser console for CORS errors

**Can't add data:**
1. Check API status indicator
2. Make sure all form fields are filled
3. Check browser console for errors

**Data not showing:**
1. Click the "Refresh" buttons
2. Check if backend database has data
3. Visit `http://127.0.0.1:8000/debug/db-status` directly
