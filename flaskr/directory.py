from logging import exception
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('directory', __name__, url_prefix='/directory')

 

@bp.route('/')
def index():
    db = get_db()

    staff_members = db.execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, department_id, extension_number, username'
        ' FROM staff_member s JOIN user u ON s.id = u.staff_id'
        ' ORDER BY s.id DESC'
    ).fetchall()

    department = db.execute(
        'SELECT d.id, department_name'
        ' FROM department d JOIN staff_member s ON d.id = s.department_id'
    ).fetchone()

    return render_template('directory/index.html',
    staff_members=staff_members, department = department)

def get_staff_member(staff_id, check_staff_member=True):
    staff_member = get_db().execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, username'
        ' FROM staff_member s JOIN user u ON s.id = u.staff_id'
        ' WHERE s.id = ?',
        (staff_id,)
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
            db.commit()
            return redirect(url_for('directory.index'))

    return render_template('directory/create.html')

@bp.route('/<int:id>/update/', methods=('GET', 'POST'))
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
    return render_template('directory/update.html', staff_member = staff_member)


@bp.route('/<int:id>/change_password', methods=('GET', 'POST'))
@login_required
def change_password(id):
    staff_member = get_staff_member(id)
    if request.method == 'POST':
        password = request.form['password']
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (staff_member['email'], )
        ).fetchone()
        if not password:
            error = 'Please fill in the box below with your new password.'
        if check_password_hash(user['password'], generate_password_hash(password)):
            error = "This password has been used previously"
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET password = ?'
                ' WHERE staff_id = ?',
                (generate_password_hash(password), id,)
            )
            db.commit()
            return redirect(url_for('directory.index'))
    return render_template('directory/change_password.html', staff_member = staff_member)

@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    if request.method == 'POST':
        username = request.form['username']
        error = None

        if not username:
            error = 'Username is required to find user.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('DELETE FROM staff_member WHERE email = ?', (username,))
            db.commit()
            return redirect(url_for('directory.index'))
            
    return render_template('directory/delete.html')

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_user(id):
    get_staff_member(id)
    db = get_db()
    db.execute('DELETE FROM staff_member WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('directory.index'))


