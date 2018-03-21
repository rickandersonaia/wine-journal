from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from winejournal.data_models.models import Base


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