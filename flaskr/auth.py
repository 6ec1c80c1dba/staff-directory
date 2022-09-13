import functools
from xml.dom import InvalidAccessErr

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)
from werkzeug.exceptions import abort, HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
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
                staff_member = db.execute(
                    'SELECT * FROM staff_member WHERE email = ?', (username, )
                ).fetchone()
                if staff_member:
                    db.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
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
        username = request.form['username']
        session["username"] = request.form.get("username")
        session["name"] = "Testing"
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username, )
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

    return render_template('auth/login.html')


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
    return redirect(url_for('index'))

def login_required(view):
    """A user must be logged in to not access the full application."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


