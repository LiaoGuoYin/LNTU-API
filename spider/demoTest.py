import os
from configparser import ConfigParser

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'LNTUME.settings'
django.setup()

from client import Client
from spider.core.classroom import buildings, classroom_fresh


def test_class_room():
    """test spider classroom"""
    for building in buildings:
        for room_data in building:
            room_data['weeks'] = 10  # TODO 周次
            print(room_data)
            classroom_fresh(room_data=room_data)


def login(username, password):
    try:
        client = Client(username, password)
        client.getStudentInfo()
        client.getTeachingPlan()
        client.getClassTable()
        client.getScores()
        client.getScoreDetail()
        client.getCET()
        client.getExamPlan()
        print(client.user, "success")
    except Exception as e:
        print(username, e)


def main():
    conf = ConfigParser()
    conf.read('/Users/liaoguoyin/Desktop/LNTUME/static/config.ini')
    for username, password in conf.items("account"):
        login(username, password)
    print("Done..")


if __name__ == '__main__':
    main()
