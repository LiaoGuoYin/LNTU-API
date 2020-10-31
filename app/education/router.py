from copy import deepcopy

from fastapi import APIRouter
from fastapi_sqlalchemy import db

from app import schemas
from app.common import notice, room
from app.const import choose_semester_id
from app.education.core import get_stu_info, get_course_table, get_grade, login, calculate_gpa
from app.schemas import ResponseT
from appDB import crud

router = APIRouter()


@router.get("/classroom", )
async def refresh_classroom(week, name):
    response = ResponseT(data=room.run(week=week, building_name=name))
    return response


@router.get("/notice", )
async def refresh_notice():  # TODO, limit offsets
    response = ResponseT(data=notice.run())
    return response


# Online Operation Mode
# data = info + course-table + grade + gpa
@router.post("/data", response_model=ResponseT)
async def refresh_education_data(user: schemas.User, semester: str = '2020-2'):
    """
        登录、获取基本信息、指定学期课表、所有成绩、加权平均成绩(GPA)
    - **username**: 用户名
    - **password**: 密码
    - **semester**: 学期; 例: 2020-1 表示 2020 年的第一个学期, 2020-2 表示 2020 年的第二个学期
    """
    response = ResponseT()
    semester_id = choose_semester_id(semester)
    session = login(**user.dict())
    grade_list = get_grade(**user.dict(), session=session)
    data = {
        'info': get_stu_info(**user.dict(), session=session),
        'courseTable': get_course_table(**user.dict(), session=session, semester_id=semester_id),
        'grade': grade_list,
        'gpa': calculate_gpa(grade_list, is_including_optional_course=1),
    }
    crud.update_user(user, db.session)
    crud.update_info(data['info'], db.session)
    crud.update_grade_list(user, data['grade'], db.session)
    crud.update_gpa(user, data['gpa'], db.session)
    crud.update_course_table(data['courseTable'], db.session)
    response.data = data
    return response


@router.post("/info", response_model=ResponseT)
async def refresh_education_info(user: schemas.User):
    """
        相当于登录
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    response.data = get_stu_info(**user.dict())
    crud.update_user(user, db.session)
    crud.update_info(response.data, db.session)
    return response


@router.post("/course-table", response_model=ResponseT)
async def refresh_education_course_table(user: schemas.User, semester: str = '2020-2'):
    """
        获取指定学期课表
    - **username**: 用户名
    - **password**: 密码
    - **semester**: 学期; 例: 2020-1 表示 2020 年的第一个学期, 2020-2 表示 2020 年的第二个学期
    """
    semester_id = choose_semester_id(semester)
    response = ResponseT(data=get_course_table(**user.dict(), semester_id=semester_id))
    crud.update_user(user, db.session)
    crud.update_course_table(response.data, db.session)
    return response


@router.post("/grade", response_model=ResponseT)
async def refresh_education_grade(user: schemas.User, isIncludingOptionalCourse=1):
    """
        计算学期成绩及 GPA
    - **username**: 用户名
    - **password**: 密码
    - (Optional) **isIncludingOptionalCourse**: 是否包括 [校级公选课]，默认包括选修课; 0 或 1
    """
    response = ResponseT()
    user = schemas.User(**user.dict())
    grade_list = get_grade(**user.dict())
    response.data = {
        'grade': grade_list,
        'gpa': calculate_gpa(deepcopy(grade_list), is_including_optional_course=isIncludingOptionalCourse)
    }
    crud.update_user(user, db.session)
    crud.update_grade_list(user, response.data['grade'], db.session)
    crud.update_gpa(user, response.data['gpa'], db.session)
    return response
