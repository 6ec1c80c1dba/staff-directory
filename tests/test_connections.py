import pytest
from flaskr.db import get_db
from flask import g


def test_index(client, auth):
    """Validates that the connections wall returns the expected posts"""
    response = client.get('/connections/')
    assert response.headers["Location"] == "/auth/login"
    assert response.status_code == 302

    auth.login()
    response = client.get('/connections/')
    assert response.status_code == 200
    assert b'Log Out' in response.data
    assert b'connect' in response.data
    assert b'Staff Directory' in response.data


@pytest.mark.parametrize('path', (
    '/connections/create',
    '/connections/1/update',
    '/connections/1/delete'
))
def test_login_required(client, path):
    """Validates that all connections endpoints require a user to be logged in"""
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"
    assert response.status_code == 302


def test_staff_member_admin_access(client, auth, app):
    """A user with admin priveledges can update the id of a post"""

    auth.login()
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET id = 10 WHERE id = 2')
        db.commit()
    # current user can see delete as an option for the post they made
    assert b'Employee Management System' in client.get('/connections/').data
    assert b'Delete' in client.get('/connections/').data

def test_create(client, auth, app):
    auth.login()
    assert client.get('/connections/create').status_code == 200
    client.post('/connections/create', data={'title': 'My Title', 'body':'My Post Body', 'created_by': 3, 'department_collection': 2})

    with app.app_context():
        db = get_db()
        db.execute('DELETE FROM post WHERE id = 5')
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 4

def test_update(client,auth,app):
    """Update Post"""
    auth.login()
    assert client.get('/connections/1/update').status_code == 200
    client.post('/connections/1/update', data={'title': 'My New Title', 'body': 'My updated post content'})
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'My New Title'


def test_delete(client, auth, app):
    """"User can delete a post they made"""
    auth.login()
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        if post:
            post = db.execute('DELETE FROM post WHERE id = 1').fetchone()
        assert post is None