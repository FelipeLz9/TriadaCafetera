from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(String, index=True)
    end_date = Column(String, index=True)
    status = Column(String, index=True)
    num_persons = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    estate_id = Column(Integer, ForeignKey('estates.id'))
    
    user = relationship("User", back_populates="bookings")
    estate = relationship("Estate", back_populates="bookings")
