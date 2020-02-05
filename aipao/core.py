import time

import requests
from lxml import etree

from aipao.models import Student, Failure, Success

RECORD_URL = "http://sportsapp.aipao.me/MyResults.ashx"
INFO_URL = "http://sportsapp.aipao.me/Manage/UserDomain_SNSP_Records.aspx/MyResutls?userId="


class Client(object):

    def __init__(self, sunnyId):
        self.param_data = {}
        self.sunnyId = sunnyId
        self.student = Student.objects.get_or_create(sunny_id=sunnyId)[0]
        self._initInfo()
        self._freshCounts()
        self.student.save()

    def getSuccess(self, pageNo=1):
        self.param_data = {
            'sunnyId': self.sunnyId,
            'pageNo': pageNo,
            'type': 0,  # 0是成功记录
        }
        response = requests.get(RECORD_URL, params=self.param_data)
        records = response.json()['Records']
        for each in records:
            IIDD = each['IIDD']
            record = Success.objects.get_or_create(IIDD=IIDD, student=self.student)[0]
            record.cost_time_min = each['CosttimeBefore']
            record.userId = each['UserName']
            record.type = each['SportType']
            record.client_type = each['LinkPoint']
            record.speed = each['Speed']
            record.cost_time_s = each['CostTime']
            record.distance = each['CostDistance']
            record.standard_distance = each['AvaLengths']
            record.date = each['ResultDateFmt']
            time_array = time.localtime(int(each['BuildDate'][6:-5]))
            record.time = time.strftime("%H:%M:%S", time_array)
            record.name = each['NickName']
            record.step = each['StepNum']
            record.save()

    def getFailure(self, pageNo=1):
        self.param_data = {
            'sunnyId': self.sunnyId,
            'pageNo': pageNo,
            'type': 1,  # 1是失败记录
        }
        response = requests.get(RECORD_URL, params=self.param_data)
        records = response.json()['Records']
        for each in records:
            IIDD = each['IIDD']
            record = Failure.objects.get_or_create(IIDD=IIDD, student=self.student)[0]
            record.reason = each['ReasonFmt']
            record.reason_id = each['NoCountReason']
            record.cost_time_min = each['CosttimeBefore']
            record.userId = each['UserName']
            record.type = each['SportType']
            record.client_type = each['LinkPoint']
            record.speed = each['Speed']
            record.cost_time_s = each['CostTime']
            record.distance = each['CostDistance']
            record.standard_distance = each['AvaLengths']
            record.date = each['ResultDateFmt']
            time_array = time.localtime(int(each['BuildDate'][6:-5]))
            record.time = time.strftime("%H:%M:%S", time_array)
            record.name = each['NickName']
            record.step = each['StepNum']
            record.save()

    def _initInfo(self):
        url = INFO_URL + str(self.sunnyId)
        response = requests.get(url)
        html_doc = etree.HTML(response.text)
        self.student.morning_records = html_doc.xpath('/html/body/header/div[2]/div[1]/span[2]/text()')[0]
        info_elements = html_doc.xpath('/html/body/header/div[2]/div[2]/div/div[2]/*')
        personal_info = [each.text for each in info_elements]
        school_info_elements = html_doc.xpath('/html/body/header/div[3]/a')
        school_info = [each.text for each in school_info_elements]
        self.student.name = personal_info[0]
        self.student.gender = personal_info[2]
        self.student.number = personal_info[3]
        self.student.school = school_info[0]
        self.student.college = school_info[1]
        self.student.i_class = F"{school_info[2]} {school_info[3]}".strip()

    def _freshCounts(self):
        URL_SUCCESS = F"http://client3.aipao.me/api/%7Btoken%7D/QM_Runs/getResultsofValidByUser?UserId={self.sunnyId}&pageIndex=1&pageSize=1"
        URL_FAILURE = F"http://client3.aipao.me/api/%7Btoken%7D/QM_Runs/getResultsofInValidByUser?UserId={self.sunnyId}&pageIndex=1&pageSize=1"
        response_success = requests.get(URL_SUCCESS)
        response_failure = requests.get(URL_FAILURE)
        self.student.total_records = response_success.json()['AllCount'] + response_failure.json()['AllCount']
        self.student.success_records = response_success.json()['AllCount']
        self.student.failure_records = response_failure.json()['AllCount']

    def __str__(self):
        return F"{self.student.name} 初始化成功 {self.student.__dict__}"
