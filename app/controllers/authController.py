from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

from app.models.user import User
from app.schemas.auth import (
    LoginRequest, RegisterRequest, TokenData, UserProfile,
    PasswordResetRequest, PasswordResetConfirm, ChangePasswordRequest
)
from app.utils.auth import get_password_hash, verify_password, create_access_token, verify_token
from app.config import settings

security = HTTPBearer()

class AuthController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_data: RegisterRequest) -> Dict[str, Any]:
        """Registrar un nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            existing_user = await self._get_user_by_username(user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya existe"
                )
            
            existing_email = await self._get_user_by_email(user_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )

            # Crear el nuevo usuario
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                full_name=user_data.full_name,
                phone=user_data.phone,
                hashed_password=hashed_password,
                is_active=1
            )
            
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            
            # Generar token de acceso
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(
                data={"sub": db_user.username, "user_id": db_user.id},
                expires_delta=access_token_expires
            )
            
            return {
                "message": "Usuario registrado exitosamente",
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 1800,  # 30 minutos en segundos
                "user": UserProfile.from_orm(db_user)
            }
            
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad en la base de datos"
            )

    async def login_user(self, login_data: LoginRequest) -> Dict[str, Any]:
        """Autenticar usuario y generar token"""
        user = await self._authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        return {
            "message": "Login exitoso",
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,  # 30 minutos en segundos
            "user": UserProfile.from_orm(user)
        }

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserProfile:
        """Obtener usuario actual desde el token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            token = credentials.credentials
            payload = verify_token(token)
            if payload is None:
                raise credentials_exception
            
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            
            if username is None or user_id is None:
                raise credentials_exception
                
        except jwt.PyJWTError:
            raise credentials_exception
        
        user = await self._get_user_by_username(username)
        if user is None:
            raise credentials_exception
            
        if user.is_active != 1:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo"
            )
        
        return UserProfile.from_orm(user)

    async def refresh_token(self, current_user: UserProfile) -> Dict[str, Any]:
        """Refrescar token de acceso"""
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": current_user.username, "user_id": current_user.id},
            expires_delta=access_token_expires
        )
        
        return {
            "message": "Token refrescado exitosamente",
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,
            "user": current_user
        }

    async def change_password(self, password_data: ChangePasswordRequest, current_user: UserProfile) -> Dict[str, str]:
        """Cambiar contraseña del usuario actual"""
        user = await self._get_user_by_username(current_user.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not verify_password(password_data.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña actual es incorrecta"
            )
        
        # Actualizar contraseña
        new_hashed_password = get_password_hash(password_data.new_password)
        user.hashed_password = new_hashed_password
        await self.db.commit()
        
        return {"message": "Contraseña actualizada exitosamente"}

    async def request_password_reset(self, reset_data: PasswordResetRequest) -> Dict[str, str]:
        """Solicitar restablecimiento de contraseña"""
        user = await self._get_user_by_email(reset_data.email)
        if not user:
            # Por seguridad, no revelamos si el email existe o no
            return {"message": "Si el email existe, se enviará un enlace de restablecimiento"}
        
        # Generar token de restablecimiento (válido por 1 hora)
        reset_token_expires = timedelta(hours=1)
        reset_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "type": "password_reset"},
            expires_delta=reset_token_expires
        )
        
        # En un entorno real, aquí enviarías un email con el token
        # Por ahora, solo retornamos el mensaje
        return {
            "message": "Si el email existe, se enviará un enlace de restablecimiento",
            "reset_token": reset_token  # Solo para desarrollo/testing
        }

    async def confirm_password_reset(self, reset_data: PasswordResetConfirm) -> Dict[str, str]:
        """Confirmar restablecimiento de contraseña"""
        try:
            payload = verify_token(reset_data.token)
            if payload is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token inválido o expirado"
                )
            
            # Verificar que es un token de restablecimiento
            if payload.get("type") != "password_reset":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token inválido"
                )
            
            username = payload.get("sub")
            user_id = payload.get("user_id")
            
            if not username or not user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token inválido"
                )
            
            user = await self._get_user_by_username(username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Actualizar contraseña
            new_hashed_password = get_password_hash(reset_data.new_password)
            user.hashed_password = new_hashed_password
            await self.db.commit()
            
            return {"message": "Contraseña restablecida exitosamente"}
            
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido o expirado"
            )

    async def logout_user(self, current_user: UserProfile) -> Dict[str, str]:
        """Cerrar sesión del usuario"""
        # En un entorno real, aquí podrías invalidar el token en una blacklist
        # Por ahora, solo retornamos un mensaje de confirmación
        return {"message": "Sesión cerrada exitosamente"}

    async def get_user_profile(self, current_user: UserProfile) -> UserProfile:
        """Obtener perfil del usuario actual"""
        return current_user

    async def update_user_profile(self, profile_data: dict, current_user: UserProfile) -> UserProfile:
        """Actualizar perfil del usuario actual"""
        user = await self._get_user_by_username(current_user.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Actualizar campos permitidos
        allowed_fields = ["full_name", "phone"]
        for field, value in profile_data.items():
            if field in allowed_fields and value is not None:
                setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return UserProfile.from_orm(user)

    # Métodos auxiliares privados
    async def _authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autenticar usuario con username y password"""
        user = await self._get_user_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
            
        if user.is_active != 1:
            return None
            
        return user

    async def _get_user_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario"""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def _get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def _get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
