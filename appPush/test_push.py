import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import schemas
from app.constants import constantsShared
from appPush import crud
from appPush.push import apple_push
from appPush.tasks import push_grade_every_hour

token_list = ['s4zp3NhVmleBqFnsiqtjlwvahOq6qwy7KZE1v24jXdU=']

notice_push_demo = schemas.NoticePushNotification(
    token=token_list[0],
    contentBody='This is a Test Notice'
)

grade_push_demo = schemas.GradePushNotification(
    token=token_list[0],
    username='88888888',
    courseName='测试课程',
    courseResult='99'
)


class TestAppPush(unittest.TestCase):
    def setUp(self) -> None:
        db_url_dict = constantsShared.get_db_url_dict()
        engine = create_engine(db_url_dict['production'], echo=True)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def testPushNotice(self):
        apple_push(category=schemas.NotificationSubscriptionEnum.NOTICE, body=notice_push_demo.contentBody,
                   device_token=notice_push_demo.token)

    def testPushGrade(self):
        apple_push(category=schemas.NotificationSubscriptionEnum.GRADE, body=grade_push_demo.contentBody,
                   device_token=grade_push_demo.token)

    def testPushGradeEveryHour(self):
        push_grade_every_hour()

    def test_retrieve_need_to_refresh_grades_user_list_with_code(self):
        user_list = crud.retrieve_need_to_refresh_grades_user_list_with_code('H271780001002.A8', self.session)
        [print(user) for user in user_list]

    def test_retrieve_need_to_refresh_grades_user_list(self):
        user_list = crud.retrieve_need_to_refresh_grades_user_list(self.session)
        [print(user) for user in user_list]


if __name__ == '__main__':
    unittest.main()
