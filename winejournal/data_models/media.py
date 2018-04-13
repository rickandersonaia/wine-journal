from winejournal.extensions import db


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    uuid = db.Column(db.String(80), nullable=False)
    s3key = db.Column(db.String(80), nullable=False)

    categories = db.relationship('Category',
                              backref=db.backref('media', lazy=True))
    regions = db.relationship('Region',
                                 backref=db.backref('media', lazy=True))
    wines = db.relationship('Wine',
                              backref=db.backref('media', lazy=True))
    tasting_notes = db.relationship('TastingNote',
                              backref=db.backref('media', lazy=True))
    comments = db.relationship('Comment',
                              backref=db.backref('media', lazy=True))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'uuid': self.uuid,
            's3key': self.s3key,
            's3bucket': self.s3bucket
        }
