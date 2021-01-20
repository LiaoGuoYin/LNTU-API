import unittest

from app.schemas import NotificationSubscriptionEnum
from appPush.push import apple_push

device_token_list = ['s4zp3NhVmleBqFnsiqtjlwvahOq6qwy7KZE1v24jXdU=']


class TestAppPush(unittest.TestCase):
    def testPushNotice(self):
        apple_push(NotificationSubscriptionEnum.NOTICE.value, '教务在线发新通知啦!', 'Pytest 测试',
                   device_token_list)


if __name__ == '__main__':
    unittest.main()
