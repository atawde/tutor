from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)