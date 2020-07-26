from enum import Enum

import requests
from lxml import etree


class URLEnum(Enum):
    URL_ROOT = 'http://202.199.224.119:8080/eams'

    # private urls
    LOGIN = URL_ROOT + '/loginExt.action'
    STUDENT_INFO = URL_ROOT + '/stdDetail.action'
    CLASS_TABLE = URL_ROOT + '/courseTableForStd!courseTable.action'
    CLASS_TABLE_OF_STD_IDS = URL_ROOT + '/courseTableForStd.action'
    GRADES = URL_ROOT + '/teach/grade/course/person!search.action'

    # CLASSROOMS = URL_ROOT + '/classroom/apply/free!search.action'
    # 学期成绩：http://202.199.224.119:8080/eams/teach/grade/course/person!search.action?semesterId = 学期 ID
    # 考试信息：http://202.199.224.119:8080/eams/stdExamTable!examTable.action?examBatch.id = 学期 ID
    # 资格考试：http://202.199.224.119:8080/eams/stdOtherExamSignUp.action
    # 公开课:http://202.199.224.119:8080/eams/stdSyllabus!search.action?lesson.project.id=1&lesson.semester.id=620
    # 校历:http://202.199.224.119:8080/eams/schoolCalendar!search.action?semester.id=620

    # public urls
    EDU_URL = 'http://jwzx.lntu.edu.cn/'
    NOTICE_URL = 'http://jwzx.lntu.edu.cn/index/jwgg.htm'  # 教务通告
    CAMPUS_CALENDAR_URL = 'http://jwzx.lntu.edu.cn/index/xl.htm'  # 校历
    CLASSROOM_STATUS_URL = 'http://jwzx.lntu.edu.cn/info/1086/1116.htm'  # 查询空教室

    def __str__(self):
        return self.value


def get_all_urls():
    try:
        url_dict = {}
        response = requests.get(URLEnum.EDU_URL)
        html_doc = etree.HTML(response.text)
        p_elements = html_doc.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div/p')
        data = [each.xpath('a/@href') for each in p_elements]
        url_dict['outer_urls'] = data[0]
        url_dict['inner_urls'] = data[1]
        url_dict['select_course_urls'] = data[2]
        url_dict['teacher_urls'] = data[3]
        return url_dict
    except requests.RequestException as e:
        return F" 请求错误: {e}"
    except IndexError as e:
        return F" 官网爆炸，抓不到: {e}"


def ping(url):
    try:
        response = requests.head(url, timeout=(0.1, 2))
        cost_ms = response.elapsed.total_seconds() * 1000
        return cost_ms
    except requests.ConnectionError:
        return 99999
