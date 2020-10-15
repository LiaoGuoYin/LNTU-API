import datetime

from sqlalchemy.orm import Session

from app import schemas
from appDB import models


def update_user(user: schemas.User, session: Session) -> models.User:
    new_user = models.User(**user.dict())
    new_user.lastLogin = datetime.datetime.now()
    session.merge(new_user)
    session.commit()
    return new_user


def update_info(user_info: schemas.UserInfo, session: Session) -> models.UserInfo:
    new_user_info = models.UserInfo(**user_info.dict())
    new_user_info.ownerUsername = user_info.username
    session.merge(new_user_info)
    session.commit()
    return new_user_info


def update_grade_table(user: schemas.User, grade_table_row_list: [schemas.GradeTable], session: Session) -> [
    models.GradeTable]:
    for row in grade_table_row_list:
        new_grade_table_row = models.GradeTable(username=user.username, **row.dict())
        new_grade_table_row.ownerUsername = user.username
        session.merge(new_grade_table_row)
    session.commit()


def update_gpa(user: schemas.User, grade_gpa: schemas.GPA, session: Session) -> models.GPA:
    new_gpa = models.GPA(username=user.username, **grade_gpa.dict())
    new_gpa.ownerUsername = user.username
    session.merge(new_gpa)
    session.commit()
    return new_gpa


def update_grade_list(user: schemas.User, grade_list: [schemas.Grade], session: Session) -> models.Grade:
    for grade in grade_list:
        new_grade = models.Grade(username=user.username, **grade.dict())
        new_grade.ownerUsername = user.username
        session.merge(new_grade)
    session.commit()


def update_course_table(course_table_list: [schemas.CourseTable], session: Session) -> models.CourseTable:
    for course in course_table_list:
        new_course = models.CourseTable(**course.dict())
        session.merge(new_course)
    session.commit()


def update_aipao_order(student: schemas.AiPaoUser, session: Session) -> models.AiPaoOrder:
    new_user = models.AiPaoOrder(**student.dict(exclude={'token'}))
    session.merge(new_user)
    session.commit()
    return new_user
