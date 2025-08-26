# AI Exam Platform - API Documentation

## Base URL
`http://localhost:8000/api/`

## Authentication
All endpoints (except registration and login) require session authentication. Frontend must include credentials with requests.

## Endpoints

### 1. User Registration
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

### 2. User Login
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

### 3. User Logout
**POST** `/auth/logout/`

Terminates the user session.

**Response (Success - 200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

### 4. Get Current User Profile
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

### 2. Login Example
```javascript
// pages/login.js
import API from '../lib/axios';

const handleLogin = async (email, password) => {
  try {
    const response = await API.post('/auth/login/', {
      email,
      password
    });
    console.log('Login successful:', response.data);
    // Redirect to dashboard
  } catch (error) {
    console.error('Login failed:', error.response?.data);
  }
};
```

### 3. Get Profile Example
```javascript
// pages/dashboard.js
import { useEffect, useState } from 'react';
import API from '../lib/axios';

const Dashboard = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await API.get('/profile/me/');
        setProfile(response.data);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
        // Redirect to login if unauthorized
      }
    };
    fetchProfile();
  }, []);

  return (
    <div>
      {profile && (
        <h1>Welcome, {profile.user.first_name}!</h1>
      )}
    </div>
  );
};
```

---

## Error Responses

### 400 Bad Request
```json
{
  "email": ["This field is required."],
  "password": ["This field is required."]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error occurred."
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
- Database uses SQLite for development
- Session-based authentication with Django sessions
