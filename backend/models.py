ffrom sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    ip = Column(String, nullable=False)
    banner_url = Column(String)
    tags = Column(String)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    uploader = relationship("User")
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    players = Column(Integer, default=0)
    max_players = Column(Integer, default=0)
    last_ping = Column(DateTime, default=datetime.utcnow)

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    server_id = Column(Integer, ForeignKey("servers.id"))
    vote_type = Column(String)  # 'like' oder 'dislike'
