from pydantic import BaseModel
from typing import Optional, List

class EstateBase(BaseModel):
    name: str
    location: str
    size: int
    price: int
    owner_id: int

class EstateCreate(EstateBase):
    pass

class EstateUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    size: Optional[int] = None
    price: Optional[int] = None
    owner_id: Optional[int] = None

class EstateResponse(EstateBase):
    id: int

    class Config:
        from_attributes = True

class ServiceResponse(BaseModel):
    id_service: int
    name: str
    description: Optional[str] = None
    category: str
    price: int
    estate_id: int

    class Config:
        from_attributes = True
