from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user

from winejournal.data_models.timestamp import TimeStampMixin
from winejournal.extensions import db


class TastingNote(db.Model, TimeStampMixin):
    __tablename__ = 'tasting_notes'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text)
    image = db.Column(db.String(250))
    vintage = db.Column(db.String(15))
    rating = db.Column(db.Float(12))
    price = db.Column(db.Float(12))
    likes = db.Column(db.Integer)
    dlikes = db.Column(db.Integer)
    wine_id = db.Column(db.Integer, db.ForeignKey('wines.id'))

    comments = db.relationship('Comment',
                               backref=db.backref('tasting_note', lazy='subquery'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'vintage': self.vintage,
            'rating': self.rating,
            'price': self.price,
            'likes': self.likes,
            'dlikes': self.dlikes,
            'created_on': self.created_on,
            'updated_on': self.updated_on
        }


def tnote_owner_required(f):
    """
    Ensure a user is admin or the tasting note owner,
    if not redirect them to the wine list page page.

    :return: Function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            tnote_id = kwargs['tnote_id']
            cat = db.session.query(TastingNote).get(tnote_id)
            owner_id = cat.author_id
            if current_user.id != owner_id:
                flash('You must be the owner to access that page')
                return redirect(url_for('wines.wine_list'))

            return f(*args, **kwargs)

    return decorated_function
