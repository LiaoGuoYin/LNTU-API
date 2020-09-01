from fastapi import APIRouter

from app import schemas
from app.common import notice
from app.const import choose_semester_id
from app.education.core import get_stu_info, get_class_table, get_grade, get_grade_table, login
from app.education.gpa import gpa_util
from app.exceptions import CommonException
from app.schemas import ResponseT

router = APIRouter()


@router.get("/")
async def home():
    return {"API-location": "/education/"}


@router.get("/notice", )
async def refresh_notice(limit: int = 10):
    response = ResponseT()
    try:
        response.data = notice.run()
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response


# Online Operation Mode
# data = info + class-table + grade-table + gpa-table
@router.post("/data", response_model=ResponseT)
async def refresh_education_data(user: schemas.User, semester: str = '2020-2'):
    semesterId = choose_semester_id(semester)
    response = ResponseT()
    try:
        session = login(**user.dict())
        semester_grade = get_grade_table(**user.dict(), session=session)
        data = {
            'info': get_stu_info(**user.dict(), session=session),
            'classTable': get_class_table(**user.dict(), session=session, semesterId=semesterId),
            # 'grade': get_grade(**user.dict(), session=session, semesterId=semesterId - 1),  # TODO: other semester
            'gradeTable': semester_grade,
            'gpa': gpa_util(semester_grade),
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
async def refresh_education_class_table(user: schemas.User, semester: str = '2020-2'):
    semesterId = choose_semester_id(semester)
    response = ResponseT()
    try:
        response.data = get_class_table(**user.dict(), semesterId=semesterId)
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


@router.post("/grade", response_model=ResponseT)
async def refresh_education_grade(user: schemas.User, semester: str = '2020-2'):
    semesterId = choose_semester_id(semester)
    response = ResponseT()
    try:
        semester_grade = get_grade(**user.dict(), semesterId=semesterId)
        semester_gpa = gpa_util(semester_grade)
        response.data = {
            'grade': semester_grade,
            'gpa': semester_gpa
        }
    except CommonException as e:
        response.code, response.message = e.code, e.msg
    return response
