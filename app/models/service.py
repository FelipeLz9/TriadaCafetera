from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    estate_id = Column(Integer, ForeignKey('estate.id'))

    providers = relationship("Provider", secondary="service_providers", back_populates="services")