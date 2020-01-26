from lxml import etree

from spider.utils.UrlEnums import UrlEnums
from web.models import CET


def cet_get_html(session):
    url = UrlEnums.CET
    response = session.get(url)
    return etree.HTML(response.text)


def cet_parser(html_doc, user):
    try:
        CETs = html_doc.xpath('/html/body/table[2]')
        for each in CETs[1:]:
            level = each.xpath('td[1]')[0].text.strip()
            if level == "不报名":
                continue
            cet = CET.objects.get_or_create(level=level, username=user)[0]
            cet.date = each.xpath('td[2]')[0].text.strip()
            cet.score = each.xpath('td[3]')[0].text.strip()
            cet.save()
    except Exception as e:
        print(e)
        return False
    return True
