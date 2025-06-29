import os
from database import SessionLocal
from models import User

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # am besten vorher hashen

def create_admin():
    db = SessionLocal()
    existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if not existing:
        new_admin = User(email=ADMIN_EMAIL, hashed_password=ADMIN_PASSWORD, is_admin=True)
        db.add(new_admin)
        db.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin already exists.")
    db.close()
