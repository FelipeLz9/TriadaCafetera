from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.utils.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta

class UserController:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Crear un nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            existing_user = self.get_user_by_username(user_data.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya existe"
                )
            
            existing_email = self.get_user_by_email(user_data.email)
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
                is_active=True
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return UserResponse.from_orm(db_user)
            
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad en la base de datos"
            )

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Obtener usuario por ID"""
        result = self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            return None
            
        return UserResponse.from_orm(user)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario (modelo de BD)"""
        result = self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    def get_user_by_username_response(self, username: str) -> Optional[UserResponse]:
        """Obtener usuario por nombre de usuario (schema de respuesta)"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        return UserResponse.from_orm(user)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        result = self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Obtener todos los usuarios con paginación"""
        result = self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        users = result.scalars().all()
        return [UserResponse.from_orm(user) for user in users]

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """Actualizar usuario"""
        # Verificar si el usuario existe
        existing_user = self.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Preparar datos para actualizar
        update_data = user_data.dict(exclude_unset=True)
        
        # Si se proporciona una nueva contraseña, hashearla
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        # Actualizar el usuario
        self.db.execute(
            update(User).where(User.id == user_id).values(**update_data)
        )
        self.db.commit()

        # Retornar el usuario actualizado
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id: int) -> bool:
        """Eliminar usuario (soft delete - marcar como inactivo)"""
        existing_user = self.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Soft delete - marcar como inactivo
        self.db.execute(
            update(User).where(User.id == user_id).values(is_active=False)
        )
        self.db.commit()
        return True

    def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        """Autenticar usuario"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
            
        if not user.is_active:
            return None
            
        return UserResponse.from_orm(user)

    def login_user(self, login_data: UserLogin) -> dict:
        """Login de usuario y generación de token"""
        user = self.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }