from lxml import etree

from spider.utils.URLManager import UrlEnums
from web.models import StudentInfo


def studentInfo_get_html(session):
    url = UrlEnums.STUDENT_INFO
    response = session.get(url)
    return etree.HTML(response.text)


def studentInfo_parser(html_doc, user):
    try:
        student = StudentInfo.objects.get_or_create(username=user)[0]
        table_element = html_doc.xpath('/html/body/center/table[1]')[0]
        student.username = table_element.xpath('./tr[1]/td[1]')[0].text.strip()
        student.name = table_element.xpath('./tr[2]/td[1]')[0].text.strip()
        student.native_from = table_element.xpath('./tr[1]/td[2]')[0].text.strip() + \
                              table_element.xpath('./tr[2]/td[2]')[0].text.strip()
        student.foreign_name = table_element.xpath('./tr[3]/td[1]')[0].text.strip()
        student.birthday = table_element.xpath('./tr[3]/td[2]')[0].text.strip()
        # student.card_kind = table_element.xpath('./tr[4]/td[1]')[0].text.strip()
        student.politics = table_element.xpath('./tr[4]/td[2]')[0].text.strip()
        student.ID_number = table_element.xpath('./tr[5]/td[1]')[0].text.strip()
        student.section = table_element.xpath('./tr[5]/td[2]')[0].text.strip()
        student.gender = table_element.xpath('./tr[6]/td[1]')[0].text.strip()
        student.nation = table_element.xpath('./tr[6]/td[2]')[0].text.strip()
        student.academy = table_element.xpath('./tr[7]/td[1]')[0].text.strip()
        student.major = table_element.xpath('./tr[7]/td[2]')[0].text.strip()
        student.class_number = table_element.xpath('./tr[8]/td[1]')[0].text.strip()
        student.category = table_element.xpath('./tr[8]/td[2]')[0].text.strip()
        student.province = table_element.xpath('./tr[9]/td[1]')[0].text.strip()
        student.score = table_element.xpath('./tr[9]/td[2]')[0].text.strip()
        # student.exam_number = table_element.xpath('./tr[10]/td[1]')[0].text.strip()
        student.graduate_from = table_element.xpath('./tr[10]/td[2]')[0].text.strip()
        student.foreign_language = table_element.xpath('./tr[11]/td[1]')[0].text.strip()
        # student.enroll_number = table_element.xpath('./tr[11]/td[2]')[0].text.strip()
        student.enroll_at = table_element.xpath('./tr[12]/td[1]')[0].text.strip()
        # student.enroll_method = table_element.xpath('./tr[12]/td[2]')[0].text.strip()
        student.graduate_at = table_element.xpath('./tr[13]/td[1]')[0].text.strip()
        student.train_method = table_element.xpath('./tr[13]/td[2]')[0].text.strip()
        student.address = table_element.xpath('./tr[14]/td[1]')[0].text.strip()
        # student.zip = table_element.xpath('./tr[14]/td[2]')[0].text.strip()
        student.phone = table_element.xpath('./tr[15]/td[1]')[0].text.strip()
        student.email = table_element.xpath('./tr[15]/td[2]')[0].text.strip()
        # student.roll_number = table_element.xpath('./tr[16]/td[1]')[0].text.strip()
        student.source_from = table_element.xpath('./tr[16]/td[2]')[0].text.strip()
        # student.graduate_to = table_element.xpath('./tr[17]/td[1]')[0].text.strip()
        # student.comment = table_element.xpath('./tr[18]/td[1]')[0].text
        student.img_url = "http://202.199.224.121:11180/newacademic/manager/studentinfo/photo/photo/{}.jpg".format(
            student.username)
        student.save()
        return True
    except Exception as e:
        print(e)
        return False
