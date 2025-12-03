from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.booking import Booking
from app.models.user import User
from app.models.estate import Estate
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse


class BookingController:
    def __init__(self, db: Session):
        self.db = db

    def create_booking(self, booking_data: BookingCreate) -> BookingResponse:
        """Crear una nueva reserva"""
        try:
            # Verificar que el usuario existe
            user_result = self.db.execute(select(User).where(User.id == booking_data.user_id))
            user = user_result.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuario con ID {booking_data.user_id} no encontrado"
                )
            
            # Verificar que la finca existe
            estate_result = self.db.execute(select(Estate).where(Estate.id == booking_data.estate_id))
            estate = estate_result.scalar_one_or_none()
            if not estate:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Finca con ID {booking_data.estate_id} no encontrada"
                )
            
            new_booking = Booking(
                start_date=booking_data.start_date,
                end_date=booking_data.end_date,
                status=booking_data.status,
                num_persons=booking_data.num_persons,
                user_id=booking_data.user_id,
                estate_id=booking_data.estate_id
            )
            
            self.db.add(new_booking)
            self.db.commit()
            self.db.refresh(new_booking)
            
            return BookingResponse.from_orm(new_booking)
            
        except HTTPException:
            self.db.rollback()
            raise
        except IntegrityError as e:
            self.db.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            if "UNIQUE constraint" in error_msg or "unique constraint" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una reserva con esta fecha de inicio"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de integridad al crear la reserva: {error_msg}"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear la reserva: {str(e)}"
            )
    
    def get_booking_by_id(self, booking_id: int) -> Optional[BookingResponse]:
        """Obtener una reserva por ID"""
        result = self.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = result.scalar_one_or_none()
        
        if not booking:
            return None
            
        return BookingResponse.from_orm(booking)
    
    def get_all_bookings(
        self, 
        skip: int = 0, 
        limit: int = 100,
        user_id: Optional[int] = None,
        estate_id: Optional[int] = None,
        status_filter: Optional[str] = None
    ) -> List[BookingResponse]:
        """Obtener todas las reservas con filtros opcionales"""
        try:
            stmt = select(Booking)
            
            # Aplicar filtros si se proporcionan
            if user_id:
                stmt = stmt.where(Booking.user_id == user_id)
            if estate_id:
                stmt = stmt.where(Booking.estate_id == estate_id)
            if status_filter:
                stmt = stmt.where(Booking.status == status_filter)
            
            stmt = stmt.offset(skip).limit(limit)
            
            result = self.db.execute(stmt)
            bookings = result.scalars().all()
            
            return [BookingResponse.from_orm(booking) for booking in bookings]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener las reservas: {str(e)}"
            )
    
    def update_booking(
        self, 
        booking_id: int, 
        booking_update: BookingUpdate
    ) -> Optional[BookingResponse]:
        """Actualizar una reserva existente"""
        # Verificar si la reserva existe
        existing_booking = self.get_booking_by_id(booking_id)
        if not existing_booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        # Actualizar solo los campos que se proporcionaron
        update_data = booking_update.model_dump(exclude_unset=True)
        
        try:
            self.db.execute(
                update(Booking).where(Booking.id == booking_id).values(**update_data)
            )
            self.db.commit()
            
            # Retornar la reserva actualizada
            return self.get_booking_by_id(booking_id)
            
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de integridad al actualizar la reserva: {str(e)}"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al actualizar la reserva: {str(e)}"
            )
    
    def delete_booking(self, booking_id: int) -> bool:
        """Eliminar una reserva"""
        existing_booking = self.get_booking_by_id(booking_id)
        if not existing_booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        try:
            self.db.execute(delete(Booking).where(Booking.id == booking_id))
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al eliminar la reserva: {str(e)}"
            )
    
    def get_bookings_by_user(self, user_id: int) -> List[BookingResponse]:
        """Obtener todas las reservas de un usuario específico"""
        return self.get_all_bookings(user_id=user_id, skip=0, limit=1000)
    
    def get_bookings_by_estate(self, estate_id: int) -> List[BookingResponse]:
        """Obtener todas las reservas de una finca específica"""
        return self.get_all_bookings(estate_id=estate_id, skip=0, limit=1000)
