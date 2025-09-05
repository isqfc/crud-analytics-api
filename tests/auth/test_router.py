from http import HTTPStatus


def test_login_to_get_token(client, user):

    response = client.post('/auth/token',
                           data={
                               'username': user.email,
                                'password': user.plain_password})

    assert response.status_code == HTTPStatus.OK
    assert response.json()['token_type'] == 'bearer'


def test_login_to_get_token_username_exception(client, user):

    response = client.post('/auth/token',
                           data={
                               'username': 'johntester@test.com',
                               'password': user.plain_password
                           })

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_login_to_get_token_password_exception(client, user):

    response = client.post('/auth/token',
                           data={
                               'username': user.email,
                               'password': 'hackerinjectertry'
                           })

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
