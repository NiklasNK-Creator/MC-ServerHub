from database import SessionLocal
from models import User
from passlib.hash import bcrypt

# Admin-Daten
ADMIN_EMAIL = "schoneniklas79@gmail.com"
ADMIN_PASSWORD = "AresLuna1"

db = SessionLocal()

# Check ob Admin schon existiert
existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
if not existing:
    admin = User(
        email=ADMIN_EMAIL,
        hashed_password=bcrypt.hash(ADMIN_PASSWORD),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print("✅ Admin wurde angelegt.")
else:
    print("ℹ️ Admin existiert schon.")

db.close()
