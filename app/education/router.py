from fastapi import APIRouter

from app import schemas
from app.common import notice
from app.education.core import get_stu_info, get_class_table, get_grade, get_grade_table, login
from app.exceptions import CommonException
from app.schemas import ResponseT

router = APIRouter()


@router.get("/")
async def home():
    return {"API-location": "/education/"}


# Online Operation Mode
# data = info + class-table + grade + grade-table
@router.post("/data", response_model=ResponseT)
async def refresh_education_data(user: schemas.User, semesterId: int = 627):
    response = ResponseT()
    try:
        session = login(**user.dict())
        data = {
            'info': get_stu_info(**user.dict(), session=session),
            'classTable': get_class_table(**user.dict(), session=session, semesterId=semesterId),
            # 'grade': get_grade(**user.dict(), session=session, semesterId=semesterId - 1),  # TODO: other semester
            'gradeTable': get_grade_table(**user.dict(), session=session),
        }
        response.data = data
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response


@router.post("/info", response_model=ResponseT)
async def refresh_education_info(user: schemas.User):
    response = ResponseT()
    try:
        response.data = get_stu_info(**user.dict())
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response


@router.post("/class-table", response_model=ResponseT)
async def refresh_education_class_table(user: schemas.User, semesterId: int = 627):
    response = ResponseT()
    try:
        response.data = get_class_table(**user.dict(), semesterId=semesterId)
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response


@router.post("/grade", response_model=ResponseT)
async def refresh_education_grade(user: schemas.User, semesterId: int = 626):
    response = ResponseT()
    try:
        response.data = get_grade(**user.dict(), semesterId=semesterId)
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response


@router.post("/grade-table", response_model=ResponseT)
async def refresh_education_grade(user: schemas.User):
    response = ResponseT()
    try:
        response.data = get_grade_table(**user.dict())
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response


@router.get("/notice", )
async def refresh_notice(limit: int = 10):
    response = ResponseT()
    try:
        response.data = notice.run()
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response
