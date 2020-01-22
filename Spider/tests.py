from django.test import TestCase

from Spider.core.Client import Client


# sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 项目路径
# os.environ.update({'DJANGO_SETTINGS_MODUEL': "LNTUME.settings"})
# django.setup()


class ClientTest(TestCase):

    def test_client_method(self):
        client = Client(1710030111, "****")
        client.getStudentInfo()
        client.getScores()
        client.getCET()
        client.getExamPlan()
        client.getClassTable()
        client.getDetail()
