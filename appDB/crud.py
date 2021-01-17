import datetime

from functools import wraps

from sqlalchemy.orm import Session
from starlette import status

from app import schemas, exceptions
from appDB import models, app_push_crud
from appDB.utils import Serializer
from appPush.tasks import push_notice


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
        old_grade = session.query(models.Grade).filter(models.Grade.username == user.username,
                                                       models.Grade.code == grade.code).first()
        if old_grade:
            session.add(old_grade)
        else:  # New Notice
            new_grade = models.Grade(username=user.username, **grade.dict())
            new_grade.isPushed = False
            session.add(new_grade)
    session.commit()


def update_classroom(classroom_data: schemas.ClassroomResponseData, session: Session):
    for room in classroom_data.classroomList:
        new_room = models.Classroom(**room.dict())
        new_room.week = classroom_data.week
        new_room.buildingName = classroom_data.buildingName
        session.merge(new_room)
    session.commit()


def update_public_notice(notice_list: [schemas.Notice], session: Session):
    for notice in notice_list:
        if not isinstance(notice, schemas.Notice):
            continue
        old_notice = session.query(models.Notice).filter(models.Notice.title == notice.title,
                                                         models.Notice.url == notice.url).first()
        if old_notice:
            session.add(old_notice)
        else:  # New Notice
            new_notice = models.Notice(**notice.dict())
            session.add(new_notice)
            token_list = app_push_crud.retrieve_need_to_push_notice_token(session)
            push_notice.delay(content=new_notice.title, token_list=token_list)
            # TODO status handler
            session.add(new_notice)
    session.commit()


# Notification
def register_notification(form: schemas.NotificationToken, session: Session) -> (int, str):
    if bool(session.query(models.User).filter_by(username=form.username).first()):
        # Identifying whether the user has previously logged in or not
        is_token_exist_previous = bool(session.query(models.NotificationToken).filter_by(token=form.token).first())
        new_token = models.NotificationToken(**form.dict(exclude={'subscriptionList'}))
        new_token.isSubscribeGrade = True if schemas.NotificationSubscriptionEnum.GRADE in form.subscriptionList else False
        new_token.isSubscribeNotice = True if schemas.NotificationSubscriptionEnum.NOTICE in form.subscriptionList else False
        session.merge(new_token)
        session.commit()
        return status.HTTP_200_OK, f'Success, {new_token.username} {"更新" if is_token_exist_previous else "新订阅"} Token: {new_token.token}'
    else:
        return status.HTTP_401_UNAUTHORIZED, f'Failure, {form.username} 还未通过 LNTU-API 登录过!'


def remove_notification(form: schemas.NotificationToken, session: Session) -> (int, str):
    delete_count = session.query(models.NotificationToken).filter_by(token=form.token, username=form.username).delete()
    if delete_count == 0:
        return status.HTTP_404_NOT_FOUND, f'Failure, 没有找到用户: {form.username}, Token: {form.token}'
    else:
        session.commit()
        return status.HTTP_200_OK, f'Success, 清除 Token: {form.token}, 对应用户 {form.username}, 操作 {delete_count} 条'


def retrieve_public_notice(offset: int, limit: int, session: Session) -> (schemas.Notice, str):
    notice_list = session.query(models.Notice).order_by(models.Notice.date.desc()).offset(offset).limit(limit).all()
    serializer = Serializer(notice_list, exclude=['lastUpdatedAt', 'isPushed'], many=True)
    last_updated_at = '' if len(notice_list) == 0 else notice_list[0].lastUpdatedAt
    return serializer.data, last_updated_at


def update_quality_user(user: schemas.User, session: Session) -> models.User:
    new_user = models.User(username=user.username, qualityPassword=user.password)
    new_user.lastUpdatedAt = datetime.datetime.now()
    session.merge(new_user)
    session.commit()
    return new_user


def update_quality_activity(user: schemas.User, quality_activity_list: [schemas.QualityActivity], session: Session):
    for activity in quality_activity_list:
        if not isinstance(activity, schemas.QualityActivity):
            continue
        new_activity = models.QualityActivity(username=user.username, **activity.dict())
        session.merge(new_activity)
    session.commit()


# Login Decorator Function
def server_user_valid_required(function_to_wrap):
    @wraps(function_to_wrap)
    def wrap(request_user: schemas.User, session: Session, *args, **kwargs):
        server_user = session.query(models.User).filter_by(username=request_user.username).first()
        if not server_user:
            # Check user server account validation
            raise exceptions.FormException(F"离线模式: {request_user.username} 用户无效，请稍后再试，可能是还未曾登录过 LNTUHelper")
        else:
            if request_user.password != server_user.password:
                raise exceptions.FormException(F"离线模式: {request_user.username} 教务在线用户名或密码错误")
            else:
                # Authenticated successfully
                return function_to_wrap(request_user, session, *args, **kwargs)

    return wrap


# Login Decorator Function for Quality TODO
def server_user_valid_required_for_quality(function_to_wrap):
    @wraps(function_to_wrap)
    def wrap(request_user: schemas.User, session: Session, *args, **kwargs):
        server_user = session.query(models.User).filter_by(username=request_user.username).first()
        if not server_user:
            # Check user server account validation
            raise exceptions.FormException(F"离线模式: {request_user.username} 用户无效，请稍后再试，可能是还未曾登录过 LNTUHelper")
        else:
            if request_user.password != server_user.qualityPassword:
                raise exceptions.FormException(F"离线模式: {request_user.username} 素拓网用户名或密码错误")
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
    serializer = Serializer(course_table_list, exclude=['username', 'semester', 'lastUpdatedAt'], many=True)
    last_updated_at = '' if len(course_table_list) == 0 else course_table_list[0].lastUpdatedAt
    return serializer.data, last_updated_at


@server_user_valid_required_for_quality
def retrieve_quality_activity(request_user: schemas.User, session: Session) -> ([schemas.QualityActivity], str):
    quality_activity_list = session.query(models.QualityActivity).filter_by(username=request_user.username).all()
    serializer = Serializer(quality_activity_list, exclude=['username', 'lastUpdatedAt'], many=True)
    last_updated_at = '' if len(quality_activity_list) == 0 else quality_activity_list[0].lastUpdatedAt
    return serializer.data, last_updated_at
