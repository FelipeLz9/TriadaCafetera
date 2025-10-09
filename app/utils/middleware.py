from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import jwt

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserProfile
from app.utils.auth import verify_token
from sqlalchemy import select

security = HTTPBearer()

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[UserProfile]:
    """
    Dependency opcional para obtener el usuario actual.
    Retorna None si no hay token o es inválido, sin lanzar excepción.
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token)
        if payload is None:
            return None
        
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if username is None or user_id is None:
            return None
            
    except jwt.PyJWTError:
        return None
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    
    if user is None or user.is_active != 1:
        return None
    
    return UserProfile.from_orm(user)

async def get_current_user_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> UserProfile:
    """
    Dependency requerido para obtener el usuario actual.
    Lanza excepción si no hay token o es inválido.
    """
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
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    if user.is_active != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    return UserProfile.from_orm(user)

def require_roles(allowed_roles: list):
    """
    Decorator para requerir roles específicos.
    """
    def role_checker(current_user: UserProfile = Depends(get_current_user_required)):
        # En este ejemplo, todos los usuarios tienen el mismo nivel de acceso
        # En un sistema más complejo, aquí verificarías los roles del usuario
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )
        return current_user
    return role_checker

def require_active_user():
    """
    Decorator para requerir usuario activo.
    """
    def active_checker(current_user: UserProfile = Depends(get_current_user_required)):
        if current_user.is_active != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        return current_user
    return active_checker
