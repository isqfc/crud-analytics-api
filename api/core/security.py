from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.core.database import get_session

oauth2_schema = OAuth2PasswordBearer(tokenurl='token')

GetSession = Annotated[Session, Depends(get_session)]


def get_current_user(
        session: GetSession,
        token: str = Depends(oauth2_schema)
):
    pass
