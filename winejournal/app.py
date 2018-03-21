from flask import Flask
from flask_assets import Environment, Bundle
from winejournal.blueprints.static_pages import staticPages
from winejournal.data_models import models
# from winejournal.blueprints.user import user
# from winejournal.blueprints.user.models import User
from winejournal.extensions import (
    debug_toolbar,
    csrf,
    db,
    login_manager
)


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

    app.register_blueprint(staticPages)
    app.register_blueprint(staticPages)

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