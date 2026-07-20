from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.security import hash_password

router = APIRouter()

@router.get("/setup-admin")
def setup_admin():

    db: Session = SessionLocal()

    try:
            existing_user = db.query(User).filter(
                User.name == "Administrator"
            ).first()

            if not existing_user:
                admin = User(
                   name="Administrator",
                   email="admin@tutor24x7.com",
                   password_hash=hash_password("admin123"),
                   role="admin"
                )
            
                db.add(admin)
                db.commit()
            
            existing_user = db.query(User).filter(
                User.name == "Student"
            ).first()

            if not existing_user:
                student = User(
                    name="Student",
                    email="student@tutor24x7.com",
                    password_hash=hash_password("student123"),
                    role="student"
                )
                db.add(student)
                db.commit()
                
            return {"message": "Admin and student created successfully"}

    finally:
        db.close()
