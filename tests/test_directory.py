import pytest
from flask import g
from flaskr.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash


def test_index(client, auth):
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
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_staff_member_admin_access(app, client, auth):
    """change a staff_members administrator acesses"""
    with app.app_context():
        db = get_db()
        db.execute('UPDATE staff_member SET system_administrator = 0 WHERE id = 2')
        db.commit()

    auth.login()
    # current user is not an administrator so can't delete staff member
    assert client.post('/directory/delete').status_code == 400
    # current user cant see delete as an option
    assert b'href="/directory/1/delete"' not in client.get('/directory/').data


@pytest.mark.parametrize('path', (
    '/directory/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 400

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

# def test_update(client,auth,app):
#     """Update a staff members record"""
#     auth.login()
#     assert client.get('/directory/12/update').status_code == 200
#     client.post('/directory/1/update', data={'title': 'Mr', 'preferred': 'Tester'})
#     with app.app_context():
#         db = get_db()
#         staff_member = db.execute('SELECT * FROM staff_member WHERE id = 2').fetchone()
#         assert staff_member['title'] == 'Mr'

# def test_change_password(client, auth, app):
#     auth.login()
#     password = generate_password_hash('Admin')
#     # assert client.get('/directory/1/update').status_code == 200
#     client.post('/directory/1/update', data={'password': password})

#     with app.app_context():
#         db = get_db()
#         user = db.execute('SELECT * FROM user WHERE id = 1').fetchone()
#         assert check_password_hash(user['password'], password) == True


@pytest.mark.parametrize('path', (
    '/directory/3/update',
))
def test_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'preferred': ''})
    assert b'Title is required.' in response.data

def test_delete(client, auth, app):
    """"Admin can delete a user"""
    auth.login()
    response = client.post('directory/delete')
    assert response.status_code == 400

    with app.app_context():
        db = get_db()
        response = client.post('directory/delete')
        staff_member = db.execute('SELECT * FROM staff_member WHERE email = "other"').fetchone()
        assert staff_member is None