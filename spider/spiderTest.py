import os

import django
from lxml import etree
from utils.URLManager import UrlEnums

os.environ['DJANGO_SETTINGS_MODULE'] = 'LNTUME.settings'
django.setup()
from api.models import User, TeachingPlanCourse


def parser0(html_doc, user):
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
                # course.save()
        return True
    except Exception as e:
        print(e.with_traceback())
        return False


def parser1(html_doc, user):
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
                # print(course.__dict__)
                # course.save()
        return True
    except AttributeError as e:
        print(e.with_traceback())
        return False
    except Exception as e:
        print(e.with_traceback())
        return False


# response = requests.get(
#     "http://202.199.224.121:11180/newacademic/manager/teachresource/schedule/export_room_schedule_detail.jsp?weeks=9&buildingid1=4&buildingname=%E9%9D%99%E8%BF%9C%E6%A5%BC")
#
# with open('output0.html', 'w') as fp:
#     fp.write(response.text)
#     print("ok HTML")


with open("output.html", "r") as fp:
    html = fp.read()

html_doc = etree.HTML(html)
user = User.objects.first()
# parser1(html_doc, user)
#
# t0 = time.time()
# for i in range(30):
#     parser0(html_doc, user)
# print(F"0耗时：{time.time() - t0}")
#
# t0 = time.time()
# for i in range(30):
#     parser1(html_doc, user)
# print(F"1耗时：{time.time() - t0}")

print(UrlEnums.TEACHING_PLAN_IDS)
print(type(UrlEnums.TEACHING_PLAN_IDS))
