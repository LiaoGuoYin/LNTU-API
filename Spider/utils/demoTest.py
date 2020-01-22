import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'LNTUME.settings'
django.setup()

from Spider.core.Client import Client


def login(username, password):
    try:
        client = Client(username, password)
        client.getStudentInfo()
        client.getScores()
        client.getDetail()
        client.getCET()
        client.getExamPlan()
        client.getClassTable()
        print(client.user.username, "success")
    except Exception as e:
        print(username, e)
        print(e)


def main():
    with open("test.txt", 'r') as fp:
        account_lists = fp.readlines()
    for account in account_lists:
        username, password = account.strip().split("----")
        login(username, password)
    print("Done..")


if __name__ == '__main__':
    main()
