import pytest


def test_index(client, auth):
    response = client.get('/')
    assert response.headers["Location"] == "/auth/login"
    assert response.status_code == 302

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Staff Directory' in response.data
    assert b'Welcome' in response.data