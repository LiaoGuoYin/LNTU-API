from django.test import TestCase

from Spider.Capture.Client import Client
from Spider.models import User, CET


class HomePageTest(TestCase):
    """Test whether out blog entiries shop up on the homepage"""

    def setUp(self) -> None:
        User.objects.create(userId=1710030215, password="****")
        # self.client = Client(username=self.user.userId, password=self.user.password)
        self.test_db_data()
        self.test_client_login()
        self.test_CET()

    def test_db_data(self):
        self.user = User.objects.get(pk=1710030215)
        self.username = self.user.userId
        self.password = self.user.password

    def test_client_login(self):
        self.client = Client(username=self.username, password=self.password)
        self.assertTrue(self.client)

    def test_CET(self):
        # CET.objects.create(level="cet4", exam_date=timezone.now(), score=388.0, userId=self.user)
        self.client.getCET()
        # 301 重定向才是成功, 200 密码错误，503 是爆炸
        self.assertIsNotNone(CET.objects.first())
