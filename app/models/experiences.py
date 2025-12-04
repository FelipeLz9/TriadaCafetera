from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Experiences(Base):
    __tablename__ = 'experiences'
    
    id_experience = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    schedule = Column(String)
    duration = Column(Integer)
    price = Column(Integer, index=True)
    location = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="experiences")
    bookings = relationship("Booking", back_populates="experience")