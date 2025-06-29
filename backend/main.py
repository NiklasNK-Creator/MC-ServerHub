from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
import auth, servers, admin  # Deine Router

# ⚠️ ZUERST die Tabellen erstellen
create_tables()

# ⚠️ DANACH den Admin erstellen
from init_admin import create_admin
create_admin()

app = FastAPI(title="Minecraft Serverlist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # bei Bedarf anpassen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(servers.router, prefix="/servers", tags=["Servers"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Serverlist API is running."}
