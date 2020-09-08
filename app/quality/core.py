import requests
from lxml import etree

from .parser import parse_report, parse_scholarship, parse_activity
from .urls import QualityExpansionURLEnum


def get_cookie(username: int, password: str):
    url = QualityExpansionURLEnum.LOGIN.value.value
    body_data = {
        'Tuserid': username,
        'Tpassword': password,
        'dllx': 'RadioButton2',
        '__EVENTVALIDATION': '',
        '__VIEWSTATE': '',
        'Button1': '',
    }

    response = requests.get(url)
    html_doc = etree.HTML(response.text)
    body_data['__EVENTVALIDATION'] = html_doc.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
    body_data['__VIEWSTATE'] = html_doc.xpath("//*[@id='__VIEWSTATE']/@value")[0]
    response = requests.post(url, data=body_data)
    if response.status_code == 500:
        raise Exception("用户名或密码错误")
    else:
        return response.request.headers.get('Cookie')


def get_report(cookie: str):
    url = QualityExpansionURLEnum.REPORT.value.value

    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if ' 您已经长时间没有操作' in response.text:
        raise Exception("登陆过期")

    parse_report(html_doc)


def get_scholarship(cookie: str, year):
    url = QualityExpansionURLEnum.SCHOLARSHIP.value.value

    body_data = {
        '__VIEWSTATE': '',
        '__EVENTVALIDATION': '',
        'Button1': ' 开始查询',
        'Dpdnf': year,  # 查询学年
    }

    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if ' 您已经长时间没有操作' in html_text:
        raise Exception("登陆过期")

    # 构造参数
    body_data['__EVENTVALIDATION'] = html_doc.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
    body_data['__VIEWSTATE'] = html_doc.xpath("//*[@id='__VIEWSTATE']/@value")[0]

    # 查询奖学金
    response = requests.post(url, headers={'Cookie': cookie}, data=body_data)
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if ' 您已经长时间没有操作' in html_text:
        raise Exception("登陆过期")
    parse_scholarship(html_doc)


def get_activity(url, cookie: str):
    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if ' 您已经长时间没有操作' in html_text:
        raise Exception("登陆过期")

    parse_activity(html_doc=html_doc)


def get_mind_activity(cookie: str):
    url = QualityExpansionURLEnum.MIND.value
    get_activity(url, cookie=cookie)


def get_competition_activity(cookie: str):
    url = QualityExpansionURLEnum.COMPETITION.value
    get_activity(url, cookie=cookie)


def get_social_activity(cookie: str):
    url = QualityExpansionURLEnum.SOCIAL.value
    get_activity(url, cookie=cookie)


def get_reading_activity(cookie: str):
    url = QualityExpansionURLEnum.READING.value
    get_activity(url, cookie=cookie)


def get_classJob_activity(cookie: str):
    url = QualityExpansionURLEnum.CLASSJOB.value
    get_activity(url, cookie=cookie)


def get_skill_activity(cookie: str):
    url = QualityExpansionURLEnum.SKILL.value
    get_activity(url, cookie=cookie)


def get_all_activity(cookie: str):
    get_mind_activity(cookie)
    get_competition_activity(cookie)
    get_social_activity(cookie)
    get_reading_activity(cookie)
    get_classJob_activity(cookie)
    get_skill_activity(cookie)


# test
# user_cookie = get_cookie(171003****, "***")
user_cookie = 'ASP.NET_SessionId=4a1gev1nuayhgadtziy3lkch'
get_report(user_cookie)
# get_all_activity(user_cookie)
# get_scholarship(user_cookie, year=2019)
# get_scholarship(user_cookie, year=2018)
# get_scholarship(user_cookie, year=2017)
# get_scholarship(user_cookie, year=2016)
