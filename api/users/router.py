from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.auth.utils import get_password_hash
from api.core.database import get_session
from api.core.models import User
from api.users.schemas import FilterPage, UserList, UserPublic, UserSchema

# w key reference
router = APIRouter(prefix='/users', tags=['users'])
GetSession = Annotated[Session, Depends(get_session)]
Filter = Annotated[FilterPage, Query()]


@router.get('/',
            status_code=HTTPStatus.OK,
            response_model=UserList
)
def read_users(
    session: GetSession,
    filter_users: Filter
):
    """
    Endpoint to list all users on database
    """
    users = session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )

    return {'users': users}


@router.post('/',
             status_code=HTTPStatus.OK,
             response_model=UserPublic
)
def create_user(
    user: UserSchema,
    session: GetSession
):
    user_db = session.scalar(select(User).where(
        (User.username == user.username) | (User.email == user.email)
    ))

    if user_db:
        if user.username == user_db.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists'
                )

        if user.username == user_db.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists'
                )

    user_db = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db
