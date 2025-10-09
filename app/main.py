from fastapi import FastAPI
from app.database import Base, engine
from app.controllers import clientController

app = FastAPI(title="Triada Cafetera API")

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Registrar el router del endpoint
app.include_router(clientController.router)
