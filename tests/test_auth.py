import pytest
from flask import g, session
from flaskr.db import get_db


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session