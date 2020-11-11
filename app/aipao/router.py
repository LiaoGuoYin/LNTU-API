from fastapi import APIRouter
from fastapi_sqlalchemy import db

from appDB import crud
from app.aipao import core
from app import schemas, exceptions

router = APIRouter()


@router.get('/record')
async def get_record_list(id: int, page: int = 1, offsets: int = 10, valid: bool = True) -> schemas.ResponseT:
    response = schemas.ResponseT(data=core.get_record(user_id=id, page=page, offsets=offsets, is_valid=valid))
    return response


@router.get('/check')
async def check_code(code: str) -> schemas.ResponseT:
    response = schemas.ResponseT()
    user = core.check_imei_code(code)
    if not user.isCodeValid:
        raise exceptions.FormException("IMEICode 无效")
    response.data = user.dict(exclude={'token'})
    crud.update_aipao_order(user, session=db.session)
    return response


@router.get('/run')
async def sunny_run(code: str) -> schemas.ResponseT:
    response = schemas.ResponseT()
    user = core.check_imei_code(code)
    if not user.isCodeValid:
        raise exceptions.FormException("IMEICode 无效")
    elif user.isDoneToday:
        raise exceptions.FormException("今天已有有效跑步记录")
    else:
        response.data = core.run_sunny(code)
        user = core.check_imei_code(code)
    crud.update_aipao_order(user, session=db.session)
    return response
