from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.controllers.userController import UserController
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Crear un nuevo usuario
    
    - **username**: Nombre de usuario único
    - **email**: Email único del usuario
    - **full_name**: Nombre completo
    - **phone**: Teléfono único
    - **password**: Contraseña del usuario
    """
    controller = UserController(db)
    return await controller.create_user(user_data)

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener lista de usuarios con paginación
    
    - **skip**: Número de usuarios a saltar (para paginación)
    - **limit**: Número máximo de usuarios a retornar
    """
    controller = UserController(db)
    return await controller.get_all_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtener un usuario específico por ID
    
    - **user_id**: ID del usuario a buscar
    """
    controller = UserController(db)
    user = await controller.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_data: UserUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar un usuario existente
    
    - **user_id**: ID del usuario a actualizar
    - **user_data**: Datos del usuario a actualizar (campos opcionales)
    """
    controller = UserController(db)
    return await controller.update_user(user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Eliminar un usuario (soft delete)
    
    - **user_id**: ID del usuario a eliminar
    """
    controller = UserController(db)
    await controller.delete_user(user_id)
    return None

@router.post("/login")
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Autenticar usuario y obtener token de acceso
    
    - **username**: Nombre de usuario
    - **password**: Contraseña del usuario
    """
    controller = UserController(db)
    return await controller.login_user(login_data)

@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    """
    Obtener usuario por nombre de usuario
    
    - **username**: Nombre de usuario a buscar
    """
    controller = UserController(db)
    user = await controller.get_user_by_username_response(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user
