from winejournal.extensions import db


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    uuid = db.Column(db.String(80), nullable=False)
    s3key = db.Column(db.String(80), nullable=False)
    s3bucket = db.Column(db.String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'uuid': self.uuid,
            's3key': self.s3key,
            's3bucket': self.s3bucket
        }
