from fastapi import APIRouter
from sentry_sdk import capture_exception

from . import core
from .. import schemas
from ..exceptions import CommonException

router = APIRouter()


@router.get('/check')
async def check_code(code: str) -> schemas.ResponseT:
    response = schemas.ResponseT()
    try:
        response.data = core.check_imei_code(code)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


@router.get('/record')
async def get_record_list(id: int, page: int = 1, offsets: int = 10, valid: bool = True) -> schemas.ResponseT:
    response = schemas.ResponseT()
    try:
        response.data = core.get_record(user_id=id, page=page, offsets=offsets, is_valid=valid)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


@router.get('/run')
async def sunny_run(code: str) -> schemas.ResponseT:
    response = schemas.ResponseT()
    try:
        response.data = core.run_sunny(code)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response
