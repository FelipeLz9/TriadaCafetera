from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.user import User

class Owner(User):
    __tablename__ = 'owners'
    id_owner = Column(Integer, ForeignKey('users.id_users'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'owner',
    }