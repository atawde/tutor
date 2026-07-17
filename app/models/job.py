from sqlalchemy import Column, Integer, String, Text
from ..db.base import Base

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(Integer, primary_key=True)

    subject_id = Column(Integer, nullable=False)
#    lesson_id = Column(Integer, nullable=False)
    pdf_path = Column(String, nullable=False)

    status = Column(String, default="pending")
    logs = Column(Text, nullable=True)