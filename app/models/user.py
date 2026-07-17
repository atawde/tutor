from sqlalchemy import Boolean, Column, Integer, String, Text
from ..db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    role = Column(String, default="student")

    is_active = Column(Boolean, default=True)
