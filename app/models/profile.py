from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Profile(Base):
    __tablename__ = 'profiles'
    
    id_profile = Column(Integer, primary_key=True)
    bio = Column(String)
    avatar_url = Column(String)
    user_id = Column(Integer, ForeignKey('users.id_users'))
    
    user = relationship("User", back_populates="profile")