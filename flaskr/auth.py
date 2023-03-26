import functools
from tokenize import group

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json, Response
)
from werkzeug.exceptions import abort, HTTPException
from werkzeug.security import check_password_hash, generate_password_hash
import re
from flask import current_app
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
app = current_app
@bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON format for improved readability in error logging instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    response.set_cookie('username', 'flask', secure=True,
                        httponly=True, samesite='Lax')
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.set_cookie('snakes', '3', max_age=600)
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.set_cookie('snakes', '3', max_age=600)
    return response


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Allow a new user to register for an acount."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                db = get_db()
                pattern = re.compile("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
                valid = pattern.match(username)
                if valid:
                    email = username
                else:
                    error = f"User {username} is not valid."
                staff_member = db.execute(
                    'SELECT s.id, email, system_administrator, in_department'
                    ' FROM staff_member s'
                    ' WHERE email = "%s"'
                    % (email)
                ).fetchone()
                if staff_member:
                    db.execute(
                        "INSERT INTO user (username, password, department_id, staff_id ) VALUES (?, ?, ?, ?)",
                        (username, generate_password_hash(password), int(
                            staff_member['in_department']), int(staff_member['id'])),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            if staff_member is None:
                error = f"User {username} is not a staff_member"
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Function to take in user input and check against the database to enable the user to login."""
    if request.method == 'POST':
        session.clear()
        username = request.form['username']
        session["username"] = request.form.get("username")
        session["name"] = "Testing"
        password = request.form['password']
        session.permanent = True
        pattern = re.compile("^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$")
        valid = pattern.match(username)
        if valid:
            email = username
        else:
            error = f"User {username} is not valid."
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (email, )
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['staff_id'] = user['staff_id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', testing=app.config['TESTING'])


@bp.before_app_request
def load_logged_in_user():
    """Funtion to load the logged in user if the session has a user id"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    """Logout the current user and remove all session data."""
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    """A user must be logged in to not access the full application."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
