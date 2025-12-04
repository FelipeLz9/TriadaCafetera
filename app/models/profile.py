from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id_profile = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    location = Column(String(100), nullable=True)
    website = Column(String(150), nullable=True)
    theme = Column(String(20), default="light")
    language = Column(String(10), default="es")
    show_email = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="profile")
