from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.schemas import Token
from api.auth.utils import create_access_token, verify_hashed_password
from api.core.database import get_session
from api.core.models import User

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
GetSession = Annotated[AsyncSession, Depends(get_session)]


@router.post('/token',
            status_code=HTTPStatus.OK,
            response_model=Token
)
async def login_to_get_token(
    form_data: OAuth2Form,
    session: GetSession
):
    """
    Endpoint to login & get his token
    """
    user = await session.scalar(select(User).where(
        User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials'
            )

    if not verify_hashed_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials'
            )

    token = create_access_token(data={'sub': user.email})
    return {'access_token': token,
            'token_type': 'bearer'}
