from enum import Enum

import requests
from lxml import etree

from app import exceptions


class URLEnum(Enum):
    URL_ROOT = 'http://202.199.224.119:8080/eams'

    # private urls
    LOGIN = URL_ROOT + '/loginExt.action'
    STUDENT_INFO = URL_ROOT + '/stdInfoApply!stdInfoCheck.action'
    COURSE_TABLE = URL_ROOT + '/courseTableForStd!courseTable.action'
    COURSE_TABLE_OF_STD_IDS = URL_ROOT + '/courseTableForStd!innerIndex.action'
    GRADE = URL_ROOT + '/teach/grade/course/person!historyCourseGrade.action'
    GRADE_TABLE = URL_ROOT + '/teach/grade/course/person!report.action'

    EXAM_OF_BATCH_ID = URL_ROOT + '/stdExamTable!innerIndex.action'
    EXAM = URL_ROOT + '/stdExamTable!examTable.action'
    OTHER_EXAM = URL_ROOT + '/stdOtherExamSignUp.action'
    PLAN = URL_ROOT + '/myPlanCompl.action'

    EVALUATE = URL_ROOT + '/quality/stdEvaluate!innerIndex.action'
    EVALUATE_SUBMIT = URL_ROOT + '/quality/stdEvaluate!finishAnswer.action'

    # CLASSROOMS = URL_ROOT + '/classroom/apply/free!search.action'
    # 公开课:http://202.199.224.119:8080/eams/stdSyllabus!search.action?lesson.project.id=1&lesson.semester.id=620
    # 校历:http://202.199.224.119:8080/eams/schoolCalendar!search.action?semester.id=620

    # public urls
    EDU_URL = 'http://jwzx.lntu.edu.cn/'
    NOTICE_URL = 'http://jwzx.lntu.edu.cn/index/jwgg.htm'  # 教务通告
    CAMPUS_CALENDAR_URL = 'http://jwzx.lntu.edu.cn/index/xl.htm'  # 校历
    CLASSROOM_STATUS_URL = 'http://jwzx.lntu.edu.cn/info/1086/1116.htm'  # 查询空教室

    def __str__(self):
        return self.value


def get_all_urls() -> dict:
    try:
        url_dict = {}
        response = requests.get(URLEnum.EDU_URL.value)
        html_doc = etree.HTML(response.text)
        p_elements = html_doc.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div/p')
        data = [each.xpath('a/@href') for each in p_elements]
        url_dict['outer_urls'] = data[0]
        url_dict['inner_urls'] = data[1]
        url_dict['select_course_urls'] = data[2]
        url_dict['teacher_urls'] = data[3]
        return url_dict
    except requests.RequestException as e:
        raise exceptions.NetworkException(f'请求错误: {e}')
    except IndexError as e:
        raise exceptions.NetworkException(f'官网爆炸，抓不到: {e}')


def ping(url) -> float:
    try:
        response = requests.head(url, timeout=(0.1, 2))
        cost_ms = response.elapsed.total_seconds() * 1000
        return cost_ms
    except requests.ConnectionError:
        return 99999.9
