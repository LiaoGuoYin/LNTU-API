from lxml import etree

from spider.utils.UrlEnums import UrlEnums
from web.models import ExamPlan


def examPlan_get_html(session):
    url = UrlEnums.EXAM_PLAN
    response = session.get(url)
    return etree.HTML(response.text)


def examPlan_parser(html_doc, user):
    try:
        elements = html_doc.xpath('/html/body/table[2]/tr[@class="infolist_common"]')
        for element in elements:
            date, time = element.xpath('td[2]/text()')[0].split()
            exam = ExamPlan.objects.get_or_create(username=user, date=date, time=time)[0]
            exam.name = element.xpath('td[1]/text()')[0]
            exam.room = element.xpath('td[3]/text()')[0]
            exam.save()
    except Exception as e:
        print(e)
        return False
    return True
