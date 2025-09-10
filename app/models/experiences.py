from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Experiences(Base):
    __tablename__ = 'experiences'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    schedule = Column(String, index=True)
    duration = Column(Integer, index=True)
    price = Column(Integer, index=True)
    location = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="experiences")
    bookings = relationship("Booking", back_populates="experience")