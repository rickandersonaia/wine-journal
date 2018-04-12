from winejournal.extensions import db
from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(250))
    image = db.Column(db.Integer, db.ForeignKey('media'))
    parent_id = db.Column(db.Integer, index=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'parent_id': self.parent_id
        }


def category_owner_required(f):
    """
    Ensure a user is either an admin or the owner of the category,
    if not redirect them to the category list page.

    :return: Function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            category_id = kwargs['category_id']
            cat = db.session.query(Category).get(category_id)
            owner_id = cat.owner
            if current_user.id != owner_id:
                flash('You must be the owner to access that page')
                return redirect(url_for('categories.list_categories'))

            return f(*args, **kwargs)

    return decorated_function