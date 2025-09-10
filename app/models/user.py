from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    hashed_password = Column(String)
    phone = Column(String, unique=True, index=True)
    is_active = Column(Integer, default=1)
    
    estates = relationship("Estate", back_populates="owner")
    experiences = relationship("Experiences", back_populates="user")
    chatbots = relationship("Chatbot", back_populates="user")