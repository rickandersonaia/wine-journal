from winejournal.extensions import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
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
