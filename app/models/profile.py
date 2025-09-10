from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Profile(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String, index=True)
    avatar_url = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="profile")