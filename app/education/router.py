from fastapi import APIRouter

from modelset.schemas import ResponseT, User

router = APIRouter()


@router.get("/")
async def home():
    return {"API-location": "/education/"}


# Offline(DB) Operation Mode
# data = class-table + grades + info 数据合集
@router.get("/data", response_model=ResponseT)
async def get_education_data(username, password, semester=''):
    response = ResponseT()
    return response


@router.get("/info", response_model=ResponseT)
async def get_education_info(username: str, password: str):
    response = ResponseT(data={username: password})
    return response


@router.get("/grades", response_model=ResponseT)
async def get_education_grades(username: str, password: str):
    response = ResponseT(data={username: password})
    return response


@router.get("/class-table", response_model=ResponseT)
async def get_education_class_table(username: str, password: str, semester: str):
    response = ResponseT()
    return response


# Online Operation Mode
# data = class-table + grades + info 数据合集
@router.post("/data", response_model=ResponseT)
async def refresh_education_data(username, password, semester='626'):
    response = ResponseT()
    return response


@router.post("/info", response_model=ResponseT)
async def refresh_education_info(user: User):
    response = ResponseT()
    return response


@router.post("/class-table", response_model=ResponseT)
async def refresh_education_class_table(user: User, semester: str):
    response = ResponseT()
    return response


@router.post("/grades", response_model=ResponseT)
async def refresh_education_grades(user: User):
    response = ResponseT()
    return response
