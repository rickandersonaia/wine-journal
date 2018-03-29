from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from winejournal.data_models.models import Base


class Wine(Base):
    __tablename__ = 'wines'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    maker = Column(String(80), nullable = False)
    vintage = Column(String(80), index= True)
    price = Column(Integer)
    description = Column(String(250))
    region = Column(Integer, ForeignKey('regions.id'))
    category = Column(Integer, ForeignKey('categories.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'maker': self.maker,
            'vintage': self.vintage,
            'price': self.price,
            'description': self.description,
            'region': self.region,
            'category': self.category,
        }