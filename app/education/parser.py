import re

from app import schemas
from app.education.utils import GetWeek
from app.exceptions import SpiderParserException
from app.schemas import ClassTableCourseSchedule, ClassTableCourse


def parse_stu_info(html_doc) -> dict:
    rows = html_doc.xpath('/html/body/div/div[2]/div[1]/table/tr')[1:-1]
    data_keys = [
        'username', 'name', 'photoURL', 'nickname', 'gender', 'grade', 'eduLength', 'project',
        'education', 'studentType', 'college', 'major', 'direction', 'enrollDate', 'graduateDate',
        'chiefCollege', 'studyType', 'membership', 'isInSchool', 'withCampus', 'withClass',
        'recordEffectDate', 'isOwnRecord', 'studentStatus', 'isWorking']
    try:
        data_values = [cell.text
                       for row in rows
                       for cell in row.xpath('./td[not(@class="title")]')]
        if len(data_keys) != len(data_values):
            raise SpiderParserException("个人信息页，数据解析缺失")
        data = dict(zip(data_keys, data_values))
        data[
            'photoURL'] = F"http://202.199.224.119:8080/eams/showSelfAvatar.action?user.name={data.get('username', 'None')}"
        return data
    except IndexError:
        raise SpiderParserException("个人信息页，数组越界")
    except AttributeError:
        raise SpiderParserException("个人信息页，结构不正常解析失败")


def parse_class_table_bottom(html_doc) -> list:
    rows = html_doc.xpath('//*[@id="tasklesson"]/div/table/tbody/tr')
    course_list = []
    try:
        for row in rows:
            cells = row.xpath('./td')
            row_data = ["".join(cell.xpath('string(.)').split()) for cell in cells[2:-2]]
            """['大数据开发技术', '3', 'H101750042048.01', '杨韬']"""
            single_course_dict = {
                'code': row_data[2],
                'name': row_data[0],
                'credit': row_data[1],
                'teacher': row_data[3],
            }
            course_list.append(ClassTableCourse(**single_course_dict))
            # 另一种解析 row_data = ["".join (cell.text.split ()) for cell in cells]
        return course_list
    except IndexError:
        raise SpiderParserException("课表页，底部数组越界")
    except AttributeError:
        raise SpiderParserException("课表页，底部解析失败")


def parse_class_table_body(html_text, course_dict_list: list) -> list:
    try:
        course_table_pattern = """activity = new TaskActivity\(actTeacherId\.join\(','\),actTeacherName\.join\(','\),"(.*?)",null,null,assistantName,"","","(.*?)"\);\s+index =(\d)\*unitCount\+(\d+);"""
        body_course_list = re.findall(course_table_pattern, html_text)
        """function TaskActivity(teacherId,teacherName,courseId,courseName,roomId,roomName,vaildWeeks,taskId,remark,assistantName,experiItemName,schGroupNo){"""
        for each in body_course_list:
            """each: ['信息系统分析与设计(H101730023056.01)', '4809', '静远楼239', '00111111111100000000000000000000000000000000000000000', 5, 1]"""
            course_data = each[0].replace('\"', '').split(',')
            course_data_code = re.findall('\((.*?)\)', course_data[0])[0]
            schedule = ClassTableCourseSchedule()
            schedule.room = each[2]
            schedule.weeks = GetWeek().marshal(each[3], 2, 1, 50)  # TODO 单 1-9 -> [1,3,5,7,9]
            schedule.weekday = int(each[-2]) + 1  # course_week
            schedule.index = int(each[-1]) + 1  # course_index
            [course.schedules.append(schedule) for course in course_dict_list if
             course_data_code == course.code]
        return course_dict_list
    except IndexError:
        return "课表体数组越界"
    except AttributeError:
        return "课表体解析错误，xpath 失败"


def parse_grades(html_doc) -> list:
    course_list: [schemas.Grade] = []
    score_table_rows = html_doc.xpath('/html/body/div[@class="grid"]/table/tbody/tr')
    try:
        for row in score_table_rows:
            cells = []
            for td in row:
                if td.text is not None:
                    cells.append(td.text.strip())
                else:
                    cells.append('')
            """['2017-2018 1', 'H271780001036', 'H271780001036.18', ' 军事理论 ', ' 专业必修 ', '1', '-- (正常)', '47 (正常)', '50 (正常)', '74 (正常)', '74', '1']"""
            course = schemas.Grade(code=cells[2])
            course.name = cells[3]
            course.credit = cells[5]
            course.grade = cells[-2]
            course.semester = cells[0]
            course.courseType = cells[4]

            course.usual = cells[8]
            course.midterm = cells[6]
            course.termEnd = cells[7]
            course.result = cells[9]
            course_list.append(course)
        return course_list
    except IndexError as e:
        # raise SpiderParserException("成绩详情页，数组越界" + traceback.extract_stack(e,limit=3)) TODO traceback
        raise SpiderParserException("成绩详情页，数组越界")
    except AttributeError as e:
        raise SpiderParserException("成绩详情页，结构解析失败")
