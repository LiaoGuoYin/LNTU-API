import hashlib
import time

from lxml import etree
from requests import Session

from core.parser import LNTUParser
from util import Logger, search_all

# TODO enum
URL_ROOT = 'http://202.199.224.119:8080/eams'
LOGIN = URL_ROOT + '/loginExt.action'
STUDENT_INFO = URL_ROOT + '/stdDetail.action'
CLASS_TABLE = URL_ROOT + '/courseTableForStd!courseTable.action'
CLASS_TABLE_OF_STD_IDS = URL_ROOT + '/courseTableForStd.action'
# SCORE = '/teach/grade/course/person!search.action'
ALL_SCORES = URL_ROOT + '/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR'


# fetchScore = URL_ROOT + '/teach/grade/course/person!historyCourseGrade.action'
# classroom = URL_ROOT + '/classroom/apply/free!search.action'
# courseTable = URL_ROOT + '/courseTableForStd!courseTable.action'
# courseTask = URL_ROOT + '/courseTableForStd!taskTable.action'


def log_in(username, password):
    url = LOGIN
    session = Session()
    response = session.get(url)
    token = search_all(
        u"form['password'].value = CryptoJS.SHA1('{}' + form['password'].value);", response.text)[0][0]
    print(token)
    key = hashlib.sha1((token + password).encode('utf-8')).hexdigest()
    data = {'username': username, 'password': key}
    time.sleep(0.5)
    response = session.post(url, data=data)
    if '密码错误' in response.text:
        Logger().e('login', '密码错误')
        raise Exception("密码错误")
    elif '请不要过快点击' in response.text:
        Logger().e('login', '点击过快（错误太多）')
        return Exception("点击过快（错误太多）")
    elif '您当前位置' in response.text:
        print(F"登陆成功: {response.request.headers['Cookie']}")
        return session
    else:
        return Exception("未知错误")


def get_std_ids(session):
    """课表查询之前，一定要访问，因此只支持 session 模式"""
    url = CLASS_TABLE_OF_STD_IDS
    response = session.get(url)
    stu_id = search_all('(form,"ids","{}");', html=response.text)[0][0]
    print(stu_id)
    return stu_id


def get_class_table(username, password, semester=626, session=None):
    url = CLASS_TABLE
    if not session:
        session = log_in(username, password)
    """获取课表之前必须访问 get_std_id() """
    ids = get_std_ids(session)
    data = {
        'ignoreHead': 1,
        'startWeek': 1,
        'setting.kind': "std",
        'ids': ids,
        'semester.id': semester,
    }
    response = session.post(url, data=data)
    html_text = response.text
    html_doc = etree.HTML(html_text)
    print(html_text)
    # save_html(html_text)
    all_course_dict = LNTUParser.parse_class_table_bottom(html_doc)
    # print(all_course_dict)
    results = LNTUParser.parse_class_table_body(html_text=html_text, all_course_dict=all_course_dict)
    print(results)
    return results


def get_std_info(username, password, session=None):
    if not session:
        session = log_in(username, password)
    url = STUDENT_INFO
    response = session.get(url)
    if "学籍信息" in response.text:
        # save_html(response.text)
        html_doc = etree.HTML(response.text)
        results = LNTUParser.parse_std_info(html_doc)
        print(results)
        return results
    else:
        return 503
        # TODO


def get_all_scores(username, password, session=None):
    if not session:
        session = log_in(username, password)
    url = ALL_SCORES
    response = session.post(url)
    if "学年学期" in response.text:
        html_doc = etree.HTML(response.text)
        # save_html(response.text)
        results = LNTUParser.parse_all_scores(html_doc=html_doc)
        print(results)
        return results
    else:
        return 503


def get_all_GPAs(username, password, session=None):
    if not session:
        session = log_in(username, password)
    url = ALL_SCORES
    response = session.post(url)
    if "学年学期" in response.text:
        html_doc = etree.HTML(response.text)
        results = LNTUParser.parse_all_GPAs(html_doc=html_doc)
        print(results)
        return results
    else:
        return 503
