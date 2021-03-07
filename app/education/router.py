from fastapi import APIRouter
from fastapi_sqlalchemy import db
from starlette import status

from app.constants import constantsShared
from app import schemas, exceptions
from app.education import core, utils
from app.education.urls import ClassTableTypeEnum
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
async def refresh_notice(offset: int = 0, limit: int = 20, init: bool = False):
    """
        获取教务通知
    - **offset: int**: 偏移起始位
    - **limit: int**: 偏移量
    """
    response = ResponseT()
    page_list = ['https://jwzx.lntu.edu.cn/index/jwgg.htm']
    if init:
        page_list.extend(['http://jwzx.lntu.edu.cn/index/jwgg/{page}.htm'.format(page=i)
                          for i in range(1, 25)])
    try:
        for page in page_list:
            notice_list = notice.get_notice_url_list_from(page)
            crud.update_public_notice(notice_list, db.session)
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.message = "教务官网在线宕机，离线模式"
    response.data, last_updated_at = crud.retrieve_public_notice(offset, limit, db.session)
    return response


@router.get("/classroom", response_model=ResponseT, summary='获取空教室')
async def refresh_classroom(week: int, name: str, offline: bool = False):
    """
        查询空教室
    - **week**: 教学周(1-26)
    - **name**: 教学楼全名简拼: 例: yhl、eyl、jyl、hldwlsys 等..
        - 注: 耘慧楼、尔雅楼、静远楼、葫芦岛物理实验室、葫芦岛机房、博文楼、博雅楼、新华楼、中和楼、致远楼、知行楼、物理实验室、主楼机房 **简拼**
    """
    response = ResponseT()
    try:
        if offline:
            raise exceptions.NetworkException("用户手动懒加载模式")
        building_id = constantsShared.building.get(name)
        if not building_id:
            raise exceptions.FormException("参数错误：请输入正确的教学楼")
        classroom_data = schemas.ClassroomResponseData(week=week, buildingName=name,
                                                       classroomList=room.run(week=week, building_id=building_id))
        crud.update_classroom(classroom_data, db.session)
        response.data = classroom_data
        if len(classroom_data.classroomList) == 0:
            raise exceptions.NetworkException("自动懒加载模式")
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_classroom(week, name, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/info", response_model=ResponseT, summary='获取个人基本信息')
async def refresh_education_info(user: schemas.User, offline: bool = False):
    """
        相当于登录
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    try:
        if offline:
            raise exceptions.NetworkException("用户手动懒加载模式")
        response.data = core.get_stu_info(**user.dict())
        crud.update_user(user, db.session)
        crud.update_info(response.data, db.session)
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_info(user, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/course-table", response_model=ResponseT, summary='获取本学期课表')
async def refresh_education_course_table(user: schemas.User, type: str = ClassTableTypeEnum.classes.value,
                                         offline: bool = False):
    """
        获取指定学期课表
    - **username**: 用户名
    - **password**: 密码
    - **type**: 课表类型; 例：class, student
    """
    response = ResponseT()
    semester = constantsShared.current_semester
    try:
        if offline:
            raise exceptions.NetworkException("用户手动懒加载模式")
        data = core.get_course_table(**user.dict(), course_table_type=type)
        crud.update_user(user, db.session)
        crud.update_course_table(user, semester, data, db.session)
        response.data = data
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_course_table(user, db.session, semester)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/grade", response_model=ResponseT, summary='获取成绩')
async def refresh_education_grade(user: schemas.User, offline: bool = False):
    """
        计算所有学期成绩
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    try:
        if offline:
            raise exceptions.NetworkException("用户手动懒加载模式")
        response.data = core.get_grade(**user.dict())
        crud.update_user(user, db.session)
        crud.update_grade_list(user, response.data, db.session)
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_grade(user, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response


@router.post("/exam", response_model=ResponseT, summary='获取考试安排')
async def refresh_education_exam(user: schemas.User, semester: str = constantsShared.current_semester,
                                 offline: bool = False):
    """
        考试安排查询
    - **username**: 用户名
    - **password**: 密码
    - **semester**: 学期; 例: 2020-秋
    - **offline**: 是否离线模式
    """
    response = ResponseT()
    try:
        if offline:
            raise exceptions.NetworkException("用户手动懒加载模式")
        exam_list = core.get_exam(**user.dict(), semester_id=constantsShared.get_semester_id(semester))
        response.data = exam_list
        crud.update_user(user, db.session)
        crud.update_exam_list(user, exam_list, semester, db.session)
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        response.data, last_updated_at = crud.retrieve_user_exam(user, db.session)
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    except exceptions.ExamException as e:
        response.code = e.code
        response.message = e.message

    return response


@router.post("/external-exam", response_model=ResponseT, summary='获取校外考试情况')
async def refresh_education_other_exam(user: schemas.User):
    """
        获取外校考试(无离线模式)
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
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
    response.data = core.get_plan(**user.dict())
    crud.update_user(user, db.session)
    return response


@router.post("/evaluation", response_model=ResponseT, summary='一键评教')
async def evaluate_teacher(evaluation_form: schemas.TeacherEvaluationRequest):
    """
        一键完成满分评教(无离线模式)
    - **username**: 用户名
    - **password**: 密码
    - **submit**: 是否提交一键评教，默认为 false
    """
    response = ResponseT()
    response.code, response.message, response.data = core.evaluate_teacher(**evaluation_form.dict())
    crud.update_user(session=db.session, user=schemas.User(**evaluation_form.dict(exclude={'submit'})))
    return response


@router.post("/data", response_model=ResponseT, summary='获取数据集合：基本信息、本学期课表、考试安排、所有成绩')
async def refresh_education_data(user: schemas.User, offline: bool = False):
    """
        登录: 获取基本信息、本学期课表、考试安排、所有成绩
    - **username**: 用户名
    - **password**: 密码
    """
    response = ResponseT()
    try:
        if offline:
            raise exceptions.NetworkException("用户手动懒加载模式")
        session = core.login(**user.dict())
        crud.update_user(user, db.session)
        response_data = schemas.EducationDataResponse(info=core.get_stu_info(**user.dict(), session=session))
        response_data.courseTable = core.get_course_table(**user.dict(), session=session)
        response_data.exam = core.get_exam(**user.dict(), session=session)
        grade_list = core.get_grade(**user.dict(), session=session)
        response_data.grade = [] if isinstance(grade_list, str) else grade_list
        crud.update_info(response_data.info, db.session)
        crud.update_exam_list(user, response_data.exam, constantsShared.current_semester, db.session)
        crud.update_grade_list(user, response_data.grade, db.session)
        crud.update_course_table(user, constantsShared.current_semester, response_data.courseTable, db.session)
        response.data = response_data
    except exceptions.NetworkException:
        response.code = status.HTTP_200_OK
        user_info, last_updated_at = crud.retrieve_user_info(user, db.session)
        response.data = {
            'info': user_info,
            'courseTable': crud.retrieve_user_course_table(user, db.session, constantsShared.current_semester)[0],
            'exam': crud.retrieve_user_exam(user, db.session)[0],
            'grade': crud.retrieve_user_grade(user, db.session)[0],
        }
        response.message = f"离线模式: {response.message}, 最后更新于: {last_updated_at}"
    return response
