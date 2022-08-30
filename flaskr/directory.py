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
    staff_members = db.execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, department_id, extension_number, username'
        ' FROM staff_member s JOIN user u ON s.id = u.staff_id'
        ' ORDER BY s.id DESC'
    ).fetchall()
    # department = get_db().execute(
    #     'SELECT d.id, department_name, location_id'
    #     ' FROM department d JOIN staff_member s ON d.id = s.department_id'
    #     ' WHERE d.id = ?',
    #         (id,)
    # ).fetchone()
    # Must add department to render template when functional
    return render_template('directory/index.html', staff_members=staff_members)

def get_staff_member(id, check_staff_member=True):
    staff_member = get_db().execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, username'
        ' FROM staff_member s JOIN user u ON s.id = u.staff_id'
        ' WHERE s.id = ?',
        (id,)
    ).fetchone()

    if staff_member is None:
        abort(404, f"Staff id {id} doesn't exist.")

    if staff_member and staff_member['id'] != g.user['id']:
        abort(403)

    return staff_member

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        preferred = request.form['preferred']
        job_role = request.form['job_role']
        email = request.form['email']
        extension_number = request.form['extension_number']
        system_administrator = request.form['system_administrator']
        department_id = request.form['department_id']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO staff_member (title, first_name, last_name, preferred, job_role, email, extension_number, system_administrator, department_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (title, first_name, last_name, preferred, job_role, email, extension_number, system_administrator, department_id)
            )
            db.execute(
                'INSERT INTO user (username)'
                ' VALUES (?)',
                (email)
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
                'UPDATE staff_member SET title = ?, preferred = ?'
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


