from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from winejournal.data_models.models import Base


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
