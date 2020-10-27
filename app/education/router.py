from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sentry_sdk import capture_exception

from app import schemas
from app.common import notice, room
from app.const import choose_semester_id
from app.education.core import get_stu_info, get_course_table, get_grade, get_grade_table, login, calculate_gpa
from app.exceptions import CommonException
from app.schemas import ResponseT
from appDB import crud

router = APIRouter()


@router.get("/gpa-all", response_model=ResponseT)
async def refresh_education_gpa(username: int, password: str):
    '''
        计算到目前为止的 GPA（重修除外）
    - **username**: 用户名
    - **password**: 密码
    '''
    response = ResponseT()
    try:
        user_dict = {'username': username,
                     'password': password}
        user = schemas.User(**user_dict)
        grade_table = get_grade_table(**user_dict)
        response.data = calculate_gpa(grade_table, is_including_optional_course=1)
        crud.update_user(user, db.session)
        crud.update_gpa(schemas.User(**user_dict), response.data, db.session)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


@router.get("/grade", response_model=ResponseT)
async def refresh_education_grade(username: int, password: str, semester: str = '2020-1', isIncludingOptionalCourse=1):
    '''
        计算学期成绩及 GPA
    - **username**: 用户名
    - **password**: 密码
    - **semester**: 学期；2020-1 表示 2020 年的第一个学期，2020-2 表示 2020 年的第二个学期
    - **isIncludingOptionalCourse**: 是否包括 [校级公选课]，默认包括选修课; 1 或 0
    '''
    semester_id = choose_semester_id(semester)
    response = ResponseT()
    try:
        user_dict = {'username': username,
                     'password': password}
        user = schemas.User(**user_dict)
        semester_grade = get_grade(**user.dict(), semester_id=semester_id)
        semester_gpa = calculate_gpa(semester_grade, is_including_optional_course=isIncludingOptionalCourse)
        semester_gpa.semester = semester
        response.data = {
            'grade': semester_grade,
            'gpa': semester_gpa
        }
        crud.update_user(user, db.session)
        crud.update_grade_list(user, response.data['grade'], db.session)
        crud.update_gpa(user, response.data['gpa'], db.session)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


@router.get("/classroom", )
async def refresh_classroom(week, name):
    response = ResponseT()
    try:
        response.data = room.run(week=week, building_name=name)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


@router.get("/notice", )
async def refresh_notice():  # TODO, limit offsets
    response = ResponseT()
    try:
        response.data = notice.run()
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


# Online Operation Mode
# data = info + course-table + grade-table + gpa-table
@router.post("/data", response_model=ResponseT)
async def refresh_education_data(user: schemas.User, semester: str = '2020-2'):
    semester_id = choose_semester_id(semester)
    response = ResponseT()
    try:
        session = login(**user.dict())
        semester_grade = get_grade_table(**user.dict(), session=session)
        data = {
            'info': get_stu_info(**user.dict(), session=session),
            'courseTable': get_course_table(**user.dict(), session=session, semester_id=semester_id),
            # TODO，本方法是否返回和学期无关的信息
            'gradeTable': semester_grade,
            'gpa': calculate_gpa(semester_grade, is_including_optional_course=1),
        }
        response.data = data
        crud.update_user(user, db.session)
        crud.update_info(data['info'], db.session)
        crud.update_grade_table(user, data['gradeTable'], db.session)
        crud.update_gpa(user, data['gpa'], db.session)
        crud.update_course_table(data['courseTable'], db.session)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


@router.post("/info", response_model=ResponseT)
async def refresh_education_info(user: schemas.User):
    response = ResponseT()
    try:
        response.data = get_stu_info(**user.dict())
        crud.update_user(user, db.session)
        crud.update_info(response.data, db.session)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response


@router.post("/course-table", response_model=ResponseT)
async def refresh_education_course_table(user: schemas.User, semester: str = '2020-2'):
    semester_id = choose_semester_id(semester)
    response = ResponseT()
    try:
        response.data = get_course_table(**user.dict(), semester_id=semester_id)
        crud.update_user(user, db.session)
        crud.update_course_table(response.data, db.session)
    except CommonException as e:
        capture_exception(e)
        response.code, response.message = e.code, e.msg
    return response
