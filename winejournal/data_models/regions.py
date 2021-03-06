from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user

from winejournal.data_models.timestamp import TimeStampMixin
from winejournal.extensions import db


class Region(db.Model, TimeStampMixin):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(250))
    parent_id = db.Column(db.Integer)
    country = db.Column(db.String(20), index=True)
    state = db.Column(db.String(20), index=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

    wine = db.relationship('Wine', backref=db.backref('wine_region',
                                                      lazy=True))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'parent_id': self.parent_id,
            'country': self.country,
            'state': self.state,
            'created_on': self.created_on,
            'updated_on': self.updated_on
        }


def region_owner_required(f):
    """
    Ensure a user is admin or the region owner,
    if not redirect them to the regions list page page.

    :return: Function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            region_id = kwargs['region_id']
            cat = db.session.query(Region).get(region_id)
            owner_id = cat.owner
            if current_user.id != owner_id:
                flash('You must be the owner to access that page')
                return redirect(url_for('regions.list_regions'))

            return f(*args, **kwargs)

    return decorated_function
