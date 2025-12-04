from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookingBase(BaseModel):
    start_date: str = Field(..., description="Fecha de inicio de la reserva (YYYY-MM-DD)")
    end_date: str = Field(..., description="Fecha de fin de la reserva (YYYY-MM-DD)")
    status: str = Field(..., description="Estado de la reserva (pending, confirmed, cancelled)")
    num_persons: int = Field(..., gt=0, description="Número de personas")
    estate_id: int = Field(..., description="ID de la finca")

class BookingCreate(BookingBase):
    user_id: int = Field(..., description="ID del usuario que hace la reserva")

class BookingUpdate(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None
    num_persons: Optional[int] = Field(None, gt=0)

class BookingResponse(BookingBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class BookingDetail(BookingResponse):
    # Aquí puedes incluir información relacionada si necesitas
    # user: Optional[UserResponse] = None
    # estate: Optional[EstateResponse] = None
    pass
