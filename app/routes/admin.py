from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import os
import uuid

from ..workers.pipeline_worker import process_chapter
from ..models.audio_lesson import AudioLesson
from ..db.deps import get_db
from ..models.job import ProcessingJob
from ..models.subject import Subject
from ..models.lesson import Lesson
from ..models.user import User
from ..dependencies import get_current_user


router = APIRouter()

UPLOAD_DIR = "output/pdf"

templates = Jinja2Templates(directory="app/templates")

@router.get("/admin")
def admin_home(request: Request,
    user=Depends(get_current_user)):

    result = templates.TemplateResponse(
            request=request,
            name="admin.html",
            context={} 
    )
    return result


@router.post("/admin/upload-pdf")
def upload_pdf(
    background_tasks: BackgroundTasks,
    subject_name: str = Form(...),
    lesson_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    subject = Subject(
        name=subject_name,
        lesson=lesson_name
    )


    db.add(subject)
    db.commit()
    db.refresh(subject)

    job = ProcessingJob(  
        subject_id=subject.id,
        pdf_path=file_path,
        status="uploaded"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # schedule background task using the BackgroundTasks instance
    background_tasks.add_task(process_chapter, job.id)

    return {
        "job_id": job.id,
        "status": job.status
    }

@router.get("/admin/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(ProcessingJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/admin/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(ProcessingJob).all()

@router.get("/admin/lessons")
def list_lessons(db: Session = Depends(get_db)):
    results = (
    db.query(
        AudioLesson.id,
        Subject.name,
        Subject.lesson,
        AudioLesson.audio_url
    )
    .join(AudioLesson, AudioLesson.subject_id == Subject.id)
    .order_by(Subject.name, Subject.lesson)
    .all()
)

    return [
    {
        "id": row.id,
        "subject": row.name,
        "lesson": row.lesson,
        "audio_url": row.audio_url
    }
    for row in results
]
