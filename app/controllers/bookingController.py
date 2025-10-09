from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate


class BookingController:
    
    @staticmethod
    async def create_booking(db: AsyncSession, booking_data: BookingCreate) -> Booking:
        """Crear una nueva reserva"""
        try:
            new_booking = Booking(
                start_date=booking_data.start_date,
                end_date=booking_data.end_date,
                status=booking_data.status,
                num_persons=booking_data.num_persons,
                user_id=booking_data.user_id,
                estate_id=booking_data.estate_id
            )
            
            db.add(new_booking)
            await db.commit()
            await db.refresh(new_booking)
            return new_booking
            
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear la reserva: {str(e)}"
            )
    
    @staticmethod
    async def get_booking_by_id(db: AsyncSession, booking_id: int) -> Optional[Booking]:
        """Obtener una reserva por ID"""
        try:
            stmt = select(Booking).where(Booking.id == booking_id)
            result = await db.execute(stmt)
            booking = result.scalar_one_or_none()
            
            if not booking:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reserva no encontrada"
                )
            
            return booking
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la reserva: {str(e)}"
            )
    
    @staticmethod
    async def get_all_bookings(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        user_id: Optional[int] = None,
        estate_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Booking]:
        """Obtener todas las reservas con filtros opcionales"""
        try:
            stmt = select(Booking)
            
            # Aplicar filtros si se proporcionan
            if user_id:
                stmt = stmt.where(Booking.user_id == user_id)
            if estate_id:
                stmt = stmt.where(Booking.estate_id == estate_id)
            if status:
                stmt = stmt.where(Booking.status == status)
            
            stmt = stmt.offset(skip).limit(limit)
            
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las reservas: {str(e)}"
            )
    
    @staticmethod
    async def update_booking(
        db: AsyncSession, 
        booking_id: int, 
        booking_update: BookingUpdate
    ) -> Booking:
        """Actualizar una reserva existente"""
        try:
            # Obtener la reserva existente
            booking = await BookingController.get_booking_by_id(db, booking_id)
            
            # Actualizar solo los campos que se proporcionaron
            update_data = booking_update.model_dump(exclude_unset=True)
            
            for field, value in update_data.items():
                setattr(booking, field, value)
            
            await db.commit()
            await db.refresh(booking)
            return booking
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al actualizar la reserva: {str(e)}"
            )
    
    @staticmethod
    async def delete_booking(db: AsyncSession, booking_id: int) -> bool:
        """Eliminar una reserva"""
        try:
            booking = await BookingController.get_booking_by_id(db, booking_id)
            
            await db.delete(booking)
            await db.commit()
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al eliminar la reserva: {str(e)}"
            )
    
    @staticmethod
    async def get_bookings_by_user(db: AsyncSession, user_id: int) -> List[Booking]:
        """Obtener todas las reservas de un usuario específico"""
        try:
            stmt = select(Booking).where(Booking.user_id == user_id)
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las reservas del usuario: {str(e)}"
            )
    
    @staticmethod
    async def get_bookings_by_estate(db: AsyncSession, estate_id: int) -> List[Booking]:
        """Obtener todas las reservas de una finca específica"""
        try:
            stmt = select(Booking).where(Booking.estate_id == estate_id)
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las reservas de la finca: {str(e)}"
            )
