from fastapi import APIRouter
from sentry_sdk import capture_exception

from app import schemas, exceptions
from app.quality.core import get_report, get_cookie, get_all_activity
from app.schemas import ResponseT

router = APIRouter()


@router.post('/data', )
async def quality_report(user: schemas.User):
    response = ResponseT()
    try:
        cookie = get_cookie(**user.dict())
        data_dict = {
            'report': get_report(cookie),
            'activity': get_all_activity(cookie),
            # 'scholarship': get_scholarship(cookie)
        }
        response.data = data_dict
    except exceptions.CommonException as e:
        capture_exception(e)
        response.code, response.message = e
    return response


@router.post('/report', )
async def quality_report(user: schemas.User):
    response = ResponseT()
    try:
        cookie = get_cookie(**user.dict())
        response.data = get_report(cookie)
    except exceptions.CommonException as e:
        capture_exception(e)
        response.code, response.message = e
    return response
