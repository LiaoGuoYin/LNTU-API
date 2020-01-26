from lxml import etree

from spider.utils.UrlEnums import UrlEnums
from web.models import Score


def score_get_html(session):
    url = UrlEnums.SCORE
    response = session.get(url)
    html = response.text.replace('<font color="#CC0000">', '').replace('</font>', '').replace(
        '<a target="_blank" href="', '').replace('">打印</a>', '')  # 破坏指定元素的结构，方便有效率地统一提取
    return etree.HTML(html)


def score_parser(html_doc, user):
    try:
        course_elements = html_doc.xpath('/html/body/table[2]/tr')
        for course in course_elements[1:]:  # 舍弃th
            course_id = course.xpath('td[1]')[0].text.strip()
            semester = course.xpath('td[10]')[0].text.strip()
            score = Score.objects.get_or_create(username=user, semester=semester, course_id=course_id)[0]
            score.name = course.xpath('td[2]')[0].text.strip()
            score.course_number = course.xpath('td[3]')[0].text.strip()
            score.scores = course.xpath('td[4]')[0].text.strip()  # 破坏1：挂科成绩和正常成绩标签不同
            score.credit = course.xpath('td[5]')[0].text.strip()
            score.inspect_method = course.xpath('td[6]')[0].text.strip()
            score.course_properties = course.xpath('td[7]')[0].text.split()[0]
            score.status = course.xpath('td[8]')[0].text.strip()
            score.exam_categories = course.xpath('td[9]')[0].text.strip()
            score.is_delay_exam = course.xpath('td[11]')[0].text.strip()
            score.details_print_id = course.xpath('td[12]')[0].text.strip()  # 破坏2：有的课程没有打印 id
            # if score.details_print_id:
            #     score.details_print_id = score.details_print_id.strip()
            score.save()
        return True
    except AttributeError as e:
        print("有课程失败")
        return False
    except Exception as e:
        print("其他未知错误")
        return False
