from fastapi import FastAPI
from app.routes import user
from app.database import create_tables

app = FastAPI(
    title="Triada Cafetera API",
    description="API para la gestión de usuarios, fincas cafeteras y experiencias",
    version="1.0.0"
)

# Incluir las rutas
app.include_router(user.router)

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    await create_tables()

@app.get("/")
def read_root():
    return {
        "message": "API del Sistema de Reservas",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Registrar el router del endpoint
app.include_router(clientController.router)
app.include_router(booking_router)

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {"status": "healthy", "message": "API funcionando correctamente"}
