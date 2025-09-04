from http import HTTPStatus


def test_read_all_users(client):

    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}
