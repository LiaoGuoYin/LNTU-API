from fastapi import APIRouter

from app import schemas
from app.quality import core
from app.schemas import ResponseT

router = APIRouter()


@router.post('/data', )
async def quality_report(user: schemas.User, year=2020):
    response = ResponseT()
    cookie = core.get_cookie(**user.dict())
    data_dict = {
        # 'report': core.get_report(cookie),
        'activity': core.get_all_activity(cookie),
        'scholarship': core.get_scholarship(cookie, year)
    }
    response.data = data_dict
    return response


@router.post('/report', )
async def quality_report(user: schemas.User):
    response = ResponseT()
    cookie = core.get_cookie(**user.dict())
    response.data = core.get_report(cookie)
    return response
