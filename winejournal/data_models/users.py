from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from winejournal.data_models.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String(50), default='')
    password = Column(String(255), nullable=False, default='')
    email = Column(String(255), nullable = False, unique=True)
    first_name = Column(String(50), nullable=False, default='')
    last_name = Column(String(50), nullable=False, default='')
    display_name = Column(String(50), default='')
    image = Column(String(255))
    role = Column(String(10), server_default='member', index=True)
    is_enabled = Column(Boolean(), server_default=True, index=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': self.display_name,
            'image': self.image,
            'role': self.role,
            'is_enabled': self.is_enabled
        }

    def is_active(self):
        return self.is_enabled
