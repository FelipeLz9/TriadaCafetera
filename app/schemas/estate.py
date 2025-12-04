from pydantic import BaseModel, Field
from typing import Optional

class EstateBase(BaseModel):
    name: str = Field(..., description="Nombre de la finca")
    location: str = Field(..., description="Ubicación de la finca")
    size: int = Field(..., gt=0, description="Tamaño de la finca en hectáreas")
    price: int = Field(..., gt=0, description="Precio de la finca")

class EstateCreate(EstateBase):
    owner_id: int = Field(..., description="ID del propietario (usuario)")

class EstateUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nombre de la finca")
    location: Optional[str] = Field(None, description="Ubicación de la finca")
    size: Optional[int] = Field(None, gt=0, description="Tamaño de la finca en hectáreas")
    price: Optional[int] = Field(None, gt=0, description="Precio de la finca")
    owner_id: Optional[int] = Field(None, description="ID del propietario")

class EstateResponse(EstateBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True

