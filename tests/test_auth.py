from email.quoprimime import header_length
from pathlib import Path
from wsgiref.headers import Headers
import pytest
from flask import g, session
from flaskr.db import get_db


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', 'admin', b'Username is required.'),
    ('test', '', b'Password is required.'),
    ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', b'login')
))
def test_register_validate_input(app, client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert b'submit' in response.data
    assert message in response.data
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test'",
        ).fetchone() is not None

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 3
        assert g.user['username'] == 'test'


# @pytest.mark.parametrize(('username', 'password', 'message'), (
#     ('a@email.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', b'Incorrect username.'),
#     ('test@mediacentral.com', 'a', b'Incorrect password.'),
# ))
# def test_login_validate_input(auth, username, password, message):
#     response = auth.login(username, password)
#     assert message in response.data

# def test_logout(client, auth):
#     auth.login()

#     with client:
#         auth.logout()
#         assert 'user_id' not in session