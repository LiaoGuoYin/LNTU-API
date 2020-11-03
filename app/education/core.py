import hashlib
import re
import time
from copy import deepcopy

import parse
import requests
from lxml import etree
from requests import Session

from app import schemas, exceptions
from app.education import parser
from app.education.urls import URLEnum
from app.education.utils import save_html_to_file
from app.exceptions import NetworkException, AccessException, FormException, SpiderParserException


def is_education_online() -> bool:
    try:
        response = requests.head(URLEnum.LOGIN.value, timeout=(1, 3))
        if response.status_code == 200:
            return True
        else:
            raise NetworkException("教务无响应，爆炸爆炸")
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, exceptions.NetworkException):
        return False


def login(username: int, password: str) -> Session:
    if not is_education_online():
        raise NetworkException("教务无响应，爆炸爆炸")
    requests.adapters.DEFAULT_RETRIES = 5
    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.111 Safari/537.36',
        'Connection': 'close',
    }
    session.keep_alive = False
    response = session.get(URLEnum.LOGIN.value)
    token = re.findall(r"SHA1\('(.*?)'", response.text)[0]
    if token is None:
        raise SpiderParserException("页面上没找到 SHA1token")
    key = hashlib.sha1((token + password).encode('utf-8')).hexdigest()
    time.sleep(0.5)  # 延迟 0.5 秒防止被 ban
    response = session.post(URLEnum.LOGIN.value, data={'username': username, 'password': key})
    if '密码错误' in response.text:
        raise FormException(F"{username} 用户名或密码错误")
    elif '请不要过快点击' in response.text:
        raise AccessException("页面请求过快")
    elif '账户不存在' in response.text:
        raise FormException(F"{username} 用户不存在")
    elif '超过人数上限' in response.text:
        raise FormException("超过人数上限，请稍后再试")
    elif '您当前位置' in response.text:
        return session
    else:
        raise AccessException("页面未知错误")


def get_stu_info(username: int, password: str, session=None, is_save: bool = False) -> schemas.UserInfo:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.STUDENT_INFO.value)
    if "学籍信息" in response.text:
        if is_save:
            save_html_to_file(response.text, 'info')
        html_doc = etree.HTML(response.text)
        return parser.parse_stu_info(html_doc)
    else:
        raise SpiderParserException("个人信息页请求失败")


def get_course_table(username: int, password: str, semester_id: int = 627, session: Session = None,
                     is_save: bool = False) -> [schemas.CourseTable]:
    def get_std_ids(tmp_session):
        # 课表查询之前，一定要访问，因此使用 session 模式
        response_inner = tmp_session.get(URLEnum.COURSE_TABLE_OF_STD_IDS.value)
        if is_save:
            save_html_to_file(response_inner.text, 'get_ids')
        stu_id = re.findall(r'\(form,"ids","(.*?)"\);', response_inner.text)[0]
        if stu_id is None:
            raise SpiderParserException("页面上没找到 ids")
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
        raise SpiderParserException("课表页请求失败")


def get_grade(username: int, password: str, session: Session = None, is_save: bool = False) -> [schemas.Grade]:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.GRADE.value)
    if is_save:
        save_html_to_file(response.text, 'grade')
    if '学年学期' in response.text:
        return parser.parse_grade(html_doc=etree.HTML(response.text))
    else:
        raise SpiderParserException("成绩查询页请求失败")


def get_grade_table(username: int, password: str, session: Session = None, is_save: bool = False) -> [
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
        raise SpiderParserException("解析总成绩查询页失败")


def get_exam(username: int, password: str, semester_id: str, session: Session = None, is_save: bool = False) -> [
    schemas.Exam]:
    def get_exam_id(tmp_session, semester_id, is_save):
        # 课表查询之前，一定要访问，因此使用 session 模式
        response_inner = tmp_session.get(URLEnum.EXAM_OF_BATCH_ID.value, params={'semester.id': semester_id})
        if is_save:
            save_html_to_file(response_inner.text, 'exam-batch-id')
        exam_batch_id = parse.search('examBatch.id={id:d}', response_inner.text)
        if exam_batch_id is None:
            raise SpiderParserException("获取考试学期id失败")
        else:
            return exam_batch_id.named['id']

    if not session:
        session = login(username, password)
    exam_batch_id = get_exam_id(session, semester_id, is_save)
    response = session.get(URLEnum.EXAM.value, params={'examBatch.id': exam_batch_id})
    if is_save:
        save_html_to_file(response.text, 'exam')
    if '课程序号' in response.text:
        return parser.parse_exam(html_doc=etree.HTML(response.text))
    else:
        raise SpiderParserException("解析考试安排页失败")


def calculate_gpa(course_list: [schemas.Grade], is_including_optional_course: str = '1') -> schemas.GPA:
    """GPA计算规则:
        "二级制: 合格(85),不合格(0)"
        "五级制: 优秀(95),良(85),中(75),及格(65),不及格(0)"
    补考和重修：同一门课程多次考核时，其绩点按平均值算。当至少一次绩点大于 1.0，且平均绩点低于 1.0 时，平均绩点按 1.0 计算。
    """
    course_list = deepcopy(course_list)
    gpa_result = schemas.GPA()
    rule_dict = {"合格": 85, "不合格": 0,
                 "优秀": 95, "良": 85, "中": 75, "及格": 65, "不及格": 0}
    for course in course_list:

        # 排除选修课
        if (is_including_optional_course == '0') and ('校级公选课' in course.courseType):
            continue

        # 分数等级置换
        course.result = rule_dict.get(course.result, course.result)
        if not course.result:
            continue

        # 计算GPA
        try:
            point = float(course.result)
            course.credit = float(course.credit)
        except ValueError:
            # 分数转换错误 TODO
            continue
        gpa_result.courseCount += 1
        gpa_result.creditTotal += course.credit
        gpa_result.scoreTotal += point * course.credit

        # 计算成绩绩点 GradePoint
        if 95 <= point <= 100:
            course_point = 4.5
        elif 90 <= point < 95:
            course_point = 4.0
        elif 85 <= point < 90:
            course_point = 3.5
        elif 80 <= point < 85:
            course_point = 3.0
        elif 75 <= point < 80:
            course_point = 2.5
        elif 70 <= point < 75:
            course_point = 2.0
        elif 65 <= point < 70:
            course_point = 1.5
        elif 60 <= point < 65:
            course_point = 1.0
        else:
            course_point = 0

        if course.status == schemas.GradeTable.CourseStatusEnum.makeUp:
            course_point /= 2
        elif course.status == schemas.GradeTable.CourseStatusEnum.reStudy:
            course_point /= 3
        else:
            pass
        final_course_point = 1 if (course_point <= 1) else course_point  # 重修多次导致单科成绩绩点 GradePoint <= 1.0
        # print(f'{course.name} \t {course.result}  \t {final_course_point}  \r {course.point}')
        gpa_result.gradePointTotal += final_course_point * course.credit

    if gpa_result.courseCount == 0:
        return gpa_result
    else:
        # 计算平均学分绩 GPA
        gpa_result.gradePointAverage = round(gpa_result.gradePointTotal / gpa_result.creditTotal, 4)  # 平均绩点
        gpa_result.weightedAverage = round(gpa_result.scoreTotal / gpa_result.creditTotal, 4)  # 加权平均分
        return gpa_result
