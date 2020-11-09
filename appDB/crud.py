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


def update_course_table(course_table_list: [schemas.CourseTable], session: Session):
    for course in course_table_list:
        if not isinstance(course, schemas.CourseTable):
            continue
        new_course = models.CourseTable(**course.dict())
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


def update_gpa(user: schemas.User, grade_gpa: schemas.GPA, session: Session) -> models.GPA:
    new_gpa = models.GPA(username=user.username, **grade_gpa.dict())
    session.merge(new_gpa)
    session.commit()
    return new_gpa


def update_aipao_order(student: schemas.AiPaoUser, session: Session) -> models.AiPaoOrder:
    new_user = models.AiPaoOrder(**student.dict(exclude={'token'}))
    session.merge(new_user)
    session.commit()
    return new_user


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
def retrieve_user_gpa(request_user: schemas.User, session: Session) -> (dict, str):
    user_gpa_result = session.query(models.GPA).filter_by(username=request_user.username).all()
    serializer = Serializer(user_gpa_result, exclude=['username', 'lastUpdatedAt'], many=True)
    last_updated_at = '' if len(user_gpa_result) == 0 else user_gpa_result[0].lastUpdatedAt
    return ({}, '') if len(serializer.data) == 0 else (serializer.data[0], last_updated_at)


@server_user_valid_required
def retrieve_user_exam(request_user: schemas.User, session: Session) -> (list, str):
    exam_list = session.query(models.Exam).filter_by(username=request_user.username).all()
    serializer = Serializer(exam_list, exclude=['username', 'lastUpdatedAt'], many=True)
    last_updated_at = '' if len(exam_list) == 0 else exam_list[0].lastUpdatedAt
    return serializer.data, last_updated_at

# TODO
# @server_user_valid_required
# def retrieve_user_course_table(request_user: schemas.User, session: Session) -> dict:
#     return dict(session.query(models.CourseTable).filter_by(username=request_user.username).first().__dict__)
