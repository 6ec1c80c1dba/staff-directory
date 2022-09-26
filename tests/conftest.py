import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Defining the app for testing"""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Defining the client for testing"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Defining the runner for testing"""
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        """Initialise the test suite"""
        self._client = client

    def login(self, username='test', password='test'):
        """Defines user to login with for auth"""
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        """Logs out the current user"""
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """Includes client parameters for auth functionality"""
    return AuthActions(client)