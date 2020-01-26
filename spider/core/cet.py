from lxml import etree

from spider.utils.UrlEnums import UrlEnums
from web.models import CET


def cet_get_html(session):
    url = UrlEnums.CET
    response = session.get(url)
    return etree.HTML(response.text)


def cet_parser(html_doc, user):
    try:
        cet_elements = html_doc.xpath('/html/body/table[2]/tr')
        for each in cet_elements[1:]:
            level = each.xpath('td[1]')[0].text.strip()
            if level == "不报名":
                continue
            date = each.xpath('td[2]')[0].text.strip()
            cet = CET.objects.get_or_create(date=date, username=user)[0]
            cet.level = level
            cet.score = each.xpath('td[3]')[0].text.strip()
            cet.save()
        return True
    except Exception as e:
        print(e.with_traceback)
        return False
