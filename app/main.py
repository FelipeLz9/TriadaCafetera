from fastapi import FastAPI
from app.database import create_tables
from app.routes import client
# Importar modelos para que se registren con Base
from app.models import *

app = FastAPI(title="Triada Cafetera API")

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Registrar los routers
app.include_router(client.router)

@app.on_event("startup")
async def startup_event():
    """Crear las tablas al iniciar la aplicación"""
    await create_tables()
