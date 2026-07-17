from sqlalchemy import Column, Integer, String, Text  # type: ignore
from ..db.base import Base

class AudioLesson(Base):
    __tablename__ = "audio_lessons"

    id = Column(Integer, primary_key=True)

    subject_id = Column(Integer)
    chapter_title = Column(String)

    audio_url = Column(String)
    narration_text = Column(Text)