from winejournal.extensions import db


class Region(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(250))
    image = db.Column(db.String(250))
    parent_id = db.Column(db.Integer)
    country = db.Column(db.String(20), index=True)
    state = db.Column(db.String(20), index=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'parent_id': self.parent_id,
            'country': self.country,
            'state': self.state
        }