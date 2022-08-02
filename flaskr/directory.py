from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('directory', __name__)

@bp.route('/')
def index():
    db = get_db()
    staff_member = db.execute(
        'SELECT p.id, staff_id, title, full_name, preferred, job_role, email, username'
        ' FROM staff_member p JOIN user u ON p.staff_id = u.id'
        ' ORDER BY staff_id DESC'
    ).fetchall()
    return render_template('directory/index.html', staff_member=staff_member)

def get_staff_member(id, check_staff_member=True):
    staff_member = get_db().execute(
        'SELECT p.id, staff_id, title, full_name, preferred, job_role, email, username'
        ' FROM staff_member p JOIN user u ON p.staff_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if staff_member is None:
        abort(404, f"Staff id {id} doesn't exist.")

    if staff_member and staff_member['staff_id'] != g.user['id']:
        abort(403)

    return staff_member

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        preferred = request.form['preferred']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, preferred, staff_id)'
                ' VALUES (?, ?, ?)',
                (title, preferred, g.user['id'])
            )
            db.commit()
            return redirect(url_for('directory.index'))

    return render_template('directory/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    staff_member = get_staff_member(id)

    if request.method == 'POST':
        title = request.form['title']
        preferred = request.form['preferred']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, preferred = ?'
                ' WHERE id = ?',
                (title, preferred, id)
            )
            db.commit()
            return redirect(url_for('directory.index'))

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_staff_member(id)
    db = get_db()
    db.execute('DELETE FROM staff_member WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('directory.index'))


