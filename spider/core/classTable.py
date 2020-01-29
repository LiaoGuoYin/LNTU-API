from lxml import etree

from spider.utils.UrlEnums import UrlEnums
from web.models import ClassCourse


def classTable_get_html(session, semester_data):
    url = UrlEnums.CLASS_TABLE
    response = session.get(url, params=semester_data)
    # with open("output0.html", 'w+') as fp:
    #     fp.write(response.text)
    #     print("ok HTML")
    return etree.HTML(response.text)


def classTable_parser(html_doc, user, semester_str):
    try:
        course_elements = html_doc.xpath('/html/body/table[4]/tr')
        for each in course_elements[1:]:  # 舍弃表头
            td_elements = each.xpath('td')  # 获取所有td
            course_id = td_elements[0].text
            course = ClassCourse.objects.get_or_create(username=user, semester=semester_str, course_id=course_id)[0]
            results = [td.xpath('string(.)').replace("\r\n", "").replace("  ", "").strip() for td in
                       td_elements]
            course.course_number = results[1]
            course.course_name = results[2]
            course.teacher = results[3]
            course.credit = results[4]
            course.course_properties = results[5]
            course.inspect_method = results[6]
            course.status = results[7]
            course.is_delay_exam = results[8]
            course.details = results[9]
            # course.comment = results[10]  # 空
            course.comment = results[11]
            course.save()
        return True
    except Exception as e:
        print(e.args)
        return False
