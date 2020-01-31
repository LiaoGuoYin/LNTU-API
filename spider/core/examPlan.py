from utils.utils import string_strip
from web.models import ExamPlan


def examPlan_parser(html_doc, user):
    try:
        exam_tr_elements = html_doc.xpath('/html/body/table[2]/tr')
        for exam_row in exam_tr_elements[1:]:
            exam_td_elements = exam_row.xpath('./td')
            data = [string_strip(td.text) for td in exam_td_elements]
            date, time = exam_td_elements[1].text.split()
            exam = ExamPlan.objects.get_or_create(username=user, date=date, time=time)[0]
            exam.name = data[0]
            exam.room = data[2]
            exam.save()
        return True
    except Exception as e:
        print(e)
        return False
