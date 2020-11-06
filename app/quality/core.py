import requests
from lxml import etree

from app import exceptions, schemas
from app.education.utils import save_html_to_file
from app.quality.parser import parse_report, parse_activity, parse_scholarship
from app.quality.urls import QualityExpansionURLEnum


def is_quality_online() -> bool:
    try:
        response = requests.head(QualityExpansionURLEnum.LOGIN.value, timeout=(1, 3))
        if response.status_code == 200:
            return True
        else:
            raise exceptions.NetworkException("素拓网无响应，爆炸爆炸")
    except (requests.exceptions.RequestException, requests.exceptions.RequestException, exceptions.NetworkException):
        return False


def get_cookie(username: str, password: str) -> str:
    if not is_quality_online():
        raise exceptions.NetworkException("素拓网无响应，爆炸爆炸")
    url = QualityExpansionURLEnum.LOGIN.value
    response = requests.get(url)
    html_doc = etree.HTML(response.text)
    body_data = {
        'Tuserid': username,
        'Tpassword': password,
        'dllx': 'RadioButton2',
        '__EVENTVALIDATION': html_doc.xpath("//*[@id='__EVENTVALIDATION']/@value")[0],
        '__VIEWSTATE': html_doc.xpath("//*[@id='__VIEWSTATE']/@value")[0],
        'Button1': '',
    }
    response = requests.post(url, data=body_data)
    if response.status_code == 500:
        raise exceptions.FormException(f'{username} 用户名或密码错误')
    else:
        return response.request.headers.get('Cookie')


def get_report(cookie: str, is_save=False) -> [schemas.QualityActivity]:
    url = QualityExpansionURLEnum.REPORT.value
    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in response.text:
        raise exceptions.AccessException('登陆过期')
    else:
        if is_save:
            save_html_to_file(html_text, 'quality-report')
        return parse_report(html_doc)


def get_scholarship(cookie: str, year) -> [schemas.QualityScholarship]:
    url = QualityExpansionURLEnum.SCHOLARSHIP.value

    # 构造参数
    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in html_text:
        raise Exception('登陆过期')
    body_data = {
        'Dpdnf': year,
        'Button1': ' 开始查询',
        '__VIEWSTATE': html_doc.xpath("//*[@id='__VIEWSTATE']/@value")[0],
        '__EVENTVALIDATION': html_doc.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
    }

    # 查询奖学金
    response = requests.post(url, headers={'Cookie': cookie}, data=body_data)
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in html_text:
        raise exceptions.AccessException('登陆过期')
    else:
        return parse_scholarship(html_doc)


def get_single_activity(url, activity_type: str, cookie: str, is_save=False) -> list:
    response = requests.get(url, headers={'Cookie': cookie})
    html_text = response.text
    html_doc = etree.HTML(html_text)
    if '您已经长时间没有操作' in html_text:
        raise exceptions.AccessException('登陆过期')
    else:
        if is_save:
            save_html_to_file(html_text, 'quality-activity')
        return parse_activity(html_doc=html_doc, activity_type=activity_type)


def get_all_activity(cookie: str) -> dict:
    activity_dict = QualityExpansionURLEnum.get_activity()
    for item, url in activity_dict.items():
        # 把字典值中的 URL 换成爬虫结果
        activity_dict[item] = get_single_activity(url.value, cookie=cookie, activity_type=item)
    return activity_dict


if __name__ == '__main__':
    # user_cookie = get_cookie(1710030215, "****")
    user_cookie = 'ASP.NET_SessionId=qjbzzfzyb4v1jnhckoia3'
    print(get_report(user_cookie))
    # get_scholarship(user_cookie, year=2019)
    # get_scholarship(user_cookie, year=2018)
    # get_scholarship(user_cookie, year=2017)
    # get_scholarship(user_cookie, year=2016)
    # get_all_activity(user_cookie)
