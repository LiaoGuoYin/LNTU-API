import hashlib
import re
import time

import requests
from lxml import etree
from requests import Session, ReadTimeout

from app.education.parser import parse_class_table_bottom, parse_class_table_body, parse_grade, parse_stu_info, \
    parse_grade_table
from app.education.urls import URLEnum
from app.education.utils import save_html_to_file
from app.exceptions import NetworkException, TokenException, AccessException, FormException, SpiderParserException


def check_education_online() -> bool:
    try:
        response = requests.head(URLEnum.LOGIN.value, timeout=(1, 3))
        if response.status_code == 200:
            return True
        else:
            raise ReadTimeout("教务在线爆炸")
    except ReadTimeout:
        raise NetworkException("3s 未响应，教务在线爆炸")
    except ConnectionError:
        raise NetworkException("连接过多，被拒绝")


def login(username: int, password: str) -> Session:
    check_education_online()
    session = Session()
    session.keep_alive = False
    response = session.get(URLEnum.LOGIN.value)
    token = re.findall(r"SHA1\('(.*?)'", response.text)[0]
    if token is None:
        raise SpiderParserException("页面上没找到 SHA1token")
    key = hashlib.sha1((token + password).encode('utf-8')).hexdigest()
    time.sleep(0.5)  # 延迟 0.5 秒防止被 ban
    response = session.post(URLEnum.LOGIN.value, data={'username': username, 'password': key})
    if '密码错误' in response.text:
        raise TokenException(F"{username} 用户名或密码错误")
    elif '请不要过快点击' in response.text:
        raise AccessException("页面请求过快")
    elif '账户不存在' in response.text:
        raise FormException(F"{username} 用户不存在")
    elif '您当前位置' in response.text:
        print(F"{username} Login success!")
        return session
    else:
        return session


def get_stu_info(username: int, password: str, session=None, is_save: bool = False):
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.STUDENT_INFO.value)
    if "学籍信息" in response.text:
        if is_save:
            save_html_to_file(response.text, "info")
        html_doc = etree.HTML(response.text)
        return parse_stu_info(html_doc)
    else:
        raise SpiderParserException("个人信息页请求失败")


def get_class_table(username: int, password: str, semesterId: int = 627, session: Session = None,
                    is_save: bool = False) -> list:
    # 默认学期 627
    def get_std_ids(session):
        # 课表查询之前，一定要访问，因此使用 session 模式
        response_inner = session.get(URLEnum.CLASS_TABLE_OF_STD_IDS)
        if is_save:
            save_html_to_file(response_inner.text, "get_ids")
        stu_id = re.findall(r'\(form,"ids","(.*?)"\);', response_inner.text)[1]
        if stu_id is None:
            raise SpiderParserException("页面上没找到 ids")
        else:
            return stu_id

    if not session:
        session = login(username, password)
    ids = get_std_ids(session)
    response = session.get(URLEnum.CLASS_TABLE.value, params={
        'ignoreHead': 1,
        'setting.kind': 'class',  # std/class
        'ids': ids,
        'semester.id': semesterId,
    })
    html_text = response.text
    if is_save:
        save_html_to_file(html_text, "class-table")
    if '课表格式说明' in html_text:
        part_course_list = parse_class_table_bottom(html_doc=etree.HTML(html_text))
        return parse_class_table_body(html_text, course_dict_list=part_course_list)
    else:
        raise SpiderParserException("课表页请求失败")


def get_grade(username: int, password: str, session: Session = None, semesterId: int = 626,
              is_save: bool = False) -> list:
    if not session:
        session = login(username, password)
    response = session.get(URLEnum.GRADE.value, params={'semesterId': semesterId})
    if is_save:
        save_html_to_file(response.text, "grade")
    if '学年学期' in response.text:
        return parse_grade(html_doc=etree.HTML(response.text))
    else:
        raise SpiderParserException("成绩查询页请求失败")


def get_grade_table(username: int, password: str, session: Session = None, is_save: bool = False) -> list:
    if not session:
        session = login(username, password)
    response = session.post(URLEnum.GRADE_TABLE.value, params={'template': 'grade.origin'})
    if is_save:
        save_html_to_file(response.text, "grade-table")
    if '个人成绩总表打印' in response.text:
        return parse_grade_table(html_doc=etree.HTML(response.text))
    else:
        raise SpiderParserException("总成绩查询页请求失败")
