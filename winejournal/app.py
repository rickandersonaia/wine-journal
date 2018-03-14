from flask import Flask
from flask_assets import Environment, Bundle
from winejournal.blueprints.static_pages import staticPages


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

    if __name__ == '__main__':
        app.debug = app.config['DEBUG']
        app.run(host='0.0.0.0', port=5000)

    return app


app = create_app()
