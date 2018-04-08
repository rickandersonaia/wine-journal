from flask_login import UserMixin, current_user
from flask import redirect, url_for, flash
from werkzeug.security import generate_password_hash
from functools import wraps

from winejournal.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), default='')
    password = db.Column(db.String(255), default='')
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')
    display_name = db.Column(db.String(50), default='')
    image = db.Column(db.String(255))
    role = db.Column(db.String(10), server_default='member', index=True)
    is_enabled = db.Column(db.Boolean(), server_default='True')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': self.display_name,
            'image': self.image,
            'role': self.role,
            'is_enabled': self.is_enabled
        }

    def is_active(self):
        return self.is_enabled

    def is_admin(self):
        if self.role =="admin":
            return True
        else:
            return False

    def is_owner(self, owner_id):
        if self.id == owner_id:
            return True
        else:
            return False

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return User.query.filter(
            (User.email == identity) | (User.username == identity)).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None


def role_list():
    roles = [
        ('member', 'regular member'),
        ('admin', 'administrator')
    ]
    return roles


def admin_required(f):
    """
    Ensure a user is admin, if not redirect them to the home page.

    :return: Function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('You must be an admin to view that page')
            return redirect(url_for('wines.list_wines'))

        return f(*args, **kwargs)

    return decorated_function

def owner_required(f):
    """
    Ensure a user is admin, if not redirect them to the home page.

    :return: Function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            user_id = kwargs['user_id']
            if current_user.id != user_id:
                flash('You must be the owner to access that page')
                return redirect(url_for('wines.list_wines'))

            return f(*args, **kwargs)

    return decorated_function

