from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(String, unique=True, index=True)
    end_date = Column(String, index=True)
    status = Column(String, index=True)
    num_persons = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    estate_id = Column(Integer, ForeignKey('fincas.id'))
    
    user = relationship("User", back_populates="bookings")
    finca = relationship("Finca", back_populates="bookings")
    conversations = relationship("Conversation", back_populates="bookings")