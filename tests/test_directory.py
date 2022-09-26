import pytest
from flask import g
from flaskr.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash


def test_index(client, auth):
    """Tests actual return of staff directory pages with expcted contents"""
    response = client.get('/directory/')
    assert response.headers["Location"] == "/auth/login"
    assert response.status_code == 302

    auth.login()
    response = client.get('/directory/')
    assert b'Log Out' in response.data
    assert b'Staff Directory' in response.data
    assert b'Title' in response.data
    assert b'Email' in response.data

@pytest.mark.parametrize('path', (
    '/directory/create',
    '/directory/1/change_password',
    '/directory/1/update/',
    '/directory/delete'
))
def test_login_required(client, path):
    """Tests that all directory endpoints require a user to be logged in"""
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_staff_member_admin_access(app, client, auth):
    """change a staff_members administrator acesses"""
    auth.login()
    # current user is not an administrator so can't delete staff member
    assert client.post('/directory/delete').status_code == 400
    # current user cant see delete as an option
    assert b'href="/directory/1/delete"' not in client.get('/directory/').data
    with app.app_context():
        db = get_db()
        db.execute('UPDATE staff_member SET system_administrator = 1 WHERE id = 3')
        db.commit()
    # current user now an admin so can see delete as an option
    assert b'href="/directory/delete"' in client.get('/directory/').data


def test_create(client, auth, app):
    auth.login()
    """Create a post"""
    assert client.get('/directory/create').status_code == 200
    client.post('/directory/create', data={'title': 'miss', 'first_name':'Jane','surname': 'Doe', 'preferred': 'JD', 'job_role': 'administrative assistant', 'email': 'example@email.com', 'system_administrator': 0 , 'department_id': 1})

    with app.app_context():
        db = get_db()
        db.execute('DELETE FROM staff_member WHERE id != 1 and id !=2')
        count = db.execute('SELECT COUNT(id) FROM staff_member').fetchone()[0]
        assert count == 2

def test_update(client,auth,app):
    """Update a staff members record"""
    auth.login()
    client.post('/directory/13/update', data={'title': 'Mr', 'preferred': 'Jon'})
    with app.app_context():
        db = get_db()
        staff_member = db.execute('SELECT * FROM staff_member WHERE id = 13').fetchone()
        assert staff_member['title'] == 'Mr'

def test_change_password(client, auth, app):
    auth.login()
    password = generate_password_hash('Admin')
    client.post('/directory/12/update', data={'password': password})


def test_delete(client, auth, app):
    """"Admin can delete a user"""
    auth.login()

    with app.app_context():
        db = get_db()
        response = client.post('directory/delete')
        staff_member = db.execute('SELECT * FROM staff_member WHERE email = "other"').fetchone()
        assert staff_member is None