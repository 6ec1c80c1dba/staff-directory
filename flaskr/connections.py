from logging import exception
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, json
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.directory import get_staff_member

bp = Blueprint('connections', __name__, url_prefix='/connections')


@bp.route('/')
@login_required
def index():
    """Returns all posts on the message board"""
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created_by, department_collection, posted_on, username, staff_id '
        ' FROM post p JOIN user u ON p.created_by = u.id'
        ' ORDER BY posted_on ASC'
    ).fetchall()
    department = db.execute(
        'SELECT d.id, department_name'
        ' FROM department d JOIN post p ON d.id = p.department_collection'
    ).fetchone()
    current_staff_member = db.execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, system_administrator'
        ' FROM staff_member s JOIN user u ON s.id = u.staff_id'
        ' WHERE s.id = ?',
        (g.user['staff_id'],)
    ).fetchone()

    return render_template('connections/index.html', posts=posts, department=department, current_staff_member=current_staff_member)


def get_post(id, check_user=True):
    """Function to return all posts for a department"""
    post = get_db().execute(
        'SELECT p.id, title, body, created_by, department_collection, posted_on'
        ' FROM post p'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    staff_member = get_db().execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, system_administrator'
        ' FROM staff_member s JOIN user u ON s.id = u.staff_id'
        ' WHERE s.id = ?',
        (g.user['staff_id'],)
    ).fetchone()
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if post['created_by'] != g.user['id']:
        if staff_member['system_administrator'] == 0:
            abort(403)

    return post


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Lets users make new posts to connections"""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Please include a Title for your post.'

        if not body:
            error = 'Please include text for the body of your post.'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, created_by, department_collection)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], g.user['department_id'])
            )
            db.commit()
            return redirect(url_for('connections.index'))

    return render_template('connections/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Users can update their posts."""
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('connections.index'))

    return render_template('connections/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    """Users and admins can delete posts."""
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('connections.index'))
