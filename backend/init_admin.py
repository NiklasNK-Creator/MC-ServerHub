import os
import bcrypt
from database import SessionLocal
from models import User

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Klartext → wird gleich gehasht

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_admin():
    db = SessionLocal()
    existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if not existing:
        hashed_pw = hash_password(ADMIN_PASSWORD)
        new_admin = User(email=ADMIN_EMAIL, hashed_password=hashed_pw, is_admin=True)
        db.add(new_admin)
        db.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin already exists.")
    db.close()
