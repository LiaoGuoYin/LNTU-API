from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import schemas, education
from app.constants import constantsShared
from appDB import models
from appPush import crud
from appPush.push import apple_push

db_url_dict = constantsShared.get_db_url_dict()
engine = create_engine(db_url_dict['production'], echo=True)
DBSession = sessionmaker(bind=engine)

celery = Celery('appPush.tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379')


@celery.task
def push_notice(need_to_push_notice_list: [schemas.NoticePushNotification]):
    for notice in need_to_push_notice_list:
        apple_push(category=schemas.NotificationSubscriptionEnum.NOTICE, body=notice.contentBody,
                   device_token=notice.token)


@celery.task
def push_grade(body: str, token: str):
    apple_push(category=schemas.NotificationSubscriptionEnum.GRADE, body=body,
               device_token=token)


@celery.task
def push_grade_every_hour():
    session = DBSession()
    grade_list = crud.retrieve_need_to_refresh_grades_user_list(session)
    session.query(models.Grade)

    for grade in grade_list:
        result = push_grade.delay(body=grade.contentBody, token=grade.token)
        print(result)
        # TODO: 回写结果到数据库
        grade_result = session.query(models.Grade).filter_by(username=grade.username, name=grade.courseName).first()
        if not grade_result:
            grade_result.isPushed = 1
            session.add(grade_result)
    else:
        session.commit()


@celery.task
def login_to_refresh_course_results(user_list: [schemas.User]):
    for user in user_list:
        print(f"检测到同课程同学刷到新成绩，{user.get('username')} 登录刷新中...")
        education.core.get_grade(**user.dict())
