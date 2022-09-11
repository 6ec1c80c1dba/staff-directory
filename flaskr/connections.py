from logging import exception
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, json
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('connections', __name__, url_prefix='/connections')

@bp.route('/')
def index():
    """Returns all posts on the message board for Department"""
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created_by, posted_on, department'
        ' FROM post p JOIN department d ON p.department = d.department_name'
        ' ORDER BY p.id DESC'
    ).fetchall()
    return render_template('connections/index.html', posts=posts)

def get_post(department_id, check_user=True):
    """Function to return all posts for a department"""
    post = get_db().execute(
        'SELECT p.id, title, body, created_by, department, created_on'
        ' FROM post p JOIN departments d ON p.department = d.department_name'
        ' WHERE p.department = ?',
        (department_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_user and post['created_by'] != g.user['username']:
        abort(403)

    return post

def get_staff_member(username, check_user=True):
    """Function to return staff_member detail """
    staff_member = get_db().execute(
        'SELECT s.email, department_id'
        ' FROM staff_member s JOIN user u ON s.email = u.username'
        ' WHERE s.email = ?',
        (username,)
    ).fetchone()

    if staff_member is None:
        abort(404, f"Staff Member {username} doesn't exist.")

    if check_user and staff_member['email'] != g.user['username']:
        abort(403)

    return staff_member

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Lets users make new posts to connections wall."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        staff_member = get_staff_member(g.user['username'])
        department = staff_member['department_id']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, created_by, department)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['username'], department)
            )
            db.commit()
            return redirect(url_for('connections.index'))

    return render_template('connections/create.html')