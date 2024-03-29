import os
from sqlite3 import connect

from flask import Flask, Response
from flask_talisman import Talisman
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import timedelta
from . import db
from . import auth
from . import home
from . import directory
from . import connections

def create_app(test_config=None):
    """Creation and configuration of the application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "2-sIth,P64bynlE/=X6va~,K_woB[z"
    app.config['DATABASE']= os.path.join(app.instance_path, 'flaskr.sqlite')
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
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

    db.init_app(app)
    Marshmallow(app)
    
    # Configure application to not use CSRF protection library when testing
    if app.config['TESTING']:
        app.register_blueprint(auth.bp)
    else:
        # Disable pre-request CSRF
        app.config['WTF_CSRF_CHECK_DEFAULT'] = False

        # Check csrf for session and http auth (but not token)
        app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = ["session", "basic"]

        # Enable CSRF protection
        csrf = CSRFProtect()
        csrf.init_app(app)
        app.config["SECURITY_CSRF_COOKIE_NAME"] = "XSRF-TOKEN"

        # Don't have csrf tokens expire (they are invalid after logout)
        app.config["WTF_CSRF_TIME_LIMIT"] = None

        # You can't get the cookie until you are logged in.
        app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
        # app.register_blueprint(csrf.exempt(auth.bp))
        app.register_blueprint(auth.bp)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return 'CSRF error - user forbidden', 403

    app.register_blueprint(directory.bp)
    app.register_blueprint(connections.bp)
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    return app
