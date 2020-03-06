import hashlib
import time

import requests
from lxml import etree
from requests import Session

from core.exceptions import NetworkException, SpiderException, ParserException
from core.parser import LNTUParser
from core.urls import URLEnums
from core.util import search_all


def test_network():
    response = requests.head(URLEnums.LOGIN, timeout=(1, 3))
    if response.status_code != 200:
        raise NetworkException("3s 未响应，教务在线爆炸")


def log_in(username, password):
    test_network()
    session = Session()
    response = session.get(URLEnums.LOGIN)
    token = search_all("form['password'].value = CryptoJS.SHA1('{}' + form['password'].value);", response.text)[0][0]
    if token is None:
        raise ParserException("页面上没找到 SHA1token")
    key = hashlib.sha1((token + password).encode('utf-8')).hexdigest()
    data = {'username': username, 'password': key}
    time.sleep(0.5)
    response = session.post(URLEnums.LOGIN, data=data)
    if '密码错误' in response.text:
        raise SpiderException(F"{username} 用户名或密码错误")
    elif '请不要过快点击' in response.text:
        raise SpiderException("页面请求过快")
    elif '您当前位置' in response.text:
        print(F"{username} Login success!")
        return session
    elif '账户不存在' in response.text:
        raise SpiderException(F"{username} 用户不存在")
    else:
        raise SpiderException("登陆页飞了")


def get_std_info(username, password, session=None):
    if not session:
        session = log_in(username, password)
    response = session.get(URLEnums.STUDENT_INFO)
    if "学籍信息" in response.text:
        # save_html(response.text)
        html_doc = etree.HTML(response.text)
        results = LNTUParser.parse_std_info(html_doc)
        return results
    else:
        raise SpiderException("个人信息页请求失败")


def get_std_ids(session):
    """课表查询之前，一定要访问，因此只支持 session 模式"""
    response = session.get(URLEnums.CLASS_TABLE_OF_STD_IDS)
    stu_id = search_all('(form,"ids","{}");', html=response.text)[0][0]
    if stu_id is None:
        raise ParserException("页面上没找到 STD_ids")
    else:
        return stu_id


def get_class_table(username, password, semester=626, session=None):
    """默认学期 626"""
    if not session:
        session = log_in(username, password)
    """获取课表之前必须 get_std_id() """
    ids = get_std_ids(session)
    data = {
        'ignoreHead': 1,
        'startWeek': 1,
        'setting.kind': 'std',
        'ids': ids,
        'semester.id': semester,
    }
    response = session.post(URLEnums.CLASS_TABLE, data=data)
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '' in html_text:
        # save_html(html_text)
        all_course_dict = LNTUParser.parse_class_table_bottom(html_doc)
        results = LNTUParser.parse_class_table_body(html_text=html_text, all_course_dict=all_course_dict)
        return results
    else:
        raise SpiderException("成绩查询页请求失败")


def get_all_scores(username, password, session=None):
    if not session:
        session = log_in(username, password)
    response = session.post(URLEnums.ALL_SCORES)
    if "学年学期" in response.text:
        html_doc = etree.HTML(response.text)
        results = LNTUParser.parse_all_scores(html_doc=html_doc)
        return results
    else:
        raise SpiderException("成绩查询页请求失败")


def get_all_GPAs(username, password, session=None):
    if not session:
        session = log_in(username, password)
    response = session.post(URLEnums.ALL_SCORES)
    if "学年学期" in response.text:
        html_doc = etree.HTML(response.text)
        results = LNTUParser.parse_all_GPAs(html_doc=html_doc)
        return results
    else:
        raise SpiderException("GPA 查询页请求失败")
