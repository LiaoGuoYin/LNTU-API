import datetime
from functools import wraps

from sqlalchemy.orm import Session

from app import schemas, exceptions
from appDB import models
from appDB.utils import Serializer


def update_user(user: schemas.User, session: Session) -> models.User:
    new_user = models.User(**user.dict())
    new_user.lastUpdatedAt = datetime.datetime.now()
    session.merge(new_user)
    session.commit()
    return new_user


def update_info(user_info: schemas.UserInfo, session: Session) -> models.UserInfo:
    new_user_info = models.UserInfo(**user_info.dict())
    session.merge(new_user_info)
    session.commit()
    return new_user_info


def update_course_table(user: schemas.User, semester: str, course_table_list: [schemas.CourseTable], session: Session):
    for course in course_table_list:
        if not isinstance(course, schemas.CourseTable):
            continue
        new_course = models.CourseTable(username=user.username, semester=semester, **course.dict())
        session.merge(new_course)
    session.commit()


def update_exam_list(user: schemas.User, exam_list: [schemas.Exam], semester: str, session: Session):
    for exam in exam_list:
        if not isinstance(exam, schemas.Exam):
            continue
        new_exam = models.Exam(username=user.username, semester=semester, **exam.dict())
        session.merge(new_exam)
    session.commit()


def update_grade_list(user: schemas.User, grade_list: [schemas.Grade], session: Session):
    for grade in grade_list:
        if not isinstance(grade, schemas.Grade):
            continue
        new_grade = models.Grade(username=user.username, **grade.dict())
        session.merge(new_grade)
    session.commit()


def update_aipao_order(student: schemas.AiPaoUser, imei: str, session: Session) -> models.AiPaoOrder:
    new_user = models.AiPaoOrder(IMEI=imei, **student.dict(exclude={'token'}))
    session.merge(new_user)
    session.commit()
    return new_user


def update_classroom(classroom_data: schemas.ClassroomResponseData, session: Session):
    for room in classroom_data.classroomList:
        new_room = models.Classroom(**room.dict())
        new_room.week = classroom_data.week
        new_room.buildingName = classroom_data.buildingName
        session.merge(new_room)
    session.commit()


# Login Decorator Function
def server_user_valid_required(function_to_wrap):
    @wraps(function_to_wrap)
    def wrap(request_user: schemas.User, session: Session, *args, **kwargs):
        server_user = session.query(models.User).filter_by(username=request_user.username).first()
        if not server_user:
            # Check user server account validation
            raise exceptions.FormException(F"离线模式: {request_user.username} 用户无效，请稍后再试，可能是未曾登录过 LNTUHelper")
        else:
            if request_user.password != server_user.password:
                raise exceptions.FormException(F"离线模式: {request_user.username} 用户名或密码错误")
            else:
                # Authenticated successfully
                return function_to_wrap(request_user, session, *args, **kwargs)

    return wrap


def retrieve_classroom(week: int, building_name: str, session: Session) -> (schemas.ClassroomResponseData, str):
    classroom_response = schemas.ClassroomResponseData(week=week, buildingName=building_name)
    classroom_list = session.query(models.Classroom).filter_by(week=classroom_response.week,
                                                               buildingName=classroom_response.buildingName).all()
    serializer = Serializer(classroom_list, exclude=['buildingName', 'week', 'lastUpdatedAt'], many=True)
    classroom_response.classroomList = serializer.data
    last_updated_at = '' if len(classroom_list) == 0 else classroom_list[0].lastUpdatedAt
    return classroom_response, last_updated_at


@server_user_valid_required
def retrieve_user_info(request_user: schemas.User, session: Session) -> (dict, str):
    user_info_result = session.query(models.UserInfo).filter_by(username=request_user.username).all()
    if len(user_info_result) == 0:  # TODO
        return {}, ''
    else:
        last_updated_at = '' if len(user_info_result) == 0 else user_info_result[0].lastUpdatedAt
        serializer = Serializer(user_info_result, exclude=['lastUpdatedAt'], many=True)
        return serializer.data[0], last_updated_at


@server_user_valid_required
def retrieve_user_grade(request_user: schemas.User, session: Session) -> (list, str):
    grade_list = session.query(models.Grade).filter_by(username=request_user.username).all()
    last_updated_at = '' if len(grade_list) == 0 else grade_list[0].lastUpdatedAt
    serializer = Serializer(grade_list, exclude=['username', 'lastUpdatedAt'], many=True)
    return serializer.data, last_updated_at


@server_user_valid_required
def retrieve_user_exam(request_user: schemas.User, session: Session) -> (list, str):
    exam_list = session.query(models.Exam).filter_by(username=request_user.username).all()
    serializer = Serializer(exam_list, exclude=['username', 'lastUpdatedAt'], many=True)
    last_updated_at = '' if len(exam_list) == 0 else exam_list[0].lastUpdatedAt
    return serializer.data, last_updated_at


@server_user_valid_required
def retrieve_user_course_table(request_user: schemas.User, session: Session, semester: str) -> (
        [schemas.CourseTable], str):
    course_table_list = session.query(models.CourseTable).filter_by(username=request_user.username,
                                                                    semester=semester).all()
    serializer = Serializer(course_table_list, exclude=['lastUpdatedAt'], many=True)
    last_updated_at = '' if len(course_table_list) == 0 else course_table_list[0].lastUpdatedAt
    return serializer.data, last_updated_at
