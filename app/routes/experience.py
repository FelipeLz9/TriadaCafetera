from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.controllers.experienceController import ExperienceController
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse, ExperienceWithUser

router = APIRouter(prefix="/experiences", tags=["experiences"])

@router.post("/", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def create_experience(experience_data: ExperienceCreate, db: AsyncSession = Depends(get_db)):
    """
    Crear una nueva experiencia
    
    - **title**: Título único de la experiencia
    - **description**: Descripción detallada
    - **schedule**: Horario de la experiencia
    - **duration**: Duración en minutos
    - **price**: Precio de la experiencia
    - **location**: Ubicación donde se realiza
    - **user_id**: ID del usuario que crea la experiencia
    """
    controller = ExperienceController(db)
    return await controller.create_experience(experience_data)

@router.get("/", response_model=List[ExperienceResponse])
async def get_experiences(
    skip: int = Query(0, ge=0, description="Número de experiencias a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de experiencias a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener lista de experiencias con paginación
    
    - **skip**: Número de experiencias a saltar (para paginación)
    - **limit**: Número máximo de experiencias a retornar
    """
    controller = ExperienceController(db)
    return await controller.get_all_experiences(skip=skip, limit=limit)

@router.get("/{experience_id}", response_model=ExperienceResponse)
async def get_experience(experience_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtener una experiencia específica por ID
    
    - **experience_id**: ID de la experiencia a buscar
    """
    controller = ExperienceController(db)
    experience = await controller.get_experience_by_id(experience_id)
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiencia no encontrada"
        )
    return experience

@router.get("/{experience_id}/with-user", response_model=ExperienceWithUser)
async def get_experience_with_user(experience_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtener una experiencia con información del usuario
    
    - **experience_id**: ID de la experiencia a buscar
    """
    controller = ExperienceController(db)
    experience = await controller.get_experience_with_user(experience_id)
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiencia no encontrada"
        )
    return experience

@router.put("/{experience_id}", response_model=ExperienceResponse)
async def update_experience(
    experience_id: int, 
    experience_data: ExperienceUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar una experiencia existente
    
    - **experience_id**: ID de la experiencia a actualizar
    - **experience_data**: Datos de la experiencia a actualizar (campos opcionales)
    """
    controller = ExperienceController(db)
    return await controller.update_experience(experience_id, experience_data)

@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(experience_id: int, db: AsyncSession = Depends(get_db)):
    """
    Eliminar una experiencia
    
    - **experience_id**: ID de la experiencia a eliminar
    """
    controller = ExperienceController(db)
    await controller.delete_experience(experience_id)
    return None

@router.get("/user/{user_id}", response_model=List[ExperienceResponse])
async def get_experiences_by_user(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de experiencias a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de experiencias a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener experiencias de un usuario específico
    
    - **user_id**: ID del usuario
    - **skip**: Número de experiencias a saltar (para paginación)
    - **limit**: Número máximo de experiencias a retornar
    """
    controller = ExperienceController(db)
    return await controller.get_experiences_by_user(user_id, skip=skip, limit=limit)

@router.get("/location/{location}", response_model=List[ExperienceResponse])
async def get_experiences_by_location(
    location: str,
    skip: int = Query(0, ge=0, description="Número de experiencias a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de experiencias a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener experiencias por ubicación
    
    - **location**: Ubicación a buscar (búsqueda parcial)
    - **skip**: Número de experiencias a saltar (para paginación)
    - **limit**: Número máximo de experiencias a retornar
    """
    controller = ExperienceController(db)
    return await controller.get_experiences_by_location(location, skip=skip, limit=limit)

@router.get("/price/range", response_model=List[ExperienceResponse])
async def get_experiences_by_price_range(
    min_price: int = Query(..., ge=0, description="Precio mínimo"),
    max_price: int = Query(..., ge=0, description="Precio máximo"),
    skip: int = Query(0, ge=0, description="Número de experiencias a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de experiencias a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener experiencias por rango de precio
    
    - **min_price**: Precio mínimo
    - **max_price**: Precio máximo
    - **skip**: Número de experiencias a saltar (para paginación)
    - **limit**: Número máximo de experiencias a retornar
    """
    if min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio mínimo no puede ser mayor al precio máximo"
        )
    
    controller = ExperienceController(db)
    return await controller.get_experiences_by_price_range(min_price, max_price, skip=skip, limit=limit)

@router.get("/search/{query}", response_model=List[ExperienceResponse])
async def search_experiences(
    query: str,
    skip: int = Query(0, ge=0, description="Número de experiencias a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de experiencias a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Buscar experiencias por título o descripción
    
    - **query**: Término de búsqueda
    - **skip**: Número de experiencias a saltar (para paginación)
    - **limit**: Número máximo de experiencias a retornar
    """
    controller = ExperienceController(db)
    return await controller.search_experiences(query, skip=skip, limit=limit)
