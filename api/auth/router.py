from fastapi import APIRouter

router = APIRouter(prefix='auth', tags=['auth'])


@router.post('/token', )
def create_access_token():
    return {'token': '1234'}
