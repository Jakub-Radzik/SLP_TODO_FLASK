import pytest


@pytest.fixture(scope='module')
def new_user():
    user = {
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test_user@mail.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    return user


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)
