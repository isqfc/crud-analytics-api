from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter(prefix='/sales', tags=['sales'])


@router.get('')
def read_sales():

    return {'sales': []}


@router.post('', status_code=HTTPStatus.CREATED)
def create_sale(id: int, sale: dict):

    return {'sale': {}}
