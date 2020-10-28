from fastapi import APIRouter

from app import schemas
from app.quality.core import get_report, get_cookie, get_all_activity
from app.schemas import ResponseT

router = APIRouter()


@router.post('/data', )
async def quality_report(user: schemas.User):
    response = ResponseT()
    cookie = get_cookie(**user.dict())
    data_dict = {
        'report': get_report(cookie),
        'activity': get_all_activity(cookie),
        # 'scholarship': get_scholarship(cookie)
    }
    response.data = data_dict
    return response


@router.post('/report', )
async def quality_report(user: schemas.User):
    response = ResponseT()
    cookie = get_cookie(**user.dict())
    response.data = get_report(cookie)
    return response
