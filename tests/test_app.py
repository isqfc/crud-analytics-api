from http import HTTPStatus


def test_read_root(client):

    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.text == """
    <!DOCTYPE html>
    <html>
    <head>
    <title>API Online</title>
    </head>
    <body>
    <h1>Endpoints</h1>
    <p>Interesting Sales Endpoints.</p>
    <ul>
        {}
    </ul>
    </body>
    </html>
    """
