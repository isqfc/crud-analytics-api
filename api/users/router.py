from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.utils import get_password_hash
from api.core.database import get_session
from api.core.models import User
from api.core.security import get_current_user
from api.users.schemas import FilterPage, UserList, UserPublic, UserSchema

# w key reference
router = APIRouter(prefix='/users', tags=['users'])
GetSession = Annotated[AsyncSession, Depends(get_session)]
Filter = Annotated[FilterPage, Query()]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/',
            status_code=HTTPStatus.OK,
            response_model=UserList
)
async def read_users(
    session: GetSession,
    filter_users: Filter
):
    """
    Endpoint to list all users on database
    """
    # Querry on DB
    users = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )

    return {'users': users}


@router.post('/',
             status_code=HTTPStatus.CREATED,
             response_model=UserPublic
)
async def create_user(
    user: UserSchema,
    session: GetSession
):
    """
    Endpoint to create a new user
    """

    # Checking if username or email already exists on DB
    user_db = await session.scalar(select(User).where(
        (User.username == user.username) | (User.email == user.email)
    ))

    # If username or email exits, return CONFLICT
    if user_db:
        if user.username == user_db.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists'
                )

        if user.email == user_db.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists'
                )
    # Creating new user by User model
    user_db = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)  # Hashing password
    )

    # Database commit
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return user_db


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    user: UserSchema,
    user_id: int,
    session: GetSession,
    current_user: CurrentUser
):

    # ID Check
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail='Not enough permissions')

    # Checking if email or username exists on DB
    check_user_list = await session.scalars(select(User).where(
        (User.email == user.email) | (User.username == user.username)))

    if check_user_list:
        for check_user in check_user_list:
            if check_user.username == user.username:
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                    detail='Email or Username already exists')

            elif check_user.email == user.email:
                raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                    detail='Email or Username already exists')

    # Hashing new password
    hash_password = get_password_hash(user.password)
    user.password = hash_password

    # Setting new attributes in current user
    for key, value in user:
        setattr(current_user, key, value)

    await session.commit()
    await session.refresh(current_user)
    return current_user
