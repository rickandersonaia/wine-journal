from winejournal.extensions import db


class Wine(db.Model):
    __tablename__ = 'wines'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    maker = db.Column(db.String(80), nullable = False)
    vintage = db.Column(db.String(80), index= True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(250))
    image = db.Column(db.String(250))
    region = db.Column(db.Integer, db.ForeignKey('regions.id'))
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    owner = db.Column(db.Integer, server_default='1')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'maker': self.maker,
            'vintage': self.vintage,
            'price': self.price,
            'description': self.description,
            'image': self.image,
            'region': self.region,
            'category': self.category,
            'owner': self.owner,
        }