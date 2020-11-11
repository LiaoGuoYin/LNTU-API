from fastapi import APIRouter
from fastapi_sqlalchemy import db
from starlette import status

from app import const
from app import schemas, exceptions
from app.education import core
from app.public import notice, room, helper
from app.schemas import ResponseT
from appDB import crud

router = APIRouter()


@router.get("/init", response_model=ResponseT, summary='获取助手初始化所需的基本信息')
async def refresh_education_refresh_helper_message():
    """
        初始化, 获取助手所需的基本信息
    """
    response = ResponseT(data=helper.refresh_helper_message())
    return response


@router.get("/notice", response_model=ResponseT, summary='获取教务通知')
async def refresh_notice():  # TODO, limit offsets
    response = ResponseT(data=notice.run())
    return response


@router.get("/classroom", response_model=ResponseT, summary='获取空教室')
async def refresh_classroom(week, name):
    """
        查询空教室
    - **week**: 教学周(1-26)
    - **name**: 教学楼全名简拼: 例: yhl、eyl、jyl、hldwlsys 等..
        - 注: 耘慧楼、尔雅楼、静远楼、葫芦岛物理实验室、葫芦岛机房、博文楼、博雅楼、新华楼、中和楼、致远楼、知行楼、物理实验室、主楼机房 **简拼**
    """
    response = ResponseT()
    try:
        building_id = const.building_dict.get(name)
        if not building_id:
            raise exceptions.FormException("参数错误：请输入正确的教学楼")
        classroom_data = schemas.ClassRoomResponse(week=week, buildingName=name,
                                                   classRoomList=room.run(week=week, building_id=building_id))
        crud.update_classroom(classroom_data, db.session)
        response.data = classroom_data
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_classroom(week, name, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/info", response_model=ResponseT, summary='获取个人基本信息')
async def refresh_education_info(user: schemas.User):
    """
        相当于登录
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    try:
        response.data = core.get_stu_info(**user.dict())
        crud.update_user(user, db.session)
        crud.update_info(response.data, db.session)
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_info(user, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/course-table", response_model=ResponseT, summary='获取指定学期课表')
async def refresh_education_course_table(user: schemas.User, semester: str = '2020-秋'):
    """
        获取指定学期课表
    - **username**: 用户名
    - **password**: 密码
    - **semester**: 学期; 例: 2020-秋、2020-春
    """
    response = ResponseT()
    try:
        semester_id = const.choose_semester_id(semester)
        data = core.get_course_table(**user.dict(), semester_id=semester_id)
        crud.update_user(user, db.session)
        crud.update_course_table(user, semester, data, db.session)
        response.data = data
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_course_table(user, semester, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/grade", response_model=ResponseT, summary='获取成绩')
async def refresh_education_grade(user: schemas.User):
    """
        计算学期成绩及 GPA
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    user = schemas.User(**user.dict())
    try:
        grade_list = core.get_grade(**user.dict())
        response.data = {
            'grade': grade_list,
            'gpa': core.calculate_gpa(grade_list)
        }
        crud.update_user(user, db.session)
        crud.update_grade_list(user, response.data['grade'], db.session)
        crud.update_gpa(user, response.data['gpa'], db.session)
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_grade(user, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/exam", response_model=ResponseT, summary='获取考试安排')
async def refresh_education_exam(user: schemas.User, semester: str = '2020-秋'):
    """
        考试安排查询
    - **username**: 用户名
    - **password**: 密码
    - **semester**: 学期; 例: 2020-秋
    """
    response = ResponseT()
    user = schemas.User(**user.dict())
    try:
        semester_id = const.choose_semester_id(semester)
        exam_list = core.get_exam(**user.dict(), semester_id=semester_id)
        response.data = exam_list
        crud.update_user(user, db.session)
        crud.update_exam_list(user, exam_list, semester, db.session)
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_exam(user, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/other-exam", response_model=ResponseT, summary='获取校外考试')
async def refresh_education_other_exam(user: schemas.User):
    """
        获取外校考试(无离线模式)
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    user = schemas.User(**user.dict())
    response.data = core.get_other_exam(**user.dict())
    crud.update_user(user, db.session)
    return response


@router.post("/plan", response_model=ResponseT, summary='获取个人教学计划完成情况')
async def refresh_education_plan(user: schemas.User):
    """
        教学计划(无离线模式)
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    user = schemas.User(**user.dict())
    response.data = core.get_plan(**user.dict())
    crud.update_user(user, db.session)
    return response


@router.post("/data", response_model=ResponseT, summary='获取数据集合：基本信息、本学期课表、考试安排、所有成绩、GPA')
async def refresh_education_data(user: schemas.User):
    """
        登录: 获取基本信息、本学期课表、考试安排、所有成绩、GPA
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    try:
        session = core.login(**user.dict())
        grade_list = core.get_grade(**user.dict(), session=session)
        course_table_data = core.get_course_table(**user.dict(), session=session)
        data = {
            'info': core.get_stu_info(**user.dict(), session=session),
            'courseTable': course_table_data,
            'exam': core.get_exam(**user.dict(), session=session),
            'grade': [] if isinstance(grade_list, str) else grade_list,
            'gpa': core.calculate_gpa(grade_list),
        }
        crud.update_user(user, db.session)
        crud.update_info(data['info'], db.session)
        crud.update_exam_list(user, data['exam'], '2020-秋', db.session)  # TODO global semester
        crud.update_grade_list(user, data['grade'], db.session)
        crud.update_gpa(user, data['gpa'], db.session)
        crud.update_course_table(user, '2020-秋', course_table_data, db.session)
        response.data = data
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        user_info, last_updated_at = crud.retrieve_user_info(user, db.session)
        response.data = {
            'info': user_info,
            'courseTable': crud.retrieve_user_course_table(user, '2020-秋', db.session),
            'exam': crud.retrieve_user_exam(user, db.session)[0],
            'grade': crud.retrieve_user_grade(user, db.session)[0],
            'gpa': crud.retrieve_user_gpa(user, db.session)[0],
        }
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response
