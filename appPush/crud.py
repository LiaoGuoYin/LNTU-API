from sqlalchemy import text
from sqlalchemy.orm import Session

from app import schemas


def retrieve_need_to_push_notice_device_token_list(notice_content_body: str, session: Session) -> [
    schemas.NoticePushNotification]:
    device_token_list = session.execute("SELECT token FROM subscription WHERE subscription.isSubscribeNotice = 1;")
    return [schemas.NoticePushNotification(
        token=each[0],
        contentBody=notice_content_body
    ) for each in device_token_list]


def retrieve_need_to_refresh_grades_user_list_with_code(course_code: str, session: Session) -> [schemas.User]:
    result_list = session.execute(text("""
        SELECT DISTINCT
            `user`.username,
            `user`.`password`
        FROM
            subscription
            LEFT JOIN `user` ON subscription.username = `user`.username,
            exam
            LEFT JOIN grade ON exam.code = grade.code
                AND exam.username = grade.username
        WHERE
            grade.isPushed IS NULL
            AND subscription.isSubscribeGrade = 1
            AND subscription.username = exam.username
            AND exam.code = :course_code;
        """), {'course_code': course_code})
    return [schemas.User(
        username=result[0],
        password=result[1]
    ) for result in result_list]


def retrieve_need_to_refresh_grades_user_list(session: Session) -> [schemas.GradePushNotification]:
    # 获取待推送成绩
    result_list = session.execute(text("""
        SELECT DISTINCT
            subscription.`token`,
            subscription.username,
            grade.`name`,
            grade.`result`
        FROM
            subscription
            LEFT JOIN `user` ON subscription.username = `user`.username,
            exam
            LEFT JOIN grade ON exam.code = grade.code
                AND exam.username = grade.username
        WHERE
            grade.isPushed = 0
            AND subscription.isSubscribeGrade = 1
            AND subscription.username = exam.username;
        """))
    return [schemas.GradePushNotification(
        token=result[0],
        username=result[1],
        courseName=result[2],
        courseResult=result[3]
    ) for result in result_list]
