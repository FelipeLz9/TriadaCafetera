<<<<<<< HEAD
from pydantic import BaseModel, EmailStr
=======
from pydantic import BaseModel, EmailStr, Field
>>>>>>> ac92324246a3a9f215ff2e9db0c8aea54c542b40
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    phone: str

class UserCreate(UserBase):
<<<<<<< HEAD
    password: str
=======
    password: str = Field(..., min_length=1, max_length=72, description="Contraseña (máximo 72 bytes para bcrypt)")
>>>>>>> ac92324246a3a9f215ff2e9db0c8aea54c542b40

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[int] = None

class UserResponse(UserBase):
    id: int
    is_active: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str
