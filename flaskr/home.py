from logging import exception
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    """Renders the homepage"""
    db = get_db()
    staff_member = db.execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, department_id, extension_number, username'
        ' FROM staff_member s JOIN user u ON s.email = u.username'
    ).fetchone()
    return render_template('index.html',staff_member = staff_member)