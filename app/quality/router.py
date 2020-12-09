from fastapi import APIRouter

from app import schemas
from app.quality import core
from app.schemas import ResponseT

router = APIRouter()


@router.post('/data', summary='获取素拓网活动记录')
async def quality_data(user: schemas.User):
    cookie = core.get_cookie(**user.dict())
    return ResponseT(data=core.get_all_activity(cookie))


@router.post('/report', summary='获取素拓网报告')
async def quality_report(user: schemas.User):
    cookie = core.get_cookie(**user.dict())
    return ResponseT(data=core.get_report(cookie))


@router.post('/scholarship', summary='获取指定学年奖学金加分情况')
async def quality_scholarship(user: schemas.User, year: int = 2020):
    cookie = core.get_cookie(**user.dict())
    return ResponseT(data=core.get_scholarship(cookie, year))
