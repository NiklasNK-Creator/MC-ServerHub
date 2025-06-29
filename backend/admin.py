from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Server

router = APIRouter()

# Server löschen
@router.delete("/server/{server_id}")
def delete_server(server_id: int):
    db: Session = SessionLocal()
    server = db.query(Server).filter(Server.id == server_id).first()

    if not server:
        raise HTTPException(status_code=404, detail="Server nicht gefunden")

    db.delete(server)
    db.commit()
    return {"message": "Server gelöscht"}
