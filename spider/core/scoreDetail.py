from lxml import etree

from spider.utils.UrlEnums import UrlEnums


def detail_get_html(session, details_print_id):
    url = str(UrlEnums.SCORES_DETAIL) + str(details_print_id)  # 保留 id，以后应该也能看
    response = session.get(url)
    html_doc = etree.HTML(response.text)
    return html_doc


def detail_parser(html_doc, score):
    try:
        # TODO 判断网页内容是否本来就为空
        detail_element = html_doc.xpath('/html/body/center/table')[0]
        score.made_up_of = detail_element.xpath('tr[5]/td/p/b/text()')[0].strip()
        score.daily_score = detail_element.xpath('tr[7]/td[1]/b/text()')[0].strip()
        score.midterm_score = detail_element.xpath('tr[7]/td[2]/b/text()')[0].strip()
        score.exam_score = detail_element.xpath('tr[7]/td[3]/b/text()')[0].strip()
        score.final_score = detail_element.xpath('tr[7]/td[4]/b/text()')[0].strip()
        score.save()
        return True
    except Exception as e:
        print(e)
        return False
