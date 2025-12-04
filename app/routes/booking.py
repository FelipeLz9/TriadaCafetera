from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.controllers.bookingController import BookingController
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
    BookingDetail
)

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva reserva
    
    - **start_date**: Fecha de inicio (YYYY-MM-DD)
    - **end_date**: Fecha de fin (YYYY-MM-DD)
    - **status**: Estado de la reserva (pending, confirmed, cancelled)
    - **num_persons**: Número de personas
    - **user_id**: ID del usuario
    - **estate_id**: ID de la finca
    """
    controller = BookingController(db)
    return controller.create_booking(booking_data)


@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    user_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    estate_id: Optional[int] = Query(None, description="Filtrar por ID de finca"),
    status_filter: Optional[str] = Query(None, description="Filtrar por estado", alias="status"),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las reservas con filtros opcionales
    
    Filtros disponibles:
    - **user_id**: Mostrar solo reservas de un usuario específico
    - **estate_id**: Mostrar solo reservas de una finca específica
    - **status**: Filtrar por estado (pending, confirmed, cancelled)
    """
    controller = BookingController(db)
    return controller.get_all_bookings(
        skip=skip,
        limit=limit,
        user_id=user_id,
        estate_id=estate_id,
        status_filter=status_filter
    )


@router.get("/{booking_id}", response_model=BookingDetail)
def get_booking_by_id(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una reserva específica por su ID
    """
    controller = BookingController(db)
    booking = controller.get_booking_by_id(booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    return booking


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una reserva existente
    
    Solo se actualizarán los campos que se envíen en el request.
    Campos opcionales:
    - **start_date**: Nueva fecha de inicio
    - **end_date**: Nueva fecha de fin
    - **status**: Nuevo estado
    - **num_persons**: Nuevo número de personas
    """
    controller = BookingController(db)
    return controller.update_booking(booking_id, booking_update)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una reserva
    """
    controller = BookingController(db)
    controller.delete_booking(booking_id)
    return None


# Endpoints adicionales para casos específicos
@router.get("/user/{user_id}", response_model=List[BookingResponse])
def get_user_bookings(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las reservas de un usuario específico
    """
    controller = BookingController(db)
    return controller.get_bookings_by_user(user_id)


@router.get("/estate/{estate_id}", response_model=List[BookingResponse])
def get_estate_bookings(
    estate_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las reservas de una finca específica
    """
    controller = BookingController(db)
    return controller.get_bookings_by_estate(estate_id)
