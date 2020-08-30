from fastapi import APIRouter

from app import schemas
from app.education.core import get_stu_info, get_class_table, get_grade, get_grade_table
from app.exceptions import CommonException
from app.schemas import ResponseT

router = APIRouter()


@router.get("/")
async def home():
    return {"API-location": "/education/"}


# Offline(DB) Operation Mode
# data = class-table + grade + info 数据合集
# @router.get("/data", response_model=ResponseT)
# async def get_education_data(username: int, password: str, semesterId: int = 627):
#     response = ResponseT()
#     return response

#
# @router.get("/info", response_model=ResponseT)
# async def get_education_info(username: int, password: str):
#     response = ResponseT(data={username: password})
#     return response


# @router.get("/grade", response_model=ResponseT)
# async def get_education_grade(username: int, password: str, semesterId: int = 627):
#     response = ResponseT(data={username: password})
#     return response


# @router.get("/class-table", response_model=ResponseT)
# async def get_education_class_table(user: schemas.User, semesterId: int = 627):
#     response = ResponseT()
#     return response


# Online Operation Mode
# data = class-table + grade + info 数据合集
@router.post("/data", response_model=ResponseT)
async def refresh_education_data(user: schemas.User, semesterId: int = 627):
    response = ResponseT()
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
async def refresh_education_grade(user: schemas.User, semesterId: int = 627):
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
