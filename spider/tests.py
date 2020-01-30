from configparser import ConfigParser
from unittest import TestCase

from client import Client
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 项目路径
# os.environ.update({'DJANGO_SETTINGS_MODUEL': "LNTUME.settings"})
# django.setup()
from core.classroom import buildings, classroom_fresh


class ClientTest(TestCase):

    def setUp(self):
        """load my test account"""
        conf = ConfigParser()
        conf.read('static/config.ini')
        for username, password in conf.items("account")[0:1]:
            self.client = Client(username, password)
            print(self.client)
            self.test_client_method()

    def test_client_method(self):
        """test one client's all methods"""
        self.client.getStudentInfo()
        self.client.getTeachingPlan()
        self.client.getClassTable()
        self.client.getScores()
        self.client.getCET()
        self.client.getExamPlan()
        self.client.getClassTable()
        self.client.getDetail()

    def test_class_room(self):
        """test spider classroom"""
        for building in buildings:
            for room_data in building:
                room_data['weeks'] = 10  # TODO 周次
                print(room_data)
                classroom_fresh(room_data=room_data)
