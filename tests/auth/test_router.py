from http import HTTPStatus


def test_login_to_get_token(client, user):

    response = client.post('/auth/token',
                           data={
                               'username': user.email,
                                'password': user.plain_password})

    assert response.status_code == HTTPStatus.OK
