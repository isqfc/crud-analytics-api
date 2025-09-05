from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.auth.utils import decode_jwt
from api.core.database import get_session
from api.core.models import User

OAuth2Schema = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='/auth/token'))] # noqa
GetSession = Annotated[Session, Depends(get_session)]


def get_current_user(
        session: GetSession,
        token: OAuth2Schema
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
        )

    try:
        payload = decode_jwt(token)
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user_db = session.scalar(select(User).where(User.email == subject_email))
    if not user_db:
        raise credentials_exception

    return user_db


def get_current_admin(
        session: GetSession,

):
    pass
