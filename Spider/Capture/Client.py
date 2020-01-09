import requests
from lxml import etree

from Spider.Capture.EvaluateTeacher import run as evaluate_run


# from Spider.models import Score

class Client(object):

    def __init__(self, userName: int, password: str):
        self.url = 'http://s2.natfrp.com:7792/academic/'
        # self.url = 'http://202.199.224.24:11189/academic/'
        # self.url = 'http://202.199.224.24:11089/newacademic/'
        self.session = requests.Session()
        self.login_with_account(userName, password)

    def login_with_account(self, userName: int, password: str):
        data = {'j_username': userName, 'j_password': password}
        url = self.url + 'j_acegi_security_check'
        response = self.session.post(url, data)
        if response.text.find('本科生教务管理系统') != -1:
            cookie = response.request.headers.get('Cookie')
            self.session.headers.update({'Cookie': cookie})
            print(self.session.headers['Cookie'])
            print('Login success!')
            return True
        else:
            # TODO 错误提示：密码不匹配!
            print('Login failed, Password or UserName is invalid.')
            return False

    def getScores(self):
        url = self.url + 'student/queryscore/queryscore.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        course_lists = html_doc.xpath('/html/body/table[2]/tr')
        score_results = {}
        for course in course_lists[1:]:
            score = Score()
            score.strId = course.xpath('td[1]/text()')[0]
            score.name = course.xpath('td[2]/text()')[0]
            score.numberId = course.xpath('td[3]/text()')[0]
            score.scores = course.xpath('td[4]/font/text()')
            score.scores = course.xpath('td[4]/text()')[0].split()[0] if len(score.scores) == 0 else \
                score.scores[0].split()[0]
            score.credit = course.xpath('td[5]/text()')[0]
            score.check_method = course.xpath('td[6]/text()')[0]
            score.select_properties = course.xpath('td[7]/text()')[0].split()[0]
            score.status = course.xpath('td[8]/text()')[0]
            score.exam_status = course.xpath('td[9]/text()')[0]
            score.semester_year = course.xpath('td[10]/text()')[0][:4]
            score.semester_season = course.xpath('td[10]/text()')[0][4:]
            score.is_slow_examine = course.xpath('td[11]/text()')[0]
            score.details_print_id = course.xpath('td[12]/a/@href')
            score.details_print_id = None if len(score.details_print_id) == 0 else score.details_print_id[0]
            score_results.update({score.name: score.__dict__})
        for k, v in score_results.items():
            if v.get('details_print_id') is not None:
                print('{} {}'.format(k, v.get('scores')), end=' ')
                self.getDetail(v.get('details_print_id'))
        return "Getting Grades done.."

    def getDetail(self, details_print_id):
        details = {}
        url = self.url + 'student/queryscore/' + details_print_id
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        detail_element = html_doc.xpath('/html/body/center/table')[0]
        details['score_composition'] = detail_element.xpath('tr[5]/td/p/b/text()')[0].strip()
        details['daily_score'] = detail_element.xpath('tr[7]/td[1]/b/text()')[0].strip()
        details['midterm_score'] = detail_element.xpath('tr[7]/td[2]/b/text()')[0].strip()
        details['exam_score'] = detail_element.xpath('tr[7]/td[3]/b/text()')[0].strip()
        details['final_score'] = detail_element.xpath('tr[7]/td[4]/b/text()')[0].strip()
        print(details)

    def getCET(self):
        url = self.url + 'student/queryscore/skilltestscore.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        CETs = html_doc.xpath('/html/body/table[2]/tr[@class="infolist_common"]')
        for each in CETs:
            CET_level = each.xpath('td[1]/text()')[0].strip()
            CET_datetime = each.xpath('td[2]/text()')[0].strip()
            CET_score = each.xpath('td[3]/text()')[0].strip()
            print(CET_level, CET_datetime, CET_score)

    def evaluateTeacher(self):
        evaluate_run(self.session.headers["Cookie"])

    def getExamTime(self):
        url = self.url + 'student/exam/index.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        nodes = html_doc.xpath('/html/body/table[2]/tr[@class="infolist_common"]')
        exams = []
        for node in nodes:
            exam = node.xpath('td/text()')
            exams.append({exam[0]: [detail.strip() for detail in exam[1:]]})
        print(exams)

    def getClassTable(self):
        pass

    def selectBestURLLine(self):
        pass


# print(etree.tostring(html_doc, encoding='unicode'))
# with open('output.html', 'w+') as fp:
#     fp.write(etree.tostring(html_doc.xpath('/html')[0], encoding="unicode"))


# with open('account.txt', 'r') as fp:
#     users = fp.readlines()
# for user in users:
#     username, password = user.split("----")
#     print(username, password)
#     client = Client(username.strip(), password.strip())
#     client.evaluateTeacher()
# client.getScores()


client = Client(1710031111, '****')
client.getCET()
# client.getScores()
# client.getExamTime()
# client.evaluateTeacher()
