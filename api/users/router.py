from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas import UserPublic, UserSchema, UserList, FilterPage
from api.core.models import User
from api.core.database import get_session


router = APIRouter(prefix='/users', tags=['users'])
GetSession = Annotated[Session, Depends(get_session)]



@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: GetSession,
    filter_users: FilterPage
):
    """
    Endpoint to list all users based on UserList on database
    """
    users = session.scalars(select(User).offset(filter_users.offset).limit(filter_users.limit))

    return {'users': users}