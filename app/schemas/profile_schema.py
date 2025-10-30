from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ProfileBase(BaseModel):
    bio: Optional[str]
    avatar_url: Optional[HttpUrl]
    location: Optional[str]
    website: Optional[HttpUrl]
    theme: Optional[str] = "light"
    language: Optional[str] = "es"
    show_email: Optional[bool] = False


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id_profile: int
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
