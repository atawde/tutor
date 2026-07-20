from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.subject import Subject
from app.models.job import ProcessingJob
from app.models.audio_lesson import AudioLesson

router = APIRouter()


@router.get("/cleanup-db")
def cleanup_db():

    db: Session = SessionLocal()

    try:
        db.query(Subject).delete()
        db.query(AudioLesson).delete()
        db.query(ProcessingJob).delete()

        db.commit()
    finally:
        db.close()
        return {"message": "Database cleaned up successfully"}
