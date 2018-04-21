from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user

from winejournal.data_models.timestamp import TimeStampMixin
from winejournal.extensions import db


class Wine(db.Model, TimeStampMixin):
    __tablename__ = 'wines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    maker = db.Column(db.String(80), nullable=False)
    vintage = db.Column(db.String(80), index=True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(250))
    image = db.Column(db.String(250))
    region = db.Column(db.Integer, db.ForeignKey('regions.id'))
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

    tasting_notes = db.relationship('TastingNote',
                                    backref=db.backref('tasting_notes',
                                                       lazy=True))

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
            'created_on': self.created_on,
            'updated_on': self.updated_on
        }


def wine_owner_required(f):
    """
    Ensure a user is either an admin or the owner of the wine,
    if not redirect them to the wine list page.

    :return: Function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            wine_id = kwargs['wine_id']
            wine = db.session.query(Wine).get(wine_id)
            owner_id = wine.owner
            if current_user.id != owner_id:
                flash('You must be the owner to access that page')
                return redirect(url_for('wines.list_wines'))

            return f(*args, **kwargs)

    return decorated_function
