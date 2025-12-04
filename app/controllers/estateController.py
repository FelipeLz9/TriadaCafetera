from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.estate import Estate
from app.schemas.estate import EstateCreate, EstateUpdate, EstateResponse

class EstateController:
    def __init__(self, db: Session):
        self.db = db

    def create_estate(self, estate_data: EstateCreate) -> EstateResponse:
        """Crear una nueva finca"""
        try:
            # Verificar si el nombre de la finca ya existe
            existing_estate = self.get_estate_by_name(estate_data.name)
            if existing_estate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una finca con ese nombre"
                )
            
            # Crear la nueva finca
            db_estate = Estate(
                name=estate_data.name,
                location=estate_data.location,
                size=estate_data.size,
                price=estate_data.price,
                owner_id=estate_data.owner_id
            )
            
            self.db.add(db_estate)
            self.db.commit()
            self.db.refresh(db_estate)
            
            return EstateResponse.from_orm(db_estate)
            
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de integridad en la base de datos: {str(e)}"
            )

    def get_estate_by_id(self, estate_id: int) -> Optional[EstateResponse]:
        """Obtener finca por ID"""
        result = self.db.execute(select(Estate).where(Estate.id == estate_id))
        estate = result.scalar_one_or_none()
        
        if not estate:
            return None
            
        return EstateResponse.from_orm(estate)

    def get_estate_by_name(self, name: str) -> Optional[Estate]:
        """Obtener finca por nombre (modelo de BD)"""
        result = self.db.execute(select(Estate).where(Estate.name == name))
        return result.scalar_one_or_none()

    def get_all_estates(
        self, 
        skip: int = 0, 
        limit: int = 100,
        owner_id: Optional[int] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None
    ) -> List[EstateResponse]:
        """Obtener todas las fincas con paginación y filtros opcionales"""
        stmt = select(Estate)
        
        # Aplicar filtros si se proporcionan
        if owner_id:
            stmt = stmt.where(Estate.owner_id == owner_id)
        if min_price is not None:
            stmt = stmt.where(Estate.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Estate.price <= max_price)
        
        stmt = stmt.offset(skip).limit(limit)
        result = self.db.execute(stmt)
        estates = result.scalars().all()
        
        return [EstateResponse.from_orm(estate) for estate in estates]

    def update_estate(self, estate_id: int, estate_data: EstateUpdate) -> Optional[EstateResponse]:
        """Actualizar finca"""
        # Verificar si la finca existe
        existing_estate = self.get_estate_by_id(estate_id)
        if not existing_estate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Finca no encontrada"
            )

        # Si se intenta cambiar el nombre, verificar que no exista otra finca con ese nombre
        update_data = estate_data.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing_by_name = self.get_estate_by_name(update_data["name"])
            if existing_by_name and existing_by_name.id != estate_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una finca con ese nombre"
                )

        # Actualizar la finca
        try:
            self.db.execute(
                update(Estate).where(Estate.id == estate_id).values(**update_data)
            )
            self.db.commit()

            # Retornar la finca actualizada
            return self.get_estate_by_id(estate_id)
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de integridad en la base de datos: {str(e)}"
            )

    def delete_estate(self, estate_id: int) -> bool:
        """Eliminar finca"""
        existing_estate = self.get_estate_by_id(estate_id)
        if not existing_estate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Finca no encontrada"
            )

        # Eliminar la finca
        self.db.execute(delete(Estate).where(Estate.id == estate_id))
        self.db.commit()
        return True

    def get_estates_by_owner(self, owner_id: int) -> List[EstateResponse]:
        """Obtener todas las fincas de un propietario específico"""
        return self.get_all_estates(owner_id=owner_id, skip=0, limit=1000)

