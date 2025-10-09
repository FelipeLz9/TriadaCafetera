from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Service(Base):
    __tablename__ = 'services'

    id_service = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    estate_id = Column(Integer, ForeignKey('estates.id'))

    estate = relationship("Estate", back_populates="services")