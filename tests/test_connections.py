import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/connections/')
    assert response.headers["Location"] == "/auth/login"
    assert response.status_code == 302

    auth.login()
    response = client.get('/connections/')
    assert b'Log Out' in response.data
    assert b'Connect' in response.data
    assert b'Staff Directory' in response.data


@pytest.mark.parametrize('path', (
    '/connections/create',
    '/connections/1/update',
    '/connections/1/delete'
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"
    assert response.status_code == 302


def test_staff_member_admin_access(client, auth, app):
    """change post id"""
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET id = 10 WHERE id = 2')
        db.commit()

    auth.login()
    # current user can see delete as an option for the post they made
    assert b'href="/connections/1/delete"' in client.get('/connections/').data


@pytest.mark.parametrize('path', (
    '/connections/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    # Tests that a user cannot delete a post they did not create
    assert client.post(path).status_code == 404

def test_create(client, auth, app):
    auth.login()
    assert client.get('/connections/create').status_code == 200
    client.post('/connections/create', data={'title': 'My Title', 'body':'My Post Body', 'created_by': 'other', 'department_collection': 2})

    with app.app_context():
        db = get_db()
        db.execute('DELETE FROM post WHERE id = 2')
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 1

def test_update(client,auth,app):
    """Update Post"""
    auth.login()
    assert client.get('/connections/1/update').status_code == 200
    client.post('/connections/1/update', data={'title': 'My New Title', 'body': 'My updated post content'})
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'My New Title'


# def test_delete(client, auth, app):
#     """"User can delete a post they made"""
#     auth.login()
#     response = client.post('/connections/1/delete')
#     assert response.status_code == 200

#     with app.app_context():
#         db = get_db()
#         staff_member = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
#         assert staff_member is None