
from jwt import decode

from api.core.settings import Settings


def test_create_access_token(access_token, input_user):

    token = access_token(data={'sub': input_user['email']})
    decoded_jwt = decode(
        token,
        key=Settings().SECRET_KEY,
        algorithms=[Settings().ALGORITHM])

    print(decoded_jwt)

    assert 'exp' in decoded_jwt
    assert decoded_jwt['sub'] == input_user['email']
