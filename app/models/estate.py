from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Estate(Base):
    __tablename__ = 'estates'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String, index=True)
    size = Column(Integer, index=True)
    price = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    bookings = relationship("Booking", back_populates="finca")
    
    owner = relationship("User", back_populates="estates")
    properties = relationship("Property", back_populates="estate")