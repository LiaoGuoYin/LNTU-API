import requests

from spider.core.EvaluateTeacher import run as evaluate_run
from spider.core.cet import cet_get_html, cet_parser
from spider.core.examPlan import examPlan_get_html, examPlan_parser
from spider.core.scoreDetail import detail_get_html, detail_parser
from spider.core.socre import score_get_html, score_parser
from spider.core.studentInfo import studentInfo_get_html, studentInfo_parser
from spider.utils.UrlEnums import UrlEnums
from web.models import Score, User


class Client(object):

    def __init__(self, username: int, password: str):
        # url_manager = URLManager()
        # urls = url_manager.getURLS()
        # self.url = urls[1].split("common/security/login.jsp")[0]
        # self.url = 'http://202.199.224.24:11089/newacademic/'
        self.session = requests.Session()
        if self.login_with_account(username, password):
            self.user, isExist = User.objects.get_or_create(username=username, password=password)
            if not isExist:
                self.user.save()

    def login_with_account(self, username: int, password: str):
        url = UrlEnums.LOGIN
        print(url)
        body = {'j_username': username, 'j_password': password}
        response = self.session.post(url, data=body)
        if response.text.find("本科生教务管理系统", 1, 50) == -1:
            raise KeyError("错误：Password or UserName is invalid or Teaching Management Online is down.")
        else:
            return True

    def getScores(self):
        html_doc = score_get_html(self.session)
        print("获取成绩: ", score_parser(html_doc, self.user))

    def getDetail(self):
        scores = Score.objects.filter(username=self.user, details_print_id__isnull=False)
        isAllOk = False
        for score in scores:
            details_print_id = score.details_print_id
            if not details_print_id:
                continue
            html_doc = detail_get_html(self.session, details_print_id)
            isAllOk = detail_parser(html_doc, score)
        print("获取成绩详情: ", isAllOk)

    def getCET(self):
        html_doc = cet_get_html(self.session)
        print("获取 CET: ", cet_parser(html_doc, self.user))

    def evaluateTeacher(self):
        evaluate_run(self.session.headers["Cookie"])

    def getExamPlan(self):
        html_doc = examPlan_get_html(self.session)
        print("获取 考试计划: ", examPlan_parser(html_doc, self.user))

    def getClassTable(self):
        # TODO
        pass

    def getStudentInfo(self):
        html_doc = studentInfo_get_html(self.session)
        print("获取个人信息: ", studentInfo_parser(html_doc, self.user))

    def selectBestURL(self):
        # TODO
        pass
