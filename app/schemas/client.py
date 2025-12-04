from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ClientBase(BaseModel):
    username: str = Field(..., description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Email único del cliente")
    full_name: Optional[str] = Field(None, description="Nombre completo del cliente")
    phone: Optional[str] = Field(None, description="Teléfono único del cliente")

class ClientCreate(ClientBase):
    password: str = Field(..., min_length=1, max_length=72, description="Contraseña (máximo 72 bytes para bcrypt)")

class ClientUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Nombre de usuario único")
    email: Optional[EmailStr] = Field(None, description="Email único del cliente")
    full_name: Optional[str] = Field(None, description="Nombre completo del cliente")
    phone: Optional[str] = Field(None, description="Teléfono único del cliente")
    password: Optional[str] = Field(None, min_length=1, max_length=72, description="Contraseña (máximo 72 bytes para bcrypt)")

class ClientResponse(ClientBase):
    id_client: int
    is_active: int

    class Config:
        from_attributes = True

class ClientInDB(ClientResponse):
    hashed_password: str
