from lxml import etree

from spider.utils.UrlEnums import UrlEnums
from web.models import ExamPlan


def examPlan_get_html(session):
    url = UrlEnums.EXAM_PLAN
    response = session.get(url)
    return etree.HTML(response.text)


def examPlan_parser(html_doc, user):
    try:
        exan_elements = html_doc.xpath('/html/body/table[2]/tr')
        for each in exan_elements[1:]:
            date, time = each.xpath('td[2]')[0].text.split()
            exam = ExamPlan.objects.get_or_create(username=user, date=date, time=time)[0]
            exam.name = each.xpath('td[1]')[0].text.strip()
            exam.room = each.xpath('td[3]')[0].text.strip()
            exam.save()
        return True
    except Exception as e:
        print(e)
        return False
