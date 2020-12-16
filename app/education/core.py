import hashlib
import re
import time

import parse
import requests
from lxml import etree
from requests import Session

from app import schemas, exceptions
from app.education import parser
from app.education.urls import URLEnum
from app.education.utils import save_html_to_file
from app.constants import constantsShared


def is_education_online() -> bool:
    try:
        response = requests.head(URLEnum.LOGIN.value, timeout=(1, 3))
        if response.status_code == 200:
            return True
        else:
            raise exceptions.NetworkException("教务无响应，爆炸爆炸")
    except (requests.exceptions.RequestException, requests.exceptions.RequestException, exceptions.NetworkException):
        return False


def login(username: str, password: str) -> Session:
    if not is_education_online():
        raise exceptions.NetworkException("教务无响应，爆炸爆炸")
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (HTML, like Gecko) '
                      'Chrome/86.0.4240.111 Safari/537.36',
        'Connection': 'close',
    }
    session.keep_alive = False
    response = session.get(URLEnum.LOGIN.value)
    token = re.findall(r"SHA1\('(.*?)'", response.text)[0]
    if token is None:
        raise exceptions.SpiderParserException("页面上没找到 SHA1token")
    key = hashlib.sha1((token + password).encode('utf-8')).hexdigest()
    time.sleep(0.48)  # 延迟 0.48 秒防止被 ban
    response = session.post(URLEnum.LOGIN.value, data={'username': username, 'password': key})
    if '密码错误' in response.text:
        raise exceptions.FormException(F"{username} 用户名或密码错误")
    elif '请不要过快点击' in response.text:
        raise exceptions.AccessException("页面请求过快")
    elif '账户不存在' in response.text:
        raise exceptions.FormException(F"{username} 用户不存在")
    elif '超过人数上限' in response.text:
        raise exceptions.FormException("超过人数上限，请稍后再试")
    elif '您当前位置' in response.text:
        return session
    elif 'security.AccountExpired' in response.text:
        raise exceptions.FormException("账号已到期，可能是已经毕业")
    else:
        raise exceptions.AccessException("页面未知错误")


def get_stu_info(username: str, password: str, session=None, is_save: bool = False) -> schemas.UserInfo:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.STUDENT_INFO.value)
    if "学籍信息" in response.text:
        if is_save:
            save_html_to_file(response.text, 'info')
        html_doc = etree.HTML(response.text)
        return parser.parse_stu_info(html_doc)
    else:
        raise exceptions.SpiderParserException("[个人信息页]获取失败")


def get_plan(username: str, password: str, session: Session = None, is_save: bool = False) -> [schemas.PlanGroup]:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.PLAN.value)
    if is_save:
        save_html_to_file(response.text, 'plan')
    if '计划完成情况' in response.text:
        return parser.parse_plan(html_doc=etree.HTML(response.text))
    else:
        raise exceptions.SpiderParserException("[个人培养方案完成情况页]获取失败")


def get_course_table(username: str, password: str, semester_id: int = constantsShared.current_semester_id,
                     session: Session = None,
                     is_save: bool = False) -> [schemas.CourseTable]:
    def get_std_ids(tmp_session):
        # 课表查询之前，一定要访问，因此使用 session 模式
        response_inner = tmp_session.get(URLEnum.COURSE_TABLE_OF_STD_IDS.value)
        if is_save:
            save_html_to_file(response_inner.text, 'get_ids')
        stu_id = re.findall(r'\(form,"ids","(.*?)"\);', response_inner.text)[0]
        if stu_id is None:
            raise exceptions.SpiderParserException("页面上没找到 ids")
        else:
            return stu_id

    if not session:
        session = login(username, password)
    ids = get_std_ids(session)
    response = session.get(URLEnum.COURSE_TABLE.value, params={
        'ignoreHead': 1,
        'setting.kind': 'std',  # std/class
        'ids': ids,
        'semester.id': semester_id,
    })
    html_text = response.text
    if is_save:
        save_html_to_file(html_text, 'course-table')
    if '课表格式说明' in html_text:
        part_course_list = parser.parse_course_table_bottom(html_doc=etree.HTML(html_text))
        return parser.parse_course_table_body(html_text, course_dict_list=part_course_list)
    else:
        raise exceptions.SpiderParserException("[课表页]获取失败")


def get_grade(username: str, password: str, session: Session = None, is_save: bool = False) -> [schemas.Grade]:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.GRADE.value)
    if is_save:
        save_html_to_file(response.text, 'grade')
    if '学年学期' in response.text:
        return parser.parse_grade(html_doc=etree.HTML(response.text))
    elif '所有成绩尚未发布' in response.text:
        return []
    else:
        raise exceptions.SpiderParserException("[成绩查询页]请求失败")


def get_grade_table(username: str, password: str, session: Session = None, is_save: bool = False) -> [
    schemas.GradeTable]:
    # 备用：获取成绩表格
    if not session:
        session = login(username, password)
    response = session.post(URLEnum.GRADE_TABLE.value, params={'template': 'grade.origin'})
    if is_save:
        save_html_to_file(response.text, 'grade-table')
    if '个人成绩总表打印' in response.text:
        return parser.parse_grade_table(html_doc=etree.HTML(response.text))
    else:
        raise exceptions.SpiderParserException("[总成绩查询页]获取失败")


def get_exam(username: str, password: str, semester_id: int = constantsShared.current_semester_id,
             session: Session = None, is_save: bool = False) -> [schemas.Exam]:
    def get_exam_id(tmp_session, inner_semester_id, inner_is_save):
        # 课表查询之前，一定要访问，因此使用 session 模式
        response_inner = tmp_session.get(URLEnum.EXAM_OF_BATCH_ID.value, params={'semester.id': inner_semester_id})
        if inner_is_save:
            save_html_to_file(response_inner.text, 'exam-batch-id')
        batch_id = parse.search('examBatch.id={id:d}', response_inner.text)
        if batch_id is None:
            raise exceptions.SpiderParserException("考试学期ID获取失败")
        else:
            return batch_id.named['id']

    if not session:
        session = login(username, password)
    exam_batch_id = get_exam_id(session, semester_id, is_save)
    response = session.get(URLEnum.EXAM.value, params={'examBatch.id': exam_batch_id})
    if is_save:
        save_html_to_file(response.text, 'exam')
    if '课程序号' in response.text:
        return parser.parse_exam(html_doc=etree.HTML(response.text))
    else:
        raise exceptions.SpiderParserException("[考试安排页]获取失败")


def get_other_exam(username: str, password: str, session: Session = None, is_save: bool = False) -> [schemas.OtherExam]:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.OTHER_EXAM.value)
    if is_save:
        save_html_to_file(response.text, 'other-exam')
    if '资格考试' in response.text:
        return parser.parse_other_exam(html_doc=etree.HTML(response.text))
    else:
        raise exceptions.SpiderParserException("[资格考试页]获取失败")
