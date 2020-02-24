import requests
from rest_framework import exceptions

from api.models import Score, User
from spider.core.cet import cet_parser
from spider.core.classTable import classTable_parser
from spider.core.examPlan import examPlan_parser
from spider.core.getHTML import get_html_doc, score_get_html_doc
from spider.core.gpa import calculateGPA
from spider.core.scoreDetail import detail_parser
from spider.core.socre import score_parser
from spider.core.studentInfo import studentInfo_parser
from spider.core.teacherEvaluate import run as evaluate_run
from spider.core.teachingPlan import teachingPlan_parser, teachingPlan_get_html
from spider.utils.URLManager import UrlEnums


class Client(object):

    def __init__(self, username: int, password: str):
        # urls = URLManager.run()
        # self.url = urls[1].split("common/security/login.jsp")[0]
        self.session = requests.Session()
        if self.login_with_account(username, password):
            """login success, update username and password"""
            self.user = User.objects.get_or_create(username=username)[0]
            self.user.password = password
            self.user.save()

    def login_with_account(self, username: int, password: str):
        url = UrlEnums.LOGIN
        body = {'j_username': username, 'j_password': password}
        response = self.session.post(url, data=body)
        if response.text.find("本科生教务管理系统", 1, 50) == -1:
            raise exceptions.AuthenticationFailed(
                "用户名或密码错误，或教务在线爆炸")
        else:
            return True

    def getIds(self):
        """Get studentId and classId: uri:./studyschedule_view_byterm.jsdo?studentId=2884862&classId=13925"""
        try:
            url = UrlEnums.TEACHING_PLAN_IDS
            html_doc = get_html_doc(self.session, url)
            element = html_doc.xpath('/html/body/center/table[5]/form/tr/td/input')
            data = element[0].get('onclick').split(r"'")[1]
            self.user.student_id, self.user.class_id = tuple(i.split("=")[1] for i in data.split("&"))
            self.user.save()
            return True
        except Exception as e:
            print(e)
            return False

    def getStudentInfo(self):
        url = UrlEnums.STUDENT_INFO
        html_doc = get_html_doc(self.session, url)
        print("获取个人信息: ", studentInfo_parser(html_doc, self.user), end=', ')

    def getTeachingPlan(self):
        if not self.user.student_id:
            self.getIds()
        uri = F"./studyschedule_view_byterm.jsdo?studentId={self.user.student_id}&classId={self.user.class_id}"
        if uri:
            html_doc = teachingPlan_get_html(self.session, uri)
            print("获取教学计划: ", teachingPlan_parser(html_doc, self.user), end=', ')

    def getClassTable(self, year=39, term=2):
        # TODO
        url = UrlEnums.CLASS_TABLE
        semester_str = F"{year} {term}"
        semester_data = {'params': {'year': year, 'term': term}}
        html_doc = get_html_doc(self.session, url, **semester_data)
        print("获取默认学期学年课表：", classTable_parser(html_doc, self.user, semester_str), end=', ')

    def getExamPlan(self):
        url = UrlEnums.EXAM_PLAN
        html_doc = get_html_doc(self.session, url)
        print("获取考试计划: ", examPlan_parser(html_doc, self.user), end=', ')

    def evaluateTeacher(self):
        evaluate_run(self.session.headers["Cookie"])

    def getScores(self):
        url = UrlEnums.SCORE
        html_doc = score_get_html_doc(self.session, url)
        print("获取成绩: ", score_parser(html_doc, self.user), end=', ')

    def getScoreDetail(self):
        scores = Score.objects.filter(username=self.user, details_print_id__istartswith="chajuandy.jsp")
        isAllOk = {True}
        for score in scores:
            url = str(UrlEnums.SCORES_DETAIL) + score.details_print_id  # 保留 id，以后应该也能看
            html_doc = get_html_doc(self.session, url)
            isOk = detail_parser(html_doc, score)
            isAllOk.add(isOk)
        print("获取成绩详情: ", True if len(isAllOk) == 1 else False, end=', ')

    def calculateGPA(self):
        """Calculate default semeter's GPA"""
        calculateGPA(user=self.user, semester="2018秋")

    def getCET(self):
        url = UrlEnums.CET
        html_doc = get_html_doc(self.session, url)
        print("获取 CET: ", cet_parser(html_doc, self.user), end=', ')

    def selectBestURL(self):
        # TODO
        pass

    def __str__(self):
        return str(self.user) + " 登陆成功"
