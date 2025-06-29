from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from init_admin import create_admin
import auth, servers, admin
from database import create_tables

# Zuerst die Tabellen erstellen
create_tables()

# Dann den Admin erstellen (nachdem die Tabellen sicher existieren)
create_admin()

# FastAPI-Instanz
app = FastAPI(title="Minecraft Serverlist API")

# CORS-Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router einbinden
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(servers.router, prefix="/servers", tags=["Servers"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

# Root-Endpunkt
@app.get("/")
def root():
    return {"message": "Serverlist API is running."}
