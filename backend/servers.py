from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Server, Vote, User
from typing import List, Optional
import shutil
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

UPLOAD_FOLDER = "backend/static/banners"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy decode token, replace mit echter JWT Logik
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user_id = int(token)  # nur Platzhalter, nicht produktiv!
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid auth token")
    return user

@router.post("/upload")
async def upload_server(
    name: str = Form(...),
    description: str = Form(""),
    ip: str = Form(...),
    tags: str = Form(""),
    banner: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Banner speichern
    banner_path = os.path.join(UPLOAD_FOLDER, banner.filename)
    with open(banner_path, "wb") as buffer:
        shutil.copyfileobj(banner.file, buffer)

    server = Server(
        name=name,
        description=description,
        ip=ip,
        tags=tags,
        banner_url=f"/static/banners/{banner.filename}",
        uploader_id=current_user.id,
        likes=0,
        dislikes=0,
        players=0,
        max_players=0
    )
    db.add(server)
    db.commit()
    return {"msg": "Server uploaded"}

@router.get("/")
def list_servers(
    sort_by: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Server)
    if tag:
        query = query.filter(Server.tags.ilike(f"%{tag}%"))
    if sort_by == "likes":
        query = query.order_by(Server.likes.desc())
    elif sort_by == "dislikes":
        query = query.order_by(Server.dislikes.desc())
    elif sort_by == "players":
        query = query.order_by(Server.players.desc())
    else:
        query = query.order_by(Server.id.desc())

    servers = query.all()
    return servers

@router.post("/vote")
def vote_server(
    server_id: int,
    vote_type: str,  # "like" oder "dislike"
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if vote_type not in ("like", "dislike"):
        raise HTTPException(status_code=400, detail="Invalid vote type")

    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    existing_vote = db.query(Vote).filter(Vote.server_id == server_id, Vote.user_id == current_user.id).first()
    if existing_vote:
        # Wenn gleiche Stimme, nix machen
        if existing_vote.vote_type == vote_type:
            return {"msg": "Already voted"}
        # Stimme ändern
        if existing_vote.vote_type == "like":
            server.likes -= 1
        else:
            server.dislikes -= 1
        existing_vote.vote_type = vote_type
    else:
        # Neue Stimme
        new_vote = Vote(user_id=current_user.id, server_id=server_id, vote_type=vote_type)
        db.add(new_vote)

    if vote_type == "like":
        server.likes += 1
    else:
        server.dislikes += 1

    db.commit()
    return {"msg": "Vote counted"}
