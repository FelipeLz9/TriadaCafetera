from fastapi import FastAPI
from app.database import Base, engine
from app.controllers import clientController
from app.routes.booking import router as booking_router

app = FastAPI(
    title="Sistema de Reservas - API",
    description="API para gestión de reservas de fincas",
    version="1.0.0"
)

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
