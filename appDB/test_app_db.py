import unittest
from fastapi import FastAPI
from fastapi_sqlalchemy import db, DBSessionMiddleware
from sqlalchemy import create_engine

from appDB import models
from appDB.models import Base
from appDB.utils import get_db_url_dict
from app import schemas


class TestAppDB(unittest.TestCase):
    '''
        主要用于检验 schemas 和 models 是否一致，避免改动引起的不匹配
    '''

    def setUp(self) -> None:
        app = FastAPI()
        db_url_dict = get_db_url_dict()
        engine = create_engine(db_url_dict['test'], echo=True)
        Base.metadata.create_all(bind=engine)  # 创建数据库
        app.add_middleware(DBSessionMiddleware, db_url=db_url_dict['test'])

    def test_education_user(self):
        user = schemas.User(username=100000, password='thisismypassword')
        with db():
            db.session.merge(models.User(**user.dict()))
            db.session.commit()

    def test_education_info(self):
        info = schemas.UserInfo(username=10000, name='LiaoGuoYin',
                                photoUrl='http://202.199.224.119:8080/eams/showSelfAvatar.action?user.name=xxxx',
                                nickname='abc', gender='男', grade='2017', educationLast='4', project='主修',
                                education='本科', studentType='本科4年', college='xxxx学院', major='xxxx', direction=None,
                                enrollDate='2022-09-01', graduateDate='2024-07-01', chiefCollege='xxxx学院',
                                studyType='普通全日制', membership='是', isInSchool='是', campus='xxxx校区',
                                majorClass='xx17-x', effectAt='2017-09-01', isInRecord='是', studentStatus='在校',
                                isWorking='否')
        with db():
            db.session.merge(models.UserInfo(**info.dict()))
            db.session.commit()

    def test_education_course_table(self):
        course_table = schemas.CourseTable(code='H101750002032.01', name='信息系统安全', teacher='毛志勇', credit='2',
                                           schedules=[
                                               schemas.CourseTableSchedule(room='静远楼344',
                                                                           weeksString='4-11',
                                                                           weeks=[4, 5, 6, 7, 8, 9, 10, 11],
                                                                           weekday=4, index=2),
                                               schemas.CourseTableSchedule(room='静远楼344',
                                                                           weeksString='4-11',
                                                                           weeks=[4, 5, 6, 7, 8, 9, 10, 11],
                                                                           weekday=2, index=2)])
        with db():
            db.session.merge(models.CourseTable(**course_table.dict()))
            db.session.commit()

    def test_education_grade(self):
        grade = schemas.Grade(name='会计学', credit='2.5', semester='2019-20202', status='正常', result='99',
                              code='H101730004040.01', courseType='专业必修', usual='17', midTerm='', endTerm='99',
                              point='3.5', makeUpScore=None, makeUpScoreResult=None)
        with db():
            db.session.merge(models.Grade(username=1000, **grade.dict()))
            db.session.commit()

    def test_education_grade_table(self):
        grade_table = schemas.GradeTable(name='微机原理（双语）', credit='2.5', semester='2019-2020(1)', status='正常',
                                         result='98')
        with db():
            db.session.merge(models.GradeTable(username=1000, **grade_table.dict()))
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
