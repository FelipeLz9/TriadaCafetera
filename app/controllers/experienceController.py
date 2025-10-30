from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.experiences import Experiences
from app.models.user import User
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse, ExperienceWithUser

class ExperienceController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_experience(self, experience_data: ExperienceCreate) -> ExperienceResponse:
        """Crear una nueva experiencia"""
        try:
            # Verificar si el título ya existe
            existing_experience = await self.get_experience_by_title(experience_data.title)
            if existing_experience:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una experiencia con este título"
                )
            
            # Verificar si el usuario existe
            user_exists = await self._user_exists(experience_data.user_id)
            if not user_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario especificado no existe"
                )

            # Crear la nueva experiencia
            db_experience = Experiences(
                title=experience_data.title,
                description=experience_data.description,
                schedule=experience_data.schedule,
                duration=experience_data.duration,
                price=experience_data.price,
                location=experience_data.location,
                user_id=experience_data.user_id
            )
            
            self.db.add(db_experience)
            await self.db.commit()
            await self.db.refresh(db_experience)
            
            return ExperienceResponse.from_orm(db_experience)
            
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad en la base de datos"
            )

    async def get_experience_by_id(self, experience_id: int) -> Optional[ExperienceResponse]:
        """Obtener experiencia por ID"""
        result = await self.db.execute(
            select(Experiences).where(Experiences.id_experience == experience_id)
        )
        experience = result.scalar_one_or_none()
        
        if not experience:
            return None
            
        return ExperienceResponse.from_orm(experience)

    async def get_experience_by_title(self, title: str) -> Optional[Experiences]:
        """Obtener experiencia por título (modelo de BD)"""
        result = await self.db.execute(
            select(Experiences).where(Experiences.title == title)
        )
        return result.scalar_one_or_none()

    async def get_all_experiences(self, skip: int = 0, limit: int = 100) -> List[ExperienceResponse]:
        """Obtener todas las experiencias con paginación"""
        result = await self.db.execute(
            select(Experiences).offset(skip).limit(limit)
        )
        experiences = result.scalars().all()
        return [ExperienceResponse.from_orm(exp) for exp in experiences]

    async def get_experiences_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ExperienceResponse]:
        """Obtener experiencias de un usuario específico"""
        result = await self.db.execute(
            select(Experiences)
            .where(Experiences.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        experiences = result.scalars().all()
        return [ExperienceResponse.from_orm(exp) for exp in experiences]

    async def get_experiences_by_location(self, location: str, skip: int = 0, limit: int = 100) -> List[ExperienceResponse]:
        """Obtener experiencias por ubicación"""
        result = await self.db.execute(
            select(Experiences)
            .where(Experiences.location.ilike(f"%{location}%"))
            .offset(skip)
            .limit(limit)
        )
        experiences = result.scalars().all()
        return [ExperienceResponse.from_orm(exp) for exp in experiences]

    async def get_experiences_by_price_range(self, min_price: int, max_price: int, skip: int = 0, limit: int = 100) -> List[ExperienceResponse]:
        """Obtener experiencias por rango de precio"""
        result = await self.db.execute(
            select(Experiences)
            .where(Experiences.price >= min_price)
            .where(Experiences.price <= max_price)
            .offset(skip)
            .limit(limit)
        )
        experiences = result.scalars().all()
        return [ExperienceResponse.from_orm(exp) for exp in experiences]

    async def update_experience(self, experience_id: int, experience_data: ExperienceUpdate) -> Optional[ExperienceResponse]:
        """Actualizar experiencia"""
        # Verificar si la experiencia existe
        existing_experience = await self.get_experience_by_id(experience_id)
        if not existing_experience:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiencia no encontrada"
            )

        # Si se actualiza el título, verificar que no exista otro con el mismo título
        if experience_data.title:
            existing_title = await self.get_experience_by_title(experience_data.title)
            if existing_title and existing_title.id_experience != experience_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una experiencia con este título"
                )

        # Si se actualiza el user_id, verificar que el usuario existe
        if experience_data.user_id:
            user_exists = await self._user_exists(experience_data.user_id)
            if not user_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario especificado no existe"
                )

        # Preparar datos para actualizar
        update_data = experience_data.dict(exclude_unset=True)

        # Actualizar la experiencia
        await self.db.execute(
            update(Experiences)
            .where(Experiences.id_experience == experience_id)
            .values(**update_data)
        )
        await self.db.commit()

        # Retornar la experiencia actualizada
        return await self.get_experience_by_id(experience_id)

    async def delete_experience(self, experience_id: int) -> bool:
        """Eliminar experiencia"""
        existing_experience = await self.get_experience_by_id(experience_id)
        if not existing_experience:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiencia no encontrada"
            )

        # Eliminar la experiencia
        await self.db.execute(
            delete(Experiences).where(Experiences.id_experience == experience_id)
        )
        await self.db.commit()
        return True

    async def get_experience_with_user(self, experience_id: int) -> Optional[ExperienceWithUser]:
        """Obtener experiencia con información del usuario"""
        result = await self.db.execute(
            select(Experiences)
            .options(selectinload(Experiences.user))
            .where(Experiences.id_experience == experience_id)
        )
        experience = result.scalar_one_or_none()
        
        if not experience:
            return None
        
        # Crear el objeto de respuesta con información del usuario
        experience_data = ExperienceResponse.from_orm(experience).dict()
        user_data = {
            "id": experience.user.id,
            "username": experience.user.username,
            "full_name": experience.user.full_name,
            "email": experience.user.email
        } if experience.user else None
        
        experience_data["user"] = user_data
        return ExperienceWithUser(**experience_data)

    async def _user_exists(self, user_id: int) -> bool:
        """Verificar si un usuario existe"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none() is not None

    async def search_experiences(self, query: str, skip: int = 0, limit: int = 100) -> List[ExperienceResponse]:
        """Buscar experiencias por título o descripción"""
        result = await self.db.execute(
            select(Experiences)
            .where(
                Experiences.title.ilike(f"%{query}%") |
                Experiences.description.ilike(f"%{query}%")
            )
            .offset(skip)
            .limit(limit)
        )
        experiences = result.scalars().all()
        return [ExperienceResponse.from_orm(exp) for exp in experiences]
