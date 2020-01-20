import requests
from lxml import etree

from Spider.core.EvaluateTeacher import run as evaluate_run
from Spider.models import Score, CET, ExamPlan, User, StudentInfo
from Spider.utils.URLManager import URLManager


class Client(object):

    def __init__(self, username: int, password: str):
        url_manager = URLManager()
        urls = url_manager.getURLS()
        # self.url = 'http://s2.natfrp.com:7792/academic/'
        # self.url = 'http://202.199.224.121:11189/newacademic/'
        # self.url = 'http://202.199.224.121:11089/newacademic/'
        self.url = urls[1].split("common/security/login.jsp")[0]
        self.session = requests.Session()
        if self.login_with_account(username, password):
            self.user = User.objects.filter(username=username, password=password).first()
            if self.user:
                pass
            else:
                self.user = User(username=username, password=password)
                self.user.save()
        else:
            # 重新输入密码
            pass

    def login_with_account(self, username: int, password: str):
        url = self.url + 'j_acegi_security_check'
        print(url)
        body = {'j_username': username, 'j_password': password}
        response = self.session.post(url, data=body)
        if response.text.find('本科生教务管理系统') != -1:  # TODO 优化判断
            return True
        else:
            # TODO 错误：密码不匹配!
            # print(response.text)
            print('Login failed, Password | UserName is invalid or Teaching Management Online has done.')
            return False

    def getScores(self):
        url = self.url + 'student/queryscore/queryscore.jsdo'
        response = self.session.get(url)
        html = response.text.replace('<font color="#CC0000">', '').replace('</font>', '').replace(
            '<a target="_blank" href="', '').replace('">打印</a>', '')  # 破坏指定元素的结构，方便有效率地统一提取
        html_doc = etree.HTML(html)
        course_lists = html_doc.xpath('/html/body/table[2]/tr')
        for course in course_lists[1:]:
            score = Score()
            score.username = self.user
            score.strId = course.xpath('td[1]/text()')[0]
            score.name = course.xpath('td[2]/text()')[0]
            score.numberId = course.xpath('td[3]/text()')[0]
            score.scores = course.xpath('td[4]')[0].text.strip()  # 破坏1：挂科成绩和正常成绩标签不同
            score.credit = course.xpath('td[5]/text()')[0]
            score.check_method = course.xpath('td[6]/text()')[0]
            score.select_properties = course.xpath('td[7]/text()')[0].split()[0]
            score.status = course.xpath('td[8]/text()')[0]
            score.exam_status = course.xpath('td[9]/text()')[0]
            score.semester_year = course.xpath('td[10]/text()')[0][:4]
            score.semester_season = course.xpath('td[10]/text()')[0][4:]
            score.is_delay_exam = course.xpath('td[11]/text()')[0]
            score.details_print_id = course.xpath('td[12]')[0].text  # 破坏2：有的课程没有打印 id
            score.save()

    def getDetail(self, score):
        if score:
            score = score[0]
            url = self.url + 'student/queryscore/' + score.details_print_id  # 保留 id，以后应该也能看
            response = self.session.get(url)
            html_doc = etree.HTML(response.text)
            detail_element = html_doc.xpath('/html/body/center/table')[0]
            score.score_composition = detail_element.xpath('tr[5]/td/p/b/text()')[0].strip()
            score.daily_score = detail_element.xpath('tr[7]/td[1]/b/text()')[0].strip()
            score.midterm_score = detail_element.xpath('tr[7]/td[2]/b/text()')[0].strip()
            score.exam_score = detail_element.xpath('tr[7]/td[3]/b/text()')[0].strip()
            score.final_score = detail_element.xpath('tr[7]/td[4]/b/text()')[0].strip()
            score.save()
        else:
            pass

    def getCET(self):
        url = self.url + 'student/queryscore/skilltestscore.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        CETs = html_doc.xpath('/html/body/table[2]/tr[@class="infolist_common"]')
        for each in CETs:
            cet = CET()
            cet.username = self.user
            cet.level = each.xpath('td[1]/text()')[0].strip()
            cet.exam_date = each.xpath('td[2]/text()')[0].strip()
            cet.score = each.xpath('td[3]/text()')[0].strip()
            if CET.objects.filter(username=cet.username, exam_date=cet.exam_date).exists():
                print(cet)
            else:
                cet.save()
        # return str(cet.__dict__)

    def evaluateTeacher(self):
        evaluate_run(self.session.headers["Cookie"])

    def getExamPlan(self):
        url = self.url + 'student/exam/index.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        elements = html_doc.xpath('/html/body/table[2]/tr[@class="infolist_common"]')
        for element in elements:
            exam = ExamPlan()
            exam.username = self.user
            exam.name = element.xpath('td[1]/text()')[0]
            exam.date, exam.time = element.xpath('td[2]/text()')[0].split()
            exam.location = element.xpath('td[3]/text()')[0]
            exam.save()

    def getClassTable(self):
        pass

    def getStudentInfo(self):
        url = self.url + '/student/studentinfo/studentinfo.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        student = StudentInfo()
        table = html_doc.xpath('/html/body/center/table[1]')[0]

        student.number = table.xpath('tr[1]/td[1]')[0].text.strip()
        student.citizenship = table.xpath('tr[1]/td[2]')[0].text.strip()
        student.name = table.xpath('tr[2]/td[1]')[0].text.strip()
        student.native_from = table.xpath('tr[2]/td[2]')[0].text.strip()
        student.foreign_name = table.xpath('tr[3]/td[1]')[0].text.strip()
        # student.birthday = table.xpath('tr[3]/td[2]')[0].text.strip()
        student.card_kind = table.xpath('tr[4]/td[1]')[0].text.strip()
        student.politics = table.xpath('tr[4]/td[1]')[0].text.strip()
        student.ID_number = table.xpath('tr[5]/td[1]')[0].text.strip()
        student.section = table.xpath('tr[5]/td[2]')[0].text.strip()
        student.gender = table.xpath('tr[6]/td[1]')[0].text.strip()
        student.nation = table.xpath('tr[6]/td[2]')[0].text.strip()
        student.academy = table.xpath('tr[7]/td[1]')[0].text.strip()
        student.major = table.xpath('tr[7]/td[2]')[0].text.strip()
        student.class_number = table.xpath('tr[8]/td[1]')[0].text.strip()
        student.category = table.xpath('tr[8]/td[2]')[0].text.strip()
        student.province = table.xpath('tr[9]/td[1]')[0].text.strip()
        student.score = table.xpath('tr[9]/td[2]')[0].text.strip()
        student.exam_number = table.xpath('tr[10]/td[1]')[0].text.strip()
        student.graduate_from = table.xpath('tr[10]/td[2]')[0].text.strip()
        student.foreign_language = table.xpath('tr[11]/td[1]')[0].text.strip()
        student.enroll_number = table.xpath('tr[11]/td[2]')[0].text.strip()
        student.enroll_method = table.xpath('tr[12]/td[1]')[0].text.strip()
        # student.enroll_at = table.xpath('tr[12]/td[2]')[0].text.strip()
        # student.graduate_at = table.xpath('tr[13]/td[1]')[0].text.strip()
        student.train_method = table.xpath('tr[13]/td[2]')[0].text.strip()
        student.address = table.xpath('tr[14]/td[1]')[0].text.strip()
        student.zip = table.xpath('tr[14]/td[2]')[0].text.strip()
        student.phone = table.xpath('tr[15]/td[1]')[0].text.strip()
        student.email = table.xpath('tr[15]/td[2]')[0].text.strip()
        student.roll_number = table.xpath('tr[16]/td[1]')[0].text.strip()
        student.source_from = table.xpath('tr[16]/td[2]')[0].text.strip()
        student.graduate_to = table.xpath('tr[17]/td[1]')[0].text.strip()
        student.comment = table.xpath('tr[18]/td[1]')[0].text

        student.save()


def selectBestURL(self):
    pass
