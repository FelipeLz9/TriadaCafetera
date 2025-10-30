from fastapi import FastAPI
from app.routes import user
from app.routes.booking import router as booking_router
from app.controllers import clientController, profileController
from app.database import create_tables

app = FastAPI(
    title="Triada Cafetera API",
    description="API para la gestión de usuarios, fincas cafeteras, experiencias y reservas",
    version="1.0.0"
)

# Incluir todas las rutas
app.include_router(user.router)
app.include_router(clientController.router)
app.include_router(booking_router)
app.include_router(profileController.router)

@app.on_event("startup")
def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    create_tables()

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Triada Cafetera API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {"status": "healthy", "message": "API funcionando correctamente"}
