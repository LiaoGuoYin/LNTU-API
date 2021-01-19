import unittest

from appPush.push import apple_push

device_token_list = ['s4zp3NhVmleBqFnsiqtjlwvahOq6qwy7KZE1v24jXdU=']


class TestAppPush(unittest.TestCase):
    def testPushNotice(self):
        apple_push('教务在线发新通知啦!', '关于第十二届蓝桥杯全国软件和信息技术专业人才大赛省赛报名', device_token_list)


if __name__ == '__main__':
    unittest.main()
