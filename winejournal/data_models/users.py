from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from winejournal.data_models.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String(24), nullable = False)
    email = Column(String(255), nullable = False, unique=True)
    password = Column(String(128))
    fname = Column(String(80))
    lname = Column(String(80))
    dname = Column(String(80))
    image = Column(String(255))
    role = Column(String(10), server_default='member', index=True)
    active = Column(Boolean(), server_default=True, index=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'fname': self.fname,
            'lname': self.lname,
            'dname': self.dname,
            'image': self.image,
            'role': self.role,
            'active': self.active
        }