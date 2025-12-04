from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    hashed_password = Column(String)
    phone = Column(String, unique=True, index=True)
    is_active = Column(Integer, default=1)
    
    # Relaciones - usar lazy="select" para evitar problemas de importación circular
    estates = relationship("Estate", back_populates="owner", lazy="select", cascade="all, delete-orphan")
    experiences = relationship("Experiences", back_populates="user", lazy="select", cascade="all, delete-orphan")
    profile = relationship("Profile", back_populates="user", lazy="select", uselist=False, cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", lazy="select", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", lazy="select", cascade="all, delete-orphan")