from app.security import hash_password
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

users = [
    {
        "name": "Administrator",
        "email": "admin@tutor24x7.com",
        "password": "admin123",
        "role": "admin",
    },
    {
        "name": "Student",
        "email": "student@example.com",
        "password": "student123",
        "role": "student",
    },
]

for u in users:
    existing = db.query(User).filter(User.email == u["email"]).first()

    if existing:
        print(f"{u['email']} already exists")
        continue

    db.add(
        User(
            name=u["name"],
            email=u["email"],
            password_hash=hash_password(u["password"]),
            role=u["role"],
            is_active=True,
        )
    )

db.commit()
print("Seed completed.")
db.close()
