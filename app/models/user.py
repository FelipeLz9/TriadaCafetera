from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relación 1:1 con Profile
    profile = relationship("Profile", back_populates="user", uselist=False)
    # Relaciones 1:N
    bookings = relationship("Booking", back_populates="user")
    experiences = relationship("Experiences", back_populates="user")
    estates = relationship("Estate", back_populates="owner")
