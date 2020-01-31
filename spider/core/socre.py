from utils.utils import string_strip
from web.models import Score


def score_parser(html_doc, user):
    try:
        course_tr_elements = html_doc.xpath('/html/body/table[2]/tr')
        for course_row in course_tr_elements[1:]:
            course_td_elments = course_row.xpath('./td')
            data = [string_strip(td.text) for td in course_td_elments]
            course_id = data[0]
            semester = data[9]
            score = Score.objects.get_or_create(username=user, semester=semester, course_id=course_id)[0]
            score.name = data[1]
            score.course_number = data[2]
            score.scores = data[3]  # 破坏1：挂科成绩和正常成绩标签不同
            score.credit = data[4]
            score.inspect_method = data[5]
            score.course_properties = data[6]
            score.status = data[7]
            score.exam_categories = data[8]
            score.semester = data[9]
            score.is_delay_exam = data[10]
            score.details_print_id = data[11]  # 破坏2：有的课程没有打印 id
            score.save()
        return True
    except AttributeError as e:
        print(F"有课程失败: {e}")
        return False
    except Exception as e:
        print(F"其他未知错误: {e}")
        return False
