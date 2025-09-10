from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    estate_id = Column(Integer, ForeignKey('estates.id'), nullable=False)

    user = relationship("User", back_populates="reviews")
    estate = relationship("Estate", back_populates="reviews")