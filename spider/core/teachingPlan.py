from lxml import etree

from api.models import TeachingPlanCourse
from spider.utils.URLManager import UrlEnums


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
        print(e)
    return uri


def teachingPlan_get_html(session, uri):
    """Get the teaching plan HTML with uri in studentId and classId"""
    url = str(UrlEnums.TEACHING_PLAN) + uri
    response = session.get(url)
    return etree.HTML(response.text)


def teachingPlan_parser(html_doc, user):
    try:
        semester_elements = html_doc.xpath('/html/body/table[2]/tr/td/table[@class="infolist_hr"]')
        for semester_index, semester in enumerate(semester_elements[1:], start=1):  # 舍弃第一个table
            course_tr_elements = semester.xpath('./tr')
            for course_row in course_tr_elements[1:]:  # 舍弃表头
                course_td_elements = course_row.xpath('./td')
                data = [td.text for td in course_td_elements]
                course_id = data[0]
                course = TeachingPlanCourse.objects.get_or_create(username=user, semester=semester_index,
                                                                  course_id=course_id)[0]
                course.course_name = data[1]
                course.inspect_method = data[2]
                course.credit = data[3]
                course.period = data[4]
                course.course_type = data[5]
                course.course_group = data[6]
                course.course_properties = data[7]
                course.save()
        return True
    except Exception as e:
        print(e)
        return False
