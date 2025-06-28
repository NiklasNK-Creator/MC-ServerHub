import time
from mcstatus import MinecraftServer
from database import SessionLocal
from models import Server
from datetime import datetime

def update_player_counts():
    db = SessionLocal()
    servers = db.query(Server).all()
    for server in servers:
        try:
            mc = MinecraftServer.lookup(server.ip)
            status = mc.status()
            server.players = status.players.online
            server.max_players = status.players.max
            server.last_ping = datetime.utcnow()
            print(f"Updated {server.name}: {server.players}/{server.max_players}")
        except Exception as e:
            print(f"Failed to ping {server.ip}: {e}")
    db.commit()
    db.close()

if __name__ == "__main__":
    while True:
        update_player_counts()
        time.sleep(300)  # alle 5 Minuten
