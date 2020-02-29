import hashlib
import time

from requests_html import HTMLSession

from core.parser import LNTUParser
from util import Logger

URL_ROOT = 'http://202.199.224.119:8080/eams'
LOGIN = URL_ROOT + '/loginExt.action'
STUDENT_INFO = URL_ROOT + '/stdDetail.action'
CLASS_TABLE = URL_ROOT + '/courseTableForStd!courseTable.action'
CLASS_TABLE_OF_STD_IDS = URL_ROOT + '/courseTableForStd.action'


# fetchScore = URL_ROOT + '/teach/grade/course/person!historyCourseGrade.action'
# classroom = URL_ROOT + '/classroom/apply/free!search.action'
# courseTable = URL_ROOT + '/courseTableForStd!courseTable.action'
# courseTask = URL_ROOT + '/courseTableForStd!taskTable.action'


def log_in(username, password):
    url = LOGIN
    session = HTMLSession()
    response = session.get(url)
    token = response.html.search(
        u"    		form['password'].value = CryptoJS.SHA1('{}' + form['password'].value);")[0]
    key = hashlib.sha1((token + password).encode('utf-8')).hexdigest()
    data = {'username': username, 'password': key}
    time.sleep(0.5)
    response = session.post(url, data=data)
    if '密码错误' in response.text:
        Logger().e('login', '密码错误')
        return False
    elif '请不要过快点击' in response.text:
        Logger().e('login', '点击过快（错误太多）')
        return False
    else:
        print(F"登陆成功: {response.request.headers['Cookie']}")
        return session


def get_std_ids(session):
    """课表查询之前，一定要访问，因此只支持 session 模式"""
    url = CLASS_TABLE_OF_STD_IDS
    response = session.get(url)
    stu_id = response.html.search('(form,"ids","{}");')[0]
    print(stu_id)
    return stu_id


def get_class_table(username, password, semester=626, session=None):
    url = CLASS_TABLE
    if not session:
        session = log_in(username, password)
    """获取课表之前必须访问 get_std_id """
    ids = get_std_ids(session)
    data = {
        'ignoreHead': 1,
        'startWeek': 1,
        'setting.kind': "std",
        'ids': ids,
        'semester.id': semester,
    }
    response = session.post(url, data=data)
    html = response.html
    course_total_dict = LNTUParser.parse_class_table_bottom(html)
    LNTUParser.parse_class_table_body(html_text=html.text, course_total_dict=course_total_dict)


def get_std_info(username, password, session=None):
    if not session:
        session = log_in(username, password)
    url = STUDENT_INFO
    response = session.get(url)
    if "学籍信息" in response.text:
        LNTUParser.parse_std_info(response.html)
    else:
        return 503
    # TODO


def main():
    get_class_table('username', 'password')
    get_std_info('password', 'password')


if __name__ == '__main__':
    main()
