from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.controllers.profileController import ProfileController
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile_data: ProfileCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo perfil
    
    - **user_id**: ID del usuario al que pertenece el perfil
    - **address**: Dirección del usuario
    - **bio**: Descripción o biografía
    - **birthdate**: Fecha de nacimiento
    """
    controller = ProfileController(db)
    return controller.create_profile(profile_data)


@router.get("/", response_model=List[ProfileResponse])
def get_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de perfiles con paginación
    
    - **skip**: Número de perfiles a saltar (para paginación)
    - **limit**: Número máximo de perfiles a retornar
    """
    controller = ProfileController(db)
    return controller.get_all_profiles(skip=skip, limit=limit)


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Obtener un perfil específico por ID
    
    - **profile_id**: ID del perfil a buscar
    """
    controller = ProfileController(db)
    profile = controller.get_profile_by_id(profile_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    return profile


@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un perfil existente
    
    - **profile_id**: ID del perfil a actualizar
    - **profile_data**: Datos del perfil a actualizar
    """
    controller = ProfileController(db)
    return controller.update_profile(profile_id, profile_data)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un perfil (soft delete)
    
    - **profile_id**: ID del perfil a eliminar
    """
    controller = ProfileController(db)
    controller.delete_profile(profile_id)
    return None
