from fastapi import FastAPI
from app.routes.booking import router as booking_router

app = FastAPI(
    title="Sistema de Reservas - API",
    description="API para gestión de reservas de fincas",
    version="1.0.0"
)

# Registrar rutas
app.include_router(booking_router)

@app.get("/")
def read_root():
    return {
        "message": "API del Sistema de Reservas",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
