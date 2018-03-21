from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from winejournal.data_models.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String(80), nullable = False)
    email = Column(String(250))
    password = Column(String(80))
    fname = Column(String(80))
    lname = Column(String(80))
    dname = Column(String(80))
    image = Column(String(250))
    role = Column(String(10))

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
            'role': self.role
        }