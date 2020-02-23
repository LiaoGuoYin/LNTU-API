from api.models import ClassCourse
from spider.utils.utils import string_strip


def classTable_parser(html_doc, user, semester_str):
    try:
        course_tr_elements = html_doc.xpath('/html/body/table[4]/tr')
        for course_row in course_tr_elements[1:]:
            course_td_elements = course_row.xpath('./td')
            # data0 = [td.xpath('string(.)').replace("\r\n", "").replace("  ", "").strip() for td in
            #            td_elements]
            data = [string_strip(td.xpath('string(.)')) for td in course_td_elements]
            course_id = data[0]
            course = ClassCourse.objects.get_or_create(username=user, semester=semester_str, course_id=course_id)[0]
            course.course_number = data[1]
            course.course_name = data[2]
            course.teacher = data[3]
            course.credit = data[4]
            course.course_properties = data[5]
            course.inspect_method = data[6]
            course.status = data[7]
            course.is_delay_exam = data[8]
            course.details = course_td_elements[9].xpath('string(.)').replace("\r\n", "").replace("  ", "").replace(
                "\n", "").strip()  # TODO
            # course.details = data[9]
            # course.comment = data[10]  # 空
            course.comment = data[11]
            course.save()
        return True
    except Exception as e:
        print(e)
        return False
