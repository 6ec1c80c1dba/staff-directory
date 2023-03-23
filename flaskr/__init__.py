import os

from flask import Flask, render_template_string, Response
from flask_security import Security, current_user, auth_required, \
     SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
from flask_talisman import Talisman

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
        )
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    # Lowering the value of session cookie lifetimes will help mitigate replay attacks, where intercepted cookies can be sent at a later time
    PERMANENT_SESSION_LIFETIME=600,
)
# Set headers for increased security
response = Response()
# added these lines to protect against cookie attack vectors in our Flask configuration.
response.set_cookie('username', 'flask', secure=True,
                        httponly=True, samesite='Lax')
response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
# Prevents external sites from embedding the mediacentral site in an iframe. 
response.headers['X-Frame-Options'] = 'SAMEORIGIN'
# Protects against XSS
response.headers['X-Content-Type-Options'] = 'nosniff'
# Implements 'very strict' CSP policy
response.headers['Content-Security-Policy'] = "default-src 'self'"

Talisman(app)

# Setup Flask-Security
app.security = Security(app, app.config['DATABASE'])


#  Mitigate this attack by configuring the flask Jinja2 to auto escape all inputs by setting autoescaping set to True
app.jinja_env.autoescape = True



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

if __name__ == '__main__':
    # run application (can also use flask run)
    app.run(test_config=None, ssl_context='adhoc')
