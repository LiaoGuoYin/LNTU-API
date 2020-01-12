import requests
from lxml import etree

from Spider.Capture.EvaluateTeacher import run as evaluate_run
from Spider.models import Score


class Client(object):

    def __init__(self, username: int, password: str):
        # self.url = 'http://s2.natfrp.com:7792/academic/'
        self.url = 'http://202.199.224.24:11189/academic/'
        # self.url = 'http://202.199.224.24:11089/newacademic/'
        self.session = requests.Session()
        self.login_with_account(username, password)
        self.userId = username
        self.password = password

    def login_with_account(self, username: int, password: str):
        url = self.url + 'j_acegi_security_check'
        form_data = {'j_username': username, 'j_password': password}
        response = self.session.post(url, data=form_data)
        if response.text.find('本科生教务管理系统') != -1:  # TODO 优化判断
            cookie = response.request.headers.get('Cookie')
            self.session.headers.update({'Cookie': cookie})
            return True
        else:
            # TODO 错误：密码不匹配!
            print(response.text)
            print('Login failed, Password | UserName is invalid or Teaching Management Online has done.')
            return False

    def getScores(self):
        url = self.url + 'student/queryscore/queryscore.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        course_lists = html_doc.xpath('/html/body/table[2]/tr')
        score_results = {}
        for course in course_lists[1:]:
            score = Score()
            score.userId = self.userId
            score.strId = course.xpath('td[1]/text()')[0]
            score.name = course.xpath('td[2]/text()')[0]
            score.numberId = course.xpath('td[3]/text()')[0]
            score.scores = course.xpath('td[4]/font/text()')  # 挂科成绩 Element
            score.scores = course.xpath('td[4]/text()')[0].split()[0] if len(str(score.scores)) == 0 else \
                score.scores[0].split()[0]  # 正常成绩 Element
            score.credit = course.xpath('td[5]/text()')[0]
            score.check_method = course.xpath('td[6]/text()')[0]
            score.select_properties = course.xpath('td[7]/text()')[0].split()[0]
            score.status = course.xpath('td[8]/text()')[0]
            score.exam_status = course.xpath('td[9]/text()')[0]
            score.semester_year = course.xpath('td[10]/text()')[0][:4]
            score.semester_season = course.xpath('td[10]/text()')[0][4:]
            score.is_delay_exam = course.xpath('td[11]/text()')[0]
            score.details_print_id = course.xpath('td[12]/a/@href')
            score.details_print_id = None if len(score.details_print_id) == 0 else score.details_print_id[0]
            score_results.update({score.name: score.__dict__})
            score.save()
        for k, v in score_results.items():
            if v.get('details_print_id') is not None:
                print('{} {}'.format(k, v['scores']), end=' ')
                self.getDetail(v['details_print_id'])
                # TODO Test ok?
        return score_results

    def getDetail(self, score: Score):
        url = self.url + 'student/queryscore/' + score.details_print_id  # 保留 id，以后应该也能看
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        detail_element = html_doc.xpath('/html/body/center/table')[0]
        score.score_composition = detail_element.xpath('tr[5]/td/p/b/text()')[0].strip()
        score.daily_score = detail_element.xpath('tr[7]/td[1]/b/text()')[0].strip()
        score.midterm_score = detail_element.xpath('tr[7]/td[2]/b/text()')[0].strip()
        score.exam_score = detail_element.xpath('tr[7]/td[3]/b/text()')[0].strip()
        score.final_score = detail_element.xpath('tr[7]/td[4]/b/text()')[0].strip()

    def getCET(self):
        url = self.url + 'student/queryscore/skilltestscore.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        CETs = html_doc.xpath('/html/body/table[2]/tr[@class="infolist_common"]')
        result_lists = []
        for each in CETs:
            CET_level = each.xpath('td[1]/text()')[0].strip()
            CET_datetime = each.xpath('td[2]/text()')[0].strip()
            CET_score = each.xpath('td[3]/text()')[0].strip()
            result_lists.append([CET_level, CET_datetime, CET_score])
            print(CET_level, CET_datetime, CET_score)
        return result_lists

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


# client = Client(1710030215, '*')
# client.getCET()
# client.getScores()
# client.getExamTime()
# client.evaluateTeacher()
