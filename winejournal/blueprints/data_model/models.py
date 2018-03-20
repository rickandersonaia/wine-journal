import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

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

class Wine(Base):
    __tablename__ = 'wines'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    region = Column(Integer(8), ForeignKey('regions.id'))
    category = Column(Integer(8), ForeignKey('categories.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'description': self.description,
            'region': self.region,
            'category': self.category,
        }

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    parent_id = Column(Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id
        }

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    parent_id = Column(Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id
        }

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key = True)
    author_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(80), nullable = False)
    tasting_notes = Column(String(250))
    vintage = Column(String(15))
    rating = Column(Float(12))
    price = Column(Float(12))
    likes = Column(Integer(8))
    dlikes = Column(Integer(8))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'title': self.title,
            'tasting_notes': self.tasting_notes,
            'vintage': self.vintage,
            'rating': self.rating,
            'price': self.price,
            'likes': self.likes,
            'dlikes': self.dlikes,
        }


engine = create_engine('postgresql+psycopg2://winejournal:devpassword@postgres:5432/winejournal')
Base.metadata.create_all(engine)