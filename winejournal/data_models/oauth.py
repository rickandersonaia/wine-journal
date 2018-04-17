from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

from winejournal.data_models.users import User
from winejournal.extensions import db


class Oauth(db.Model, OAuthConsumerMixin):
    __tablename__ = 'flask_dance_oauth'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
