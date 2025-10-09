from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
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


@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db)
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
    return await BookingController.create_booking(db, booking_data)


@router.get("/", response_model=List[BookingResponse])
async def get_all_bookings(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    user_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    estate_id: Optional[int] = Query(None, description="Filtrar por ID de finca"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener todas las reservas con filtros opcionales
    
    Filtros disponibles:
    - **user_id**: Mostrar solo reservas de un usuario específico
    - **estate_id**: Mostrar solo reservas de una finca específica
    - **status**: Filtrar por estado (pending, confirmed, cancelled)
    """
    return await BookingController.get_all_bookings(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        estate_id=estate_id,
        status=status
    )


@router.get("/{booking_id}", response_model=BookingDetail)
async def get_booking_by_id(
    booking_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener una reserva específica por su ID
    """
    return await BookingController.get_booking_by_id(db, booking_id)


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    db: AsyncSession = Depends(get_db)
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
    return await BookingController.update_booking(db, booking_id, booking_update)


@router.delete("/{booking_id}", status_code=204)
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar una reserva
    """
    await BookingController.delete_booking(db, booking_id)
    return {"message": "Reserva eliminada exitosamente"}


# Endpoints adicionales para casos específicos
@router.get("/user/{user_id}", response_model=List[BookingResponse])
async def get_user_bookings(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener todas las reservas de un usuario específico
    """
    return await BookingController.get_bookings_by_user(db, user_id)


@router.get("/estate/{estate_id}", response_model=List[BookingResponse])
async def get_estate_bookings(
    estate_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener todas las reservas de una finca específica
    """
    return await BookingController.get_bookings_by_estate(db, estate_id)
