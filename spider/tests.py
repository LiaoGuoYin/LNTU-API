from client import Client


# sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 项目路径
# os.environ.update({'DJANGO_SETTINGS_MODUEL': "LNTUME.settings"})
# django.setup()


# class ClientTest(TestCase):
class ClientTest(object):

    def test_client_method(self):
        client = Client(1710030215, "****")
        client.getStudentInfo()
        client.getScores()
        client.getCET()
        client.getExamPlan()
        client.getClassTable()
        client.getDetail()


ClientTest().test_client_method()
