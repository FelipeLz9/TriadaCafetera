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

from fastapi import FastAPI
from database import Base, engine
from controllers import profileController

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Instancia principal de FastAPI
app = FastAPI(
    title="API de Perfiles",
    description="API para gestionar perfiles de usuario (ProfileController)",
    version="1.0.0"
)

# Incluir el router del controlador de perfiles
app.include_router(profileController.router)

# Endpoint raíz para verificar que el servidor funciona
@app.get("/")
def root():
    return {"message": "🚀 API de Perfiles funcionando correctamente"}
