import requests
from lxml import etree

from Spider.core.EvaluateTeacher import run as evaluate_run
from Spider.models import Score, CET, ExamPlan, User, StudentInfo


class Client(object):

    def __init__(self, username: int, password: str):
        # url_manager = URLManager()
        # urls = url_manager.getURLS()
        # self.url = urls[1].split("common/security/login.jsp")[0]
        self.url = 'http://202.199.224.24:11089/newacademic/'
        self.session = requests.Session()
        if self.login_with_account(username, password):
            self.user, isExist = User.objects.get_or_create(username=username, password=password)
            if not isExist:
                self.user.save()

    def login_with_account(self, username: int, password: str):
        url = self.url + 'j_acegi_security_check'
        print(url)
        body = {'j_username': username, 'j_password': password}
        response = self.session.post(url, data=body)
        if response.text.find("本科生教务管理系统", 1, 50) == -1:
            raise KeyError("错误：Password or UserName is invalid or Teaching Management Online has done.")
        else:
            return True

    def getScores(self):
        url = self.url + 'student/queryscore/queryscore.jsdo'
        response = self.session.get(url)
        html = response.text.replace('<font color="#CC0000">', '').replace('</font>', '').replace(
            '<a target="_blank" href="', '').replace('">打印</a>', '')  # 破坏指定元素的结构，方便有效率地统一提取
        html_doc = etree.HTML(html)
        course_lists = html_doc.xpath('/html/body/table[2]/tr')
        for course in course_lists[1:]:  # 舍弃th
            course_id = course.xpath('td[1]/text()')[0]
            semester = course.xpath('td[10]/text()')[0]
            score = Score.objects.get_or_create(username=self.user, semester=semester, course_id=course_id)[0]
            score.name = course.xpath('td[2]/text()')[0]
            score.course_number = course.xpath('td[3]/text()')[0]
            score.scores = course.xpath('td[4]')[0].text.strip()  # 破坏1：挂科成绩和正常成绩标签不同
            score.credit = course.xpath('td[5]/text()')[0]
            score.inspect_method = course.xpath('td[6]/text()')[0]
            score.course_properties = course.xpath('td[7]/text()')[0].split()[0]
            score.status = course.xpath('td[8]/text()')[0]
            score.exam_categories = course.xpath('td[9]/text()')[0]
            score.is_delay_exam = course.xpath('td[11]/text()')[0]
            score.details_print_id = course.xpath('td[12]')[0].text  # 破坏2：有的课程没有打印 id
            if score.details_print_id:
                score.details_print_id = score.details_print_id.strip()
            score.save()

    def getDetail(self):
        scores = Score.objects.filter(username=self.user, details_print_id__isnull=False)
        for score in scores:
            if not score.details_print_id:
                continue
            score.details_print_id = score.details_print_id
            url = self.url + 'student/queryscore/' + score.details_print_id  # 保留 id，以后应该也能看
            response = self.session.get(url)
            html_doc = etree.HTML(response.text)
            # TODO 判断网页内容是否本来就为空
            detail_element = html_doc.xpath('/html/body/center/table')[0]
            score.made_up_of = detail_element.xpath('tr[5]/td/p/b/text()')[0].strip()
            score.daily_score = detail_element.xpath('tr[7]/td[1]/b/text()')[0].strip()
            score.midterm_score = detail_element.xpath('tr[7]/td[2]/b/text()')[0].strip()
            score.exam_score = detail_element.xpath('tr[7]/td[3]/b/text()')[0].strip()
            score.final_score = detail_element.xpath('tr[7]/td[4]/b/text()')[0].strip()
            score.save()

    def getCET(self):
        url = self.url + 'student/queryscore/skilltestscore.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        CETs = html_doc.xpath('/html/body/table[2]')

        for each in CETs[1:]:
            level = each.xpath('td[1]')[0].text.strip()
            if level == "不报名":
                continue
            cet = CET.objects.get_or_create(level=level, username=self.user)[0]
            cet.date = each.xpath('td[2]')[0].text.strip()
            cet.score = each.xpath('td[3]')[0].text.strip()
            cet.save()

    def evaluateTeacher(self):
        evaluate_run(self.session.headers["Cookie"])

    def getExamPlan(self):
        url = self.url + 'student/exam/index.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        elements = html_doc.xpath('/html/body/table[2]/tr[@class="infolist_common"]')
        for element in elements:
            date, time = element.xpath('td[2]/text()')[0].split()
            exam = ExamPlan.objects.get_or_create(username=self.user, date=date, time=time)[0]
            exam.name = element.xpath('td[1]/text()')[0]
            exam.room = element.xpath('td[3]/text()')[0]
            exam.save()

    def getClassTable(self):
        pass

    def getStudentInfo(self):
        url = self.url + '/student/studentinfo/studentinfo.jsdo'
        response = self.session.get(url)
        html_doc = etree.HTML(response.text)
        student = StudentInfo.objects.get_or_create(number=self.user)[0]
        table = html_doc.xpath('/html/body/center/table[1]')[0]

        student.number = table.xpath('tr[1]/td[1]')[0].text.strip()
        student.citizenship = table.xpath('tr[1]/td[2]')[0].text.strip()
        student.name = table.xpath('tr[2]/td[1]')[0].text.strip()
        student.native_from = table.xpath('tr[2]/td[2]')[0].text.strip()
        student.foreign_name = table.xpath('tr[3]/td[1]')[0].text.strip()
        student.birthday = table.xpath('tr[3]/td[2]')[0].text.strip()
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
        student.enroll_at = table.xpath('tr[12]/td[1]')[0].text.strip()
        student.enroll_method = table.xpath('tr[12]/td[2]')[0].text.strip()
        student.graduate_at = table.xpath('tr[13]/td[1]')[0].text.strip()
        student.train_method = table.xpath('tr[13]/td[2]')[0].text.strip()
        student.address = table.xpath('tr[14]/td[1]')[0].text.strip()
        student.zip = table.xpath('tr[14]/td[2]')[0].text.strip()
        student.phone = table.xpath('tr[15]/td[1]')[0].text.strip()
        student.email = table.xpath('tr[15]/td[2]')[0].text.strip()
        student.roll_number = table.xpath('tr[16]/td[1]')[0].text.strip()
        student.source_from = table.xpath('tr[16]/td[2]')[0].text.strip()
        student.graduate_to = table.xpath('tr[17]/td[1]')[0].text.strip()
        student.comment = table.xpath('tr[18]/td[1]')[0].text
        student.img_url = "http://202.199.224.121:11180/newacademic/manager/studentinfo/photo/photo/{}.jpg".format(
            student.number)
        student.save()

    def selectBestURL(self):
        pass
