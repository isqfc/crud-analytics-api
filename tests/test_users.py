from http import HTTPStatus

from api.users.schemas import UserPublic


def test_read_all_users(client, user):

    user_list = UserPublic.model_validate(user).model_dump()
    response = client.get('/users', params='offset=0&limit=100')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_list]}
