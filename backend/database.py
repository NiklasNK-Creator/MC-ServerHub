import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

def create_tables():
    from models import Base  # erst hier importieren, damit kein Zirkulärer Import entsteht
    Base.metadata.create_all(bind=engine)
