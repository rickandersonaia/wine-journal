import os

from flask import Flask
from flask_assets import Environment, Bundle
from flask_uploads import configure_uploads, UploadSet, IMAGES

from winejournal.blueprints.categories import categories
from winejournal.blueprints.regions import regions
from winejournal.blueprints.s3 import s3
from winejournal.blueprints.static_pages import staticPages
from winejournal.blueprints.static_pages.views import \
    twitter_blueprint, \
    google_blueprint, \
    facebook_blueprint
from winejournal.blueprints.tasting_notes import tastingNote
from winejournal.blueprints.media.views import media
from winejournal.blueprints.users import users
from winejournal.blueprints.wines import wines
from winejournal.extensions import (
    debug_toolbar,
    csrf,
    db,
    login_manager
)

photos = UploadSet('photos', IMAGES)


def create_app(settings_override=None):
    """
    Create the Flask application using the app factory pattern
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.static_folder = 'static'

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    assets = Environment(app)
    css = Bundle('scss/styles.scss',
                 filters='pyscss', output='css/styles.css')
    assets.register('css_all', css)
    assets.init_app(app)

    app.config['UPLOADED_PHOTOS_DEST'] = 'winejournal/static/img'
    configure_uploads(app, photos)

    app.register_blueprint(staticPages)
    app.register_blueprint(categories)
    app.register_blueprint(regions)
    app.register_blueprint(wines)
    app.register_blueprint(users)
    app.register_blueprint(s3)
    app.register_blueprint(tastingNote)
    app.register_blueprint(media)
    app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')
    app.register_blueprint(google_blueprint, url_prefix='/google_login')
    app.register_blueprint(facebook_blueprint, url_prefix='/facebook_login')

    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return None


def static_file_directory():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
