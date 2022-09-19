import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/connections/')
    assert response.headers["Location"] == "/auth/login"
    assert response.status_code == 302

    auth.login()
    response = client.get('/connections/')
    assert b'Log Out' in response.data
    assert b'Posts' in response.data
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


def test_staff_member_admin_access(app, client, auth):
    """change post id"""
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET id = 10 WHERE id = 2')
        db.commit()

    auth.login()
    # current user is not an administrator so can't delete a post they did not create
    assert client.post('/connections/1/delete').status_code == 403
    # current user cant see delete as an option
    assert b'href="/connections/1/delete"' in client.get('/connections/').data


@pytest.mark.parametrize('path', (
    '/connections/1/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    #Tests that a user cannot delete a post they did not create
    assert client.post(path).status_code == 403

def test_create(client, auth, app):
    auth.login()
    assert client.get('/connections/create').status_code == 200
    # client.post('/connections/create', data={'title': 'My Title', 'body':'My Post Body','surname': 'Doe', 'preferred': 'JD', 'job_role': 'administrative assistant', 'email': 'example@email.com', 'system_administrator': 0 , 'department_id': 1})

#     with app.app_context():
#         db = get_db()
#         db.execute('DELETE FROM staff_member WHERE id != 1 and id !=2')
#         count = db.execute('SELECT COUNT(id) FROM staff_member').fetchone()[0]
#         assert count == 2

# def test_update(client,auth,app):
#     """Update functionality testing"""
#     auth.login()
#     assert client.get('/directory/2/update').status_code == 200
#     client.post('/directory/1/update', data={'title': 'Mr', 'preferred': 'Tester'})
#     with app.app_context():
#         db = get_db()
#         staff_member = db.execute('SELECT * FROM staff_member WHERE id = 2').fetchone()
#         assert staff_member['title'] == 'Mr'

# def test_change_password(client, auth, app):
#     auth.login()
#     assert client.get('/directory/2/update').status_code == 200
#     client.post('/directory/2/update', data={'title': 'Mr', 'preferred': 'Tester'})

#     with app.app_context():
#         db = get_db()
#         user = db.execute('SELECT * FROM user WHERE id = 2').fetchone()
#         assert check_password_hash(user['password'], password) == True


# @pytest.mark.parametrize('path', (
#     '/directory/1/update',
# ))
# def test_update_validate(client, auth, path):
#     auth.login()
#     response = client.post(path, data={'title': '', 'preferred': ''})
#     assert b'Title is required.' in response.data

# def test_delete(client, auth, app):
#     """"Admin can delete a user"""
#     auth.login()
#     response = client.post('directory/delete')
#     assert response.status_code == 200

#     with app.app_context():
#         db = get_db()
#         staff_member = db.execute('SELECT * FROM staff_member WHERE id = 1').fetchone()
#         assert staff_member is None