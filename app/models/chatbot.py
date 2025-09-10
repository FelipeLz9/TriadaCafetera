from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Chatbot(Base):
    __tablename__ = 'chatbots'
    
    id = Column(Integer, primary_key=True, index=True)
    ask = Column(String, unique=True, index=True)
    answer = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="chatbots")
    conversations = relationship("Conversation", back_populates="chatbot")