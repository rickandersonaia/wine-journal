from flask_login import UserMixin
from werkzeug.security import generate_password_hash

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
