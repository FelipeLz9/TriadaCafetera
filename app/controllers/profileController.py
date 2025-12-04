from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.profile import Profile
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate, ProfileResponse
from app.models.user import User

class ProfileController:
    def __init__(self, db: Session):
        self.db = db

    # ----------------------------
    #   Crear perfil
    # ----------------------------
    def create_profile(self, profile_data: ProfileCreate) -> ProfileResponse:
        """Crear un nuevo perfil"""
        try:
            # Verificar que exista el usuario asociado
            user_exist = self.db.execute(
                select(User).where(User.id == profile_data.user_id)
            ).scalar_one_or_none()

            if not user_exist:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El usuario asociado no existe"
                )

            # Verificar si el usuario YA tiene un perfil
            existing_profile = self.db.execute(
                select(Profile).where(Profile.user_id == profile_data.user_id)
            ).scalar_one_or_none()

            if existing_profile:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya tiene un perfil"
                )

            # Crear perfil
            db_profile = Profile(
                user_id=profile_data.user_id,
                bio=profile_data.bio,
                avatar_url=str(profile_data.avatar_url) if profile_data.avatar_url else None,
                location=profile_data.location,
                website=str(profile_data.website) if profile_data.website else None,
                theme=profile_data.theme,
                language=profile_data.language,
                show_email=profile_data.show_email
            )

            self.db.add(db_profile)
            self.db.commit()
            self.db.refresh(db_profile)

            return ProfileResponse.from_orm(db_profile)

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad en la base de datos"
            )

    # ----------------------------
    #   Obtener perfil por ID
    # ----------------------------
    def get_profile_by_id(self, profile_id: int) -> Optional[ProfileResponse]:
        """Obtener perfil por ID"""
        result = self.db.execute(
            select(Profile).where(Profile.id_profile == profile_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            return None

        return ProfileResponse.from_orm(profile)

    # ----------------------------
    #   Obtener perfil por user_id
    # ----------------------------
    def get_profile_by_user_id(self, user_id: int) -> Optional[ProfileResponse]:
        """Obtener perfil por ID de usuario"""
        result = self.db.execute(
            select(Profile).where(Profile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            return None

        return ProfileResponse.from_orm(profile)

    # ----------------------------
    #   Obtener todos los perfiles
    # ----------------------------
    def get_all_profiles(self, skip: int = 0, limit: int = 100) -> List[ProfileResponse]:
        """Obtener todos los perfiles con paginación"""
        result = self.db.execute(
            select(Profile).offset(skip).limit(limit)
        )
        profiles = result.scalars().all()

        return [ProfileResponse.from_orm(profile) for profile in profiles]

    # ----------------------------
    #   Actualizar perfil
    # ----------------------------
    def update_profile(self, profile_id: int, profile_data: ProfileUpdate) -> Optional[ProfileResponse]:
        """Actualizar perfil"""

        # Verificar que exista
        existing_profile = self.get_profile_by_id(profile_id)
        if not existing_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil no encontrado"
            )

        update_data = profile_data.model_dump(exclude_unset=True)
        
        # Convertir HttpUrl a string si existen
        if "avatar_url" in update_data and update_data["avatar_url"]:
            update_data["avatar_url"] = str(update_data["avatar_url"])
        if "website" in update_data and update_data["website"]:
            update_data["website"] = str(update_data["website"])

        # Actualizar
        self.db.execute(
            update(Profile).where(Profile.id_profile == profile_id).values(**update_data)
        )
        self.db.commit()

        return self.get_profile_by_id(profile_id)

    # ----------------------------
    #   Eliminar perfil (soft delete)
    # ----------------------------
    def delete_profile(self, profile_id: int) -> bool:
        """Eliminar perfil (soft delete)"""

        existing_profile = self.get_profile_by_id(profile_id)
        if not existing_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil no encontrado"
            )

        # Eliminar perfil (hard delete ya que no hay campo is_active)
        profile_to_delete = self.db.execute(
            select(Profile).where(Profile.id_profile == profile_id)
        ).scalar_one_or_none()
        
        if profile_to_delete:
            self.db.delete(profile_to_delete)
        self.db.commit()

        return True


