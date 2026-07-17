from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..dependencies import get_current_user

import os
import uuid

from ..workers.pipeline_worker import process_chapter
from ..models.audio_lesson import AudioLesson
from ..db.deps import get_db
from ..models.job import ProcessingJob
from ..models.subject import Subject

router = APIRouter()

UPLOAD_DIR = "app/output"

templates = Jinja2Templates(directory="app/templates")

@router.get("/student")
def student_home(request: Request,
    user=Depends(get_current_user)
    ):

    return templates.TemplateResponse(
        request=request,
        name="student.html"
    )

@router.get("/student/subjects")
def list_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    return subjects

@router.get("/student/lessons/{subject_id}")
def list_lessons(subject_id: int, db: Session = Depends(get_db)):
    print("🔥 Fetching lessons from database")

    jobs = db.query(AudioLesson).filter(
        AudioLesson.subject_id == subject_id
        ).all()

    return jobs