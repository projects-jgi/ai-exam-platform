# AI Exam Platform - API Documentation

## Base URL
`http://localhost:8000/api/`

## Authentication
All endpoints (except registration and login) require session authentication. Frontend must include credentials with requests.

## Endpoints

### 1. User Authentication

#### User Registration
**POST** `/auth/register/`

Creates a new user and automatically creates corresponding profile.

**Request Body:**
```json
{
  "email": "student@jainuniversity.ac.in",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "student"
}
```

**Response (Success - 201 Created):**
```json
{
  "message": "User created successfully. Please log in.",
  "user_id": 4,
  "user_type": "student"
}
```

**User Types:** `student`, `faculty`, `hod`, `admin`

---

#### User Login
**POST** `/auth/login/`

Authenticates user and creates session.

**Request Body:**
```json
{
  "email": "student@jainuniversity.ac.in",
  "password": "securepassword123"
}
```

**Response (Success - 200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 4,
    "email": "student@jainuniversity.ac.in",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "student"
  }
}
```

---

#### User Logout
**POST** `/auth/logout/`

Terminates the user session.

**Response (Success - 200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

#### Get Current User Profile
**GET** `/profile/me/`

Returns complete profile information for authenticated user.

**Response (Success - 200 OK):**
```json
{
  "user": {
    "id": 4,
    "email": "student@jainuniversity.ac.in",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "student"
  },
  "profile": {
    "user": {
      "id": 4,
      "email": "student@jainuniversity.ac.in",
      "first_name": "John",
      "last_name": "Doe",
      "user_type": "student"
    },
    "group": null,
    "student_id": "STU0004",
    "is_active": true
  }
}
```

---

### 2. Exam Management

#### List Available Exams
**GET** `/exams/`

Returns exams available to the current user based on their role and group.

**Response (Student - 200 OK):**
```json
[
  {
    "id": 3,
    "title": "MCA Semester 3 Final Exam",
    "description": "End of semester examination",
    "created_by": 1,
    "created_by_name": "Professor Smith",
    "start_time": "2025-08-28T07:00:00+05:30",
    "end_time": "2025-08-28T08:00:00+05:30",
    "duration_minutes": 60,
    "max_attempts": 1,
    "shuffle_questions": false,
    "show_results_after": false,
    "is_proctored": true,
    "status": "active",
    "questions": [],
    "created_at": "2025-08-27T21:47:52.645527+05:30",
    "updated_at": "2025-08-27T21:47:52.645527+05:30"
  }
]
```

---

#### Get Exam Details
**GET** `/exams/{id}/`

Returns detailed information about a specific exam.

**Response (200 OK):**
```json
{
  "id": 3,
  "title": "MCA Semester 3 Final Exam",
  "description": "End of semester examination",
  "created_by": 1,
  "created_by_name": "Professor Smith",
  "start_time": "2025-08-28T07:00:00+05:30",
  "end_time": "2025-08-28T08:00:00+05:30",
  "duration_minutes": 60,
  "max_attempts": 1,
  "shuffle_questions": false,
  "show_results_after": false,
  "is_proctored": true,
  "status": "active",
  "questions": [
    {
      "id": 1,
      "exam": 3,
      "question_text": "What is Python?",
      "question_type": "descriptive",
      "points": 10,
      "order": 1,
      "code_template": "",
      "test_cases": null,
      "options": [],
      "created_at": "2025-08-27T21:50:12.645527+05:30"
    }
  ],
  "created_at": "2025-08-27T21:47:52.645527+05:30",
  "updated_at": "2025-08-27T21:47:52.645527+05:30"
}
```

---

#### Start Exam Attempt
**POST** `/exams/{exam_id}/start/`

Starts a new exam attempt for the authenticated student.

**Response (Success - 200 OK):**
```json
{
  "attempt_id": 1,
  "message": "Exam started successfully",
  "duration_minutes": 60
}
```

---

### 3. Exam Attempt Management

#### Get Attempt Details
**GET** `/attempts/{attempt_id}/`

Returns detailed information about a specific exam attempt.

**Response (200 OK):**
```json
{
  "id": 1,
  "student": 6,
  "student_name": "Rahul M",
  "exam": 3,
  "attempt_number": 1,
  "start_time": "2025-08-31T20:25:37.771491+05:30",
  "end_time": null,
  "actual_duration": null,
  "violation_count": 0,
  "screen_switch_count": 0,
  "status": "in_progress",
  "score": null,
  "max_score": null,
  "answers": [
    {
      "id": 1,
      "attempt": 1,
      "question": 1,
      "mcq_answer": null,
      "descriptive_answer": "Python is a programming language...",
      "code_answer": "",
      "file_answer": null,
      "points_awarded": 10.0,
      "feedback": "Good answer!",
      "submitted_at": "2025-08-31T20:36:46.966120+05:30"
    }
  ]
}
```

---

#### Submit Answer
**POST** `/attempts/{attempt_id}/submit/`

Submits an answer for a question in an ongoing exam attempt.

**Request Body:**
```json
{
  "question_id": 1,
  "answer": "Python is a high-level programming language...",
  "answer_type": "descriptive"
}
```

**Response (Success - 200 OK):**
```json
{
  "message": "Answer submission received",
  "attempt_id": 1,
  "status": "Answer processing will be implemented soon"
}
```

---

#### Complete Exam Attempt
**POST** `/attempts/{attempt_id}/complete/`

Marks an exam attempt as completed and calculates final duration.

**Response (Success - 200 OK):**
```json
{
  "message": "Exam completed successfully",
  "score": 85.5,
  "duration_minutes": 58
}
```

---

## Frontend Integration Guide

### 1. Axios Configuration
```javascript
// lib/axios.js
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true, // ESSENTIAL for session cookies
});

export default API;
```

### 2. Complete Exam Flow Example
```javascript
// Example of complete exam flow
const completeExamFlow = async (examId) => {
  try {
    // 1. Start exam attempt
    const startResponse = await API.post(`/exams/${examId}/start/`);
    const attemptId = startResponse.data.attempt_id;
    
    // 2. Submit answers
    await API.post(`/attempts/${attemptId}/submit/`, {
      question_id: 1,
      answer: "Python is a programming language...",
      answer_type: "descriptive"
    });
    
    // 3. Complete attempt
    const completeResponse = await API.post(`/attempts/${attemptId}/complete/`);
    console.log('Exam completed:', completeResponse.data);
    
  } catch (error) {
    console.error('Exam error:', error.response?.data);
  }
};
```

### 3. Get Exam Attempts Example
```javascript
// Get student's exam attempts
const getStudentAttempts = async () => {
  try {
    const response = await API.get('/attempts/'); // This endpoint needs implementation
    return response.data;
  } catch (error) {
    console.error('Failed to fetch attempts:', error);
  }
};
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Exam is not available at this time"
}
```

### 403 Forbidden
```json
{
  "error": "You are not allowed to take this exam"
}
```

### 404 Not Found
```json
{
  "error": "Exam not found"
}
```

### 409 Conflict
```json
{
  "error": "Maximum attempts reached for this exam"
}
```

---

## CORS Configuration
Backend is configured to accept requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

---

## Request Headers
For authenticated requests, include:
- `Content-Type: application/json`
- Session cookies (automatically handled by browser with `withCredentials: true`)

---

## Development Notes
- Backend runs on port 8000
- Frontend should run on port 3000 for CORS compatibility
- Database: PostgreSQL with complete schema
- Session-based authentication with Django sessions
- CSRF protection enabled (include X-CSRFToken header for POST requests)
