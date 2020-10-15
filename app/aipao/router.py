from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sentry_sdk import capture_exception

from appDB import crud
from . import core
from .. import schemas
from ..exceptions import CommonException

router = APIRouter()


@router.get('/check')
async def check_code(code: str) -> schemas.ResponseT:
    response = schemas.ResponseT()
    try:
        response_data = core.check_imei_code(code)
        crud.update_aipao_order(response_data, session=db.session)
        response.data = response_data.dict(exclude={'token'})
        response.data.update({
            'url': f'http://sportsapp.aipao.me/Manage/UserDomain_SNSP_Records.aspx/MyResutls?userId={response_data.id}'
        })
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
        crud.update_aipao_order(core.check_imei_code(code), session=db.session)
        response.data = core.run_sunny(code)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response
