from fastapi import APIRouter

from app import schemas
from app.education.core import get_stu_info
from app.exceptions import CommonException
from app.schemas import ResponseT

router = APIRouter()


@router.get("/")
async def home():
    return {"API-location": "/education/"}


# Offline(DB) Operation Mode
# data = class-table + grades + info 数据合集
@router.get("/data", response_model=ResponseT)
async def get_education_data(username: int, password: str, semester=''):
    response = ResponseT()
    return response


@router.get("/info", response_model=ResponseT)
async def get_education_info(username: int, password: str):
    response = ResponseT(data={username: password})
    return response


@router.get("/grades", response_model=ResponseT)
async def get_education_grades(username: int, password: str):
    response = ResponseT(data={username: password})
    return response


@router.get("/class-table", response_model=ResponseT)
async def get_education_class_table(user: schemas.User, semester: str):
    response = ResponseT()
    return response


# Online Operation Mode
# data = class-table + grades + info 数据合集
@router.post("/data", response_model=ResponseT)
async def refresh_education_data(user: schemas.User, semester='626'):
    response = ResponseT()
    return response


@router.post("/info", response_model=ResponseT)
async def refresh_education_info(user: schemas.User):
    response = ResponseT()
    try:
        response.data = get_stu_info(user.username, user.password)
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response


@router.post("/class-table", response_model=ResponseT)
async def refresh_education_class_table(user: schemas.User, semester: str):
    response = ResponseT()
    return response


@router.post("/grades", response_model=ResponseT)
async def refresh_education_grades(user: schemas.User):
    response = ResponseT()
    return response
