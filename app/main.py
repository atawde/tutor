from fastapi import FastAPI
from .routes.admin import router as admin_router
from .routes.student import router as student_router
from .routes.auth import router as auth_router
from .routes.home import router as home_router
from .routes.setup_seed import router as seed_admin_router  
from .db.base import Base
from .db.session import engine

from fastapi.staticfiles import StaticFiles

# IMPORTANT: create tables ON START
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Textbook Narrator")
app.mount("/audio", StaticFiles(directory="output/audio"), name="audio")
app.include_router(admin_router)
app.include_router(student_router)
app.include_router(auth_router)
app.include_router(home_router)
app.include_router(seed_admin_router)
# app.include_router(jobs_router)


# uvicorn app.main:app --reload (from tutor folder, not from app folder and start venv before)
# http://127.0.0.1:8000/admin
"""
sqlite3 app.db
Class : Subject ; Table : subjects ; fields : id, name, lesson
Class : ProcessingJob ; Table : processing_jobs ; fields : id, subject_id, pdf_path, status
Class : AudioLesson ; Table : audio_lessons ; fields : id, subject_id, chapter_title, audio_url, narration_text
Class : User ; Table : users ; fields : id, name, email, role, hashed_password, is_active

Potential : Vedantu (https://www.vedantu.com/) or 
            Byju's (https://byjus.com/) for AI-based learning platforms, 
            but they are more focused on live classes and interactive learning rather than 
            automated content generation from textbooks.

Based on my experience, expect questions like:
1. Does it work for Hindi medium?
2.Can it support CBSE as well as State Boards?
3. How long does it take to generate one book?
4. Can teachers edit the narration?
5. Can students bookmark sections?
6. Can we integrate it with our LMS?
Be ready with answers—even if some are "planned for the roadmap."
"""

