from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.database import get_db
from app.controllers.authController import AuthController
from app.schemas.auth import (
    LoginRequest, RegisterRequest, Token, UserProfile,
    PasswordResetRequest, PasswordResetConfirm, ChangePasswordRequest
)
from app.utils.middleware import get_current_user_required

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Registrar un nuevo usuario
    
    - **username**: Nombre de usuario único
    - **email**: Email único del usuario
    - **full_name**: Nombre completo
    - **phone**: Teléfono único
    - **password**: Contraseña del usuario
    """
    controller = AuthController(db)
    return await controller.register_user(user_data)

@router.post("/login", response_model=dict)
async def login(
    login_data: LoginRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Autenticar usuario y obtener token de acceso
    
    - **username**: Nombre de usuario
    - **password**: Contraseña del usuario
    """
    controller = AuthController(db)
    return await controller.login_user(login_data)

@router.post("/logout", response_model=dict)
async def logout(
    current_user: UserProfile = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    """
    Cerrar sesión del usuario actual
    
    Requiere autenticación.
    """
    controller = AuthController(db)
    return await controller.logout_user(current_user)

@router.post("/refresh", response_model=dict)
async def refresh_token(
    current_user: UserProfile = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    """
    Refrescar token de acceso
    
    Requiere autenticación.
    """
    controller = AuthController(db)
    return await controller.refresh_token(current_user)

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: UserProfile = Depends(get_current_user_required)
):
    """
    Obtener perfil del usuario actual
    
    Requiere autenticación.
    """
    return current_user

@router.put("/me", response_model=UserProfile)
async def update_user_profile(
    profile_data: dict,
    current_user: UserProfile = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar perfil del usuario actual
    
    Campos permitidos: full_name, phone
    
    Requiere autenticación.
    """
    controller = AuthController(db)
    return await controller.update_user_profile(profile_data, current_user)

@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: UserProfile = Depends(get_current_user_required),
    db: AsyncSession = Depends(get_db)
):
    """
    Cambiar contraseña del usuario actual
    
    - **current_password**: Contraseña actual
    - **new_password**: Nueva contraseña
    
    Requiere autenticación.
    """
    controller = AuthController(db)
    return await controller.change_password(password_data, current_user)

@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    reset_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Solicitar restablecimiento de contraseña
    
    - **email**: Email del usuario
    
    En un entorno real, se enviaría un email con el enlace de restablecimiento.
    """
    controller = AuthController(db)
    return await controller.request_password_reset(reset_data)

@router.post("/reset-password", response_model=dict)
async def reset_password(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """
    Confirmar restablecimiento de contraseña
    
    - **token**: Token de restablecimiento recibido por email
    - **new_password**: Nueva contraseña
    """
    controller = AuthController(db)
    return await controller.confirm_password_reset(reset_data)

@router.get("/verify-token", response_model=dict)
async def verify_token_endpoint(
    current_user: UserProfile = Depends(get_current_user_required)
):
    """
    Verificar si el token es válido
    
    Requiere autenticación.
    """
    return {
        "valid": True,
        "message": "Token válido",
        "user": current_user
    }

@router.get("/status", response_model=dict)
async def auth_status():
    """
    Verificar estado del servicio de autenticación
    """
    return {
        "status": "active",
        "message": "Servicio de autenticación funcionando correctamente",
        "endpoints": {
            "register": "/auth/register",
            "login": "/auth/login",
            "logout": "/auth/logout",
            "refresh": "/auth/refresh",
            "profile": "/auth/me",
            "change_password": "/auth/change-password",
            "forgot_password": "/auth/forgot-password",
            "reset_password": "/auth/reset-password"
        }
    }
