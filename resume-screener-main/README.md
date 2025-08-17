# AI Resume Screening Tool - Django Backend

This is the backend for the AI Resume Screening Tool, built with Django and Django Rest Framework.
This version includes AI logic for scoring resumes based on job descriptions.

## Project Structure

- `resume_screener/`: The main Django project folder.
- `api/`: The Django app for our API.
  - `ai_logic.py`: Core AI functions for text extraction and similarity scoring.
  - `models.py`: Database models.
  - `serializers.py`: Data serializers.
  - `views.py`: API endpoint logic.
  - `urls.py`: App-level URL routing.
- `requirements.txt`: Python dependencies.
- `manage.py`: Django's command-line utility.

## Setup Instructions

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: The first time you run the application, the `sentence-transformers` model will be downloaded. This may take a few minutes.*

3. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints

- `POST /api/register/` - Register a new user
- `POST /api/token/` - Get JWT access token
- `POST /api/token/refresh/` - Refresh JWT token
- `GET/POST /api/jobs/` - List and create job descriptions
- `GET/PUT/DELETE /api/jobs/<id>/` - Get, update, or delete a job description
- `POST /api/jobs/<job_id>/upload/` - Upload resumes for a job

## Features

- JWT authentication
- Resume file upload (PDF, DOCX)
- AI-powered resume scoring using sentence transformers
- Job description management
- Resume scoring and ranking 