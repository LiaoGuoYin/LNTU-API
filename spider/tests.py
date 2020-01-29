from configparser import ConfigParser
from unittest import TestCase

from client import Client


# sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 项目路径
# os.environ.update({'DJANGO_SETTINGS_MODUEL': "LNTUME.settings"})
# django.setup()


class ClientTest(TestCase):

    def setUp(self):
        """load my test account"""
        conf = ConfigParser()
        conf.read('static/config.ini')
        for username, password in conf.items("account")[0:1]:
            self.client = Client(username, password)
            print(self.client)

    def test_client_method(self):
        # self.client.getStudentInfo()
        self.client.getTeachingPlan()
        self.client.getClassTable()
        # self.client.getScores()
        # self.client.getCET()
        # self.client.getExamPlan()
        # self.client.getClassTable()
        # self.client.getDetail()
