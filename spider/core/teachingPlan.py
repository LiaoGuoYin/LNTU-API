from lxml import etree

from spider.utils.UrlEnums import UrlEnums
from web.models import TeachingPlanCourse


def teachingPlan_get_uri(session):
    """Get studentId and classId"""
    uri = None
    try:
        url = str(UrlEnums.TEACHING_PLAN) + "studyschedule.jsdo"
        response = session.get(url)
        html_doc = etree.HTML(response.text)
        uri_element = html_doc.xpath('/html/body/center/table[5]/form/tr/td/input')
        uri = uri_element[0].get('onclick').split(r"'")[1]
    except Exception as e:
        print(e.with_traceback)
    return uri


def teachingPlan_get_html(session, uri):
    """Get the teaching plan HTML with uri in studentId and classId"""
    url = str(UrlEnums.TEACHING_PLAN) + uri
    response = session.get(url)
    return etree.HTML(response.text)


def teachingPlan_parser(html_doc, user):
    try:
        semester_elements = html_doc.xpath('/html/body/table[2]/tr/td/table[@class="infolist_hr"]')
        for semester_index, element in enumerate(semester_elements[1:], start=1):  # 舍弃第一个table
            planning_courses = element.xpath('tr')
            for each in planning_courses[1:]:  # 舍弃表头
                course_id = each.xpath('td[1]')[0].text.strip()
                course = TeachingPlanCourse.objects.get_or_create(username=user, semester=semester_index,
                                                                  course_id=course_id)[0]
                course.course_name = each.xpath('td[2]')[0].text.strip()
                course.inspect_method = each.xpath('td[3]')[0].text.strip()
                course.credit = each.xpath('td[4]')[0].text.strip()
                course.period = each.xpath('td[5]')[0].text.strip()
                course.course_type = each.xpath('td[6]')[0].text.strip()
                course.course_group = each.xpath('td[7]')[0].text.strip()
                course.course_properties = each.xpath('td[8]')[0].text.strip()
                course.save()
    except Exception as e:
        print(e.with_traceback())
        return False
    return True
