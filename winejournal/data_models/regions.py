from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from winejournal.data_models.models import Base


class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    parent_id = Column(Integer)
    country = Column(String(20), index=True)
    state = Column(String(20), index=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'country': self.country,
            'state': self.state
        }