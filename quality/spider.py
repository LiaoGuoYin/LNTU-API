import requests
from lxml import etree

from quality.parser import ExpansionParser
from quality.urls import QualityExpansionURL


def get_cookie(username: int, password: str):
    url = QualityExpansionURL.LOGIN
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
    response = requests.post(QualityExpansionURL.__len__(), data=body_data)
    if response.status_code == 500:
        raise Exception("用户名或密码错误")
    else:
        return response.request.headers.get('Cookie')


def get_report(cookie: str):
    url = QualityExpansionURL.REPORT

    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in response.text:
        raise Exception("登陆过期")

    ExpansionParser.parse_report(html_doc)


def get_scholarship(cookie: str, year):
    url = QualityExpansionURL.SCHOLARSHIP
    body_data = {
        '__VIEWSTATE': '',
        '__EVENTVALIDATION': '',
        'Button1': '开始查询',
        'Dpdnf': year,  # 查询学年
    }

    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in html_text:
        raise Exception("登陆过期")

    # 构造参数
    body_data['__EVENTVALIDATION'] = html_doc.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
    body_data['__VIEWSTATE'] = html_doc.xpath("//*[@id='__VIEWSTATE']/@value")[0]

    # 查询奖学金
    response = requests.post(url, headers={'Cookie': cookie}, data=body_data)
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in html_text:
        raise Exception("登陆过期")
    ExpansionParser.parse_scholarship(html_doc)


def get_activity(url, cookie: str):
    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in html_text:
        raise Exception("登陆过期")

    ExpansionParser.parse_activity(html_doc=html_doc)


def get_mind_activity(cookie: str):
    url = QualityExpansionURL.MIND
    get_activity(url, cookie=cookie)


def get_competition_activity(cookie: str):
    url = QualityExpansionURL.COMPETITION
    get_activity(url, cookie=cookie)


def get_social_activity(cookie: str):
    url = QualityExpansionURL.SOCIAL
    get_activity(url, cookie=cookie)


def get_reading_activity(cookie: str):
    url = QualityExpansionURL.READING
    get_activity(url, cookie=cookie)


def get_classJob_activity(cookie: str):
    url = QualityExpansionURL.CLASSJOB
    get_activity(url, cookie=cookie)


def get_skill_activity(cookie: str):
    url = QualityExpansionURL.SKILL
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
user_cookie = 'ASP.NET_SessionId=u1qbgwxxujtftg5bw3ynfdcs'
get_report(user_cookie)
get_all_activity(user_cookie)
get_scholarship(user_cookie, year=2019)
get_scholarship(user_cookie, year=2018)
get_scholarship(user_cookie, year=2017)
get_scholarship(user_cookie, year=2016)
