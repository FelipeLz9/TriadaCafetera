from fastapi import FastAPI
from app.database import Base, engine
from app.routes import client

app = FastAPI(title="Triada Cafetera API")

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Registrar los routers
app.include_router(client.router)
