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
    """Renders the homepage for logged in users"""
    db = get_db()
    current_staff_member = db.execute(
        'SELECT s.id, title, first_name, last_name, preferred, job_role, email, system_administrator'
        ' FROM staff_member s JOIN user u ON s.id = u.staff_id'
        ' WHERE s.id = ?',
        (g.user['staff_id'],)
    ).fetchone()
    return render_template('index.html', current_staff_member=current_staff_member)
