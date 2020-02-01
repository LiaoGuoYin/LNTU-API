import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'LNTUME.settings'
django.setup()

from client import Client, User
from spider.core.classroom import buildings, classroom_fresh
from spider.core.gpa import calculateGPA


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


def test_gpa(username):
    # years = [2018, 2019]
    # seasons = ["春", "秋"]
    # semesters = [str(year) + str(season)
    #              for year in years
    #              for season in seasons]
    # print(semesters)
    # for semester in semesters[-1:]:
    #     scores = Score.objects.filter(username_id=1710030120, semester=semester)
    #     calculateGPA(scores)
    users = User.objects.filter(username=1710030101)
    for user in users:
        user.latest_GPA = calculateGPA(user)
        print(user)


def main():
    # conf = ConfigParser()
    # conf.read('/Users/liaoguoyin/Desktop/LNTUME/static/config.ini')
    # for username, password in conf.items("account")[5:5]:
    #     login(username, password)
    # print("Done..")
    test_gpa(1710030215)


if __name__ == '__main__':
    main()
