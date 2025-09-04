from http import HTTPStatus


def test_read_sales(client):

    response = client.get('/sales')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'sales': []}
