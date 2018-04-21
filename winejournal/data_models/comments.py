from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user

from winejournal.data_models.timestamp import TimeStampMixin
from winejournal.extensions import db


class Comment(db.Model, TimeStampMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text)
    image = db.Column(db.String(250))
    tnote_id = db.Column(db.Integer, db.ForeignKey('tasting_notes.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'text': self.text,
            'image': self.image,
            'tnote_id': self.tnote_id,
            'created_on': self.created_on,
            'updated_on': self.updated_on
        }


def comment_owner_required(f):
    """
    Ensure a user is admin or the comment owner,
    if not redirect them to the wine list page page.

    :return: Function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            comment_id = kwargs['comment_id']
            cat = db.session.query(Comment).get(comment_id)
            owner_id = cat.author_id
            if current_user.id != owner_id:
                flash('You must be the owner to access that page')
                return redirect(url_for('wines.wine_list'))

            return f(*args, **kwargs)

    return decorated_function
