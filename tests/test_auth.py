from email.quoprimime import header_length
from pathlib import Path
from wsgiref.headers import Headers
import pytest
from flask import g, session
from flaskr.db import get_db


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', 'admin', b'Username is required.'),
    ('test', '', b'Password is required.'),
    ('test@email.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', b'login')
))
def test_register_validate_input(app, client, username, password, message):
    """Testing user reigstration functionality"""
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test@email.com'",
        ).fetchone() is not None

def test_login(client, auth):
    """Test to identify current user details"""
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 3
        assert g.user['staff_id'] == 12
        assert g.user['username'] == 'test@email.com'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a@email.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', b'Incorrect username.'),
    ('john@email.com', 'a', b'Incorrect password.'),
    ('test@email.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', b'login')
))

def test_login_validate_input(auth, username, password, message):
    """Testing user login functionality"""
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    """Tests logging out a user"""
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session