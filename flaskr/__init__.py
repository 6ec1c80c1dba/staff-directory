import os
from sqlite3 import connect

from flask import Flask, Response
from flask_talisman import Talisman
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect, CSRFError

def create_app(test_config=None):
    """Creation and configuration of the application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "2-sIth,P64bynlE/=X6va~,K_woB[z"
    app.config['DATABASE']= os.path.join(app.instance_path, 'flaskr.sqlite')
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

       # Disable https if app is run in testing mode
    force_https = False if app.config['TESTING'] else True

    Talisman(
        app=app,
        force_https = force_https
    )

    app.jinja_env.autoescape = True

    Marshmallow(app)
    # Configure application to not use CSRF protection library when testing
    if app.config['TESTING']:
        pass
    else:
        CSRFProtect(app)

    # @app.errorhandler(CSRFError)
    # def handle_csrf_error(e):
    #     return 'CSRF error - user forbidden', 403

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
