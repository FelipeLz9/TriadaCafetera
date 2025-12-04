from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExperienceBase(BaseModel):
    title: str
    description: str
    schedule: str
    duration: int
    price: int
    location: str
    user_id: int

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    schedule: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[int] = None
    location: Optional[str] = None
    user_id: Optional[int] = None

class ExperienceResponse(ExperienceBase):
    id_experience: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ExperienceWithUser(ExperienceResponse):
    """Experiencia con información del usuario"""
    user: Optional[dict] = None
