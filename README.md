# AI-Powered Online Examination & Proctoring Platform

A secure online exam system with AI-based proctoring for Jain University MCA department.

## 🚀 Tech Stack

- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** College Email + Password + OTP (MFA)
- **Frontend:** Next.js + TailwindCSS
- **File Storage:** MinIO
- **DevOps:** Docker + Redis

## 🏗️ Project Structure
ai-exam-platform/
├── backend/ # Django project
├── core/ # Main app (users, profiles, auth)
├── venv/ # Virtual environment (ignored)
├── .env # Environment variables (ignored)
├── requirements.txt
├── manage.py
└── README.md

## ⚡ Quick Start
## 🎯 New Features Added

### Exam Management System
- ✅ **Exam Creation & Management** - Faculty can create exams with various settings
- ✅ **Student Exam Access** - Automatic enrollment based on student groups
- ✅ **Timed Exam Attempts** - Start, submit, and complete exams with duration tracking
- ✅ **Multiple Question Types** - Support for MCQ, coding, descriptive, and file upload questions
- ✅ **Answer Submission** - Students can submit answers with automatic tracking
- ✅ **Real-time Status Updates** - Track exam progress from in_progress to submitted

### API Endpoints Now Available
- `GET /api/exams/` - List available exams
- `GET /api/exams/{id}/` - Get exam details
- `POST /api/exams/{exam_id}/start/` - Start exam attempt
- `GET /api/attempts/{attempt_id}/` - View attempt details
- `POST /api/attempts/{attempt_id}/submit/` - Submit answers
- `POST /api/attempts/{attempt_id}/complete/` - Complete exam attempt

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/projects-jgi/ai-exam-platform.git
   cd ai-exam-platform
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   # Create your own .env file based on the existing .env file.
   # Ensure to update the database credentials and any other necessary configurations.
   ```

5. **Database Setup**
   ```sql
   CREATE DATABASE ai_exam_db;
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 📊 Database Schema
[Add your ER diagram here](https://docs/erd.png)

## 📝 API Documentation
See `API_DOCS.md` for detailed API endpoints and examples.

---

**Team Message:**
"Hi team! I've pushed the complete authentication API with detailed documentation. Please pull the latest code and check the `API_DOCS.md` file for integration instructions. The `README.md` has also been updated with setup guides. Let me know if you face any issues! 🚀"
