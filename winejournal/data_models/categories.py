from sqlalchemy import Column, ForeignKey, Integer, String, Float
from winejournal.data_models.models import Base, engine


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    parent_id = Column(Integer, index=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id
        }