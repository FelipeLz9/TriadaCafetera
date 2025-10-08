from fastapi import FastAPI
from controllers import profileController
from database import Base, engine

# Crear las tablas en la base de datos (solo la primera vez)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar el router del perfil
app.include_router(profileController.router)

@app.get("/")
def root():
    return {"message": "API de perfiles funcionando correctamente 🚀"}
