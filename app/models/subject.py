from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    lesson = Column(String)