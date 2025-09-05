from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import decode, encode
from pwdlib import PasswordHash

from api.core.settings import Settings

pass_context = PasswordHash.recommended()


# w reference
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACESS_TOKEN_EXPIRE_TIME
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode,
        key=Settings().SECRET_KEY,
        algorithm=[Settings().ALGORITHM]
    )

    return encoded_jwt


def get_password_hash(password: str):
    return pass_context.hash(password)


def verify_hashed_password(plain_password: str, hashed_password: str):
    return pass_context.verify(plain_password, hashed_password)


def decode_jwt(token: str):
    return decode(
        token,
        key=Settings().SECRET_KEY,
        algorithms=[Settings().ALGORITHM]
        )
