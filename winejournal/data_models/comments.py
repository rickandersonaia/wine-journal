from winejournal.extensions import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(80), nullable = False)
    tasting_notes = db.Column(db.String(250))
    image = db.Column(db.String(250))
    vintage = db.Column(db.String(15))
    rating = db.Column(db.Float(12))
    price = db.Column(db.Float(12))
    likes = db.Column(db.Integer(8))
    dlikes = db.Column(db.Integer(8))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'title': self.title,
            'tasting_notes': self.tasting_notes,
            'image': self.image,
            'vintage': self.vintage,
            'rating': self.rating,
            'price': self.price,
            'likes': self.likes,
            'dlikes': self.dlikes,
        }
