from fastapi import APIRouter

router = APIRouter(prefix='/sales', tags=['sales'])


@router.get('')
def read_sales():
    pass