import os
from sqlite3 import connect

from flask import Flask


def create_app(test_config=None):
    """Creation and configuration of the application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=600,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import directory
    app.register_blueprint(directory.bp)
    from . import connections
    app.register_blueprint(connections.bp)
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    return app
