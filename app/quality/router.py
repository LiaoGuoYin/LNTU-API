from fastapi import APIRouter

from app import schemas
from app.quality import core
from app.schemas import ResponseT

router = APIRouter()


@router.post('/data', summary='获取素拓网活动记录，及指定学年奖学金加分表')
async def quality_report(user: schemas.User, year: int = 2020):
    response = ResponseT()
    cookie = core.get_cookie(**user.dict())
    data_dict = {
        # 'report': core.get_report(cookie),
        'activity': core.get_all_activity(cookie),
        'scholarship': core.get_scholarship(cookie, year)
    }
    response.data = data_dict
    return response


@router.post('/report', summary='获取素拓网报告')
async def quality_report(user: schemas.User):
    response = ResponseT()
    cookie = core.get_cookie(**user.dict())
    response.data = core.get_report(cookie)
    return response
