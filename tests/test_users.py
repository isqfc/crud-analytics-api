from http import HTTPStatus

from api.users.schemas import UserPublic


# w key reference
def test_read_all_users(client, user):

    user_list = UserPublic.model_validate(user).model_dump()
    response = client.get('/users', params='offset=0&limit=100')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_list]}


def test_create_user(client, input_user, output_user):

    response = client.post('/users', json=input_user)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == output_user


def test_create_user_username_exception(client, user):

    new_user = {'username': user.username,
                'email': 'test@test.com',
                'password': 'testest123'}
    response = client.post('/users', json=new_user)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_exception(client, user):

    new_user = {'username': 'john tester smith',
                'email': user.email,
                'password': 'testest123'}

    response = client.post('/users', json=new_user)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}
