from fastapi import FastAPI
<<<<<<< HEAD
from app.routes import user
from app.routes.booking import router as booking_router
from app.controllers import clientController, profileController
=======
from app.routes import user, experience, auth
>>>>>>> origin/Feature/auth-endpoint
from app.database import create_tables

app = FastAPI(
    title="Triada Cafetera API",
    description="API para la gestión de usuarios, fincas cafeteras, experiencias y reservas",
    version="1.0.0"
)

# Incluir todas las rutas
app.include_router(user.router)
<<<<<<< HEAD
app.include_router(clientController.router)
app.include_router(booking_router)
app.include_router(profileController.router)
=======
app.include_router(experience.router)
app.include_router(auth.router)
>>>>>>> origin/Feature/auth-endpoint

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    await create_tables()

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a Triada Cafetera API",
        "version": "1.0.0",
        "docs": "/docs",
<<<<<<< HEAD
        "redoc": "/redoc"
=======
        "endpoints": {
            "users": "/users",
            "experiences": "/experiences",
            "auth": "/auth"
        }
>>>>>>> origin/Feature/auth-endpoint
    }

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {"status": "healthy", "message": "API funcionando correctamente"}
