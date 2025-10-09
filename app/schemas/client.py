from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None

class ClientCreate(ClientBase):
    password: str

class ClientUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class ClientResponse(ClientBase):
    id_client: int
    is_active: int

    class Config:
        from_attributes = True

class ClientInDB(ClientResponse):
    hashed_password: str
