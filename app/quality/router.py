from fastapi import APIRouter
from fastapi_sqlalchemy import db
from starlette import status

from app import exceptions
from appDB import crud
from app import schemas
from app.quality import core
from app.schemas import ResponseT

router = APIRouter()


@router.post('/data', summary='获取素拓网活动记录')
async def quality_data(user: schemas.User, offline: bool = False):
    """
        获取素拓网活动记录
    - **username**: 用户名
    - **password**: 素拓网密码
    """
    response = ResponseT()
    try:
        if offline:
            raise exceptions.NetworkException("用户手动离线模式")
        cookie = core.get_cookie(**user.dict())
        response_data = core.get_all_activity(cookie)
        crud.update_quality_user(user, db.session)
        crud.update_quality_activity(user, response_data, db.session)
        response.data = response_data
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_quality_activity(user, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post('/report', summary='获取素拓网报告')
async def quality_report(user: schemas.User):
    cookie = core.get_cookie(**user.dict())
    return ResponseT(data=core.get_report(cookie))


@router.post('/scholarship', summary='获取指定学年奖学金加分情况')
async def quality_scholarship(user: schemas.User, year: int = 2020):
    cookie = core.get_cookie(**user.dict())
    return ResponseT(data=core.get_scholarship(cookie, year))
