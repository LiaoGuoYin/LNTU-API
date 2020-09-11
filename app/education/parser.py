import re

from app import schemas
from app.education.utils import GetWeek
from app.exceptions import SpiderParserException
from app.schemas import CourseTableSchedule, CourseTable


def parse_stu_info(html_doc) -> schemas.UserInfo:
    rows = html_doc.xpath('/html/body/div/div[2]/div[1]/table/tr')[1:-1]
    data_keys = ['username', 'name', 'photoUrl', 'nickname', 'gender', 'grade', 'educationLast', 'project',
                 'education',
                 'studentType', 'college', 'major', 'direction', 'enrollDate', 'graduateDate', 'chiefCollege',
                 'studyType', 'membership', 'isInSchool', 'campus', 'majorClass', 'effectAt', 'isInRecord',
                 'studentStatus', 'isWorking']
    try:
        data_values = [cell.text
                       for row in rows
                       for cell in row.xpath('./td[not(@class="title")]')]
        if len(data_keys) != len(data_values):
            raise SpiderParserException("个人信息页，数据解析缺失")
        data = dict(zip(data_keys, data_values))
        data[
            'photoUrl'] = F"http://202.199.224.119:8080/eams/showSelfAvatar.action?user.name={data.get('username', 'None')}"
        return schemas.UserInfo(**data)
    except IndexError:
        raise SpiderParserException("个人信息页，数组越界")
    except AttributeError:
        raise SpiderParserException("个人信息页，结构不正常解析失败")


def parse_course_table_bottom(html_doc) -> [schemas.CourseTable]:
    rows = html_doc.xpath('//*[@id="tasklesson"]/div/table/tbody/tr')
    course_list = []
    try:
        for row in rows:
            cells = row.xpath('./td')
            if not len(cells):
                # 处理课表为空的情况（可能是学期字段错误）
                return []
            row_data = ["".join(cell.xpath('string(.)').split()) for cell in cells[2:-2]]
            """['大数据开发技术', '3', 'H101750042048.01', '杨韬']"""
            single_course_dict = {
                'code': row_data[2],
                'name': row_data[0],
                'credit': row_data[1],
                'teacher': row_data[3],
            }
            course_list.append(CourseTable(**single_course_dict))
            # 另一种解析 row_data = ["".join (cell.text.split ()) for cell in cells]
        return course_list
    except IndexError:
        raise SpiderParserException("课表页，底部数组越界")
    except AttributeError:
        raise SpiderParserException("课表页，底部解析失败")


def parse_course_table_body(html_text, course_dict_list: [schemas.CourseTable]) -> [schemas.CourseTable]:
    try:
        course_table_pattern = r"""activity = new TaskActivity\(actTeacherId\.join\(','\),actTeacherName\.join\(','\),"(.*?)",null,null,assistantName,"","","(.*?)"\);\s+index =(\d)\*unitCount\+(\d+);"""
        body_course_list = re.findall(course_table_pattern, html_text)
        # function TaskActivity(teacherId,teacherName,courseId,courseName,roomId,roomName,vaildWeeks,taskId,remark,assistantName,experiItemName,schGroupNo){"""
        for each in body_course_list:
            # each example: ('206427(H101730023056.01)","信息系统分析与设计(H101730023056.01)","4809","静远楼239","00111111111100000000000000000000000000000000000000000', '1570829', '4', '0')"""
            course_data = each[0].replace('\"', '').split(',')
            course_data.extend(each[-2:])
            course_data_code = re.findall(r'\((.*?)\)', course_data[1])[0]
            schedule = CourseTableSchedule()
            # '静远楼313(JY313)' -> '静远楼313'
            schedule.room = course_data[3] if course_data[3].find('(') == -1 else course_data[3].split('(')[0]
            tmp_weeks = GetWeek().marshal(course_data[4], 2, 1, 50)
            """"
            转换周为列表：
            单 1-9 -> [1,3,5,7,9]
            双 2-10 -> [2,4,6,8,10]
            2-15 -> [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            """
            if tmp_weeks.startswith('双') or tmp_weeks.startswith('单'):
                start_week, end_week = map(int, tmp_weeks[1:].split('-'))
                schedule.weeks = list(range(start_week, end_week + 1, 2))
            else:
                start_week, end_week = map(int, tmp_weeks.split('-'))
                schedule.weeks = list(range(start_week, end_week + 1))
            schedule.weekday = int(course_data[5]) + 1  # course_week
            schedule.index = int(course_data[6]) + 1  # course_index
            [course.schedules.append(schedule) for course in course_dict_list if
             course_data_code == course.code]
        return course_dict_list
    except IndexError:
        return "课表体数组越界"
    except AttributeError:
        return "课表体解析错误，xpath 失败"


def parse_grade(html_doc) -> [schemas.Grade]:
    course_list: [schemas.Grade] = []
    score_table_rows = html_doc.xpath('/html/body/div[@class="grid"]/table/tbody/tr')
    try:
        for row in score_table_rows:
            cells = []
            for td in row:
                if td.text is not None:
                    cells.append(''.join(td.xpath('string(.)').split()))
                else:
                    cells.append('')
            # cells: ['2017-2018 1', 'H271780001036', 'H271780001036.18', ' 军事理论 ', ' 专业必修 ', '1', '-- (正常)', '47 (正常)', '50 (正常)', '74 (正常)', '74', '1']
            if len(cells) == 0:
                return []
            course = schemas.Grade(code=cells[2])
            course.name = cells[3]
            course.credit = cells[5]
            course.grade = cells[-2]
            course.semester = cells[0]
            course.courseType = cells[4]
            course.usual = cells[8]
            course.midterm = cells[6]
            course.termEnd = cells[7]
            course.score = cells[9]
            course_list.append(course)
        return course_list
    except IndexError as e:
        raise SpiderParserException(f"成绩详情页，数组越界: {e}")
    except AttributeError as e:
        raise SpiderParserException(f"成绩详情页，结构解析失败: {e}")


def parse_grade_table(html_doc) -> [schemas.GradeTable]:
    course_list: [schemas.GradeTable] = []
    score_table_rows = html_doc.xpath('/html/body/table[2]/tr')
    try:
        cells_element = []
        cells = []
        for row in score_table_rows[1:]:
            cells_element.append(row[:4])
            if row[-1].text != '\xa0':
                # 处理一行多个成绩的情况
                cells_element.append(row[4:])
        for tr in cells_element:
            tmp_course_info = []
            for td in tr:
                tmp_course_info.append(td.text)
            course_style = tr[2].xpath('./@style')
            # 重修、补考、正常 元素的样式不同:
            # 斜体为补考成绩: ['font-style:italic; ']
            # 下划线为重新学习成绩: ['text-decoration:underline; ']
            if len(course_style) != 0:
                course_style = course_style[0]
                course_style = schemas.GradeTable.CourseStatusEnum.reStudy if (
                        'underline' in course_style) else schemas.GradeTable.CourseStatusEnum.makeUp
            else:
                course_style = schemas.GradeTable.CourseStatusEnum.normal
            tmp_course_info.append(course_style)
            cells.append(tmp_course_info)
        for each in cells:
            # each: ['数据结构与算法分析', '4', '95', '2018-2019(1)', '重修']
            grade_table = schemas.GradeTable(name=each[0])
            grade_table.credit = each[1]
            grade_table.score = each[2]
            grade_table.semester = each[3]
            grade_table.status = each[4]
            course_list.append(grade_table)
        return course_list
    except Exception as e:
        return e


def calculate_gpa(grade_list) -> schemas.GPA:
    # TODO bug，重修有学分折半
    """GPA计算规则:
        "二级制: 合格(85),不合格(0)"
        "五级制: 优秀(95),良(85),中(75),及格(65),不及格(0)"
    """
    gpa_result = schemas.GPA()
    rule_dict = {"合格": 85, "不合格": 0,
                 "优秀": 95, "良": 85, "中": 75, "及格": 65, "不及格": 0}
    for grade in grade_list:
        # 分数等级置换
        # print(F"{grade.name}：{grade.score} ", end='')
        grade.score = rule_dict.get(grade.score, grade.score)
        if grade.score:
            pass
            # print(F" -> {grade.score}")
        else:
            # print(F" None -> {grade.score}(异常)")
            continue

        # 计算GPA
        point = float(grade.score)
        grade.credit = float(grade.credit)
        gpa_result.courseCount += 1
        gpa_result.creditTotal += grade.credit
        gpa_result.scoreTotal += point * grade.credit

        # 计算学分绩
        if 95 <= point <= 100:
            gpa_result.gradePointTotal += grade.credit * 4.5
        elif 90 <= point < 95:
            gpa_result.gradePointTotal += grade.credit * 4.0
        elif 85 <= point < 90:
            gpa_result.gradePointTotal += grade.credit * 3.5
        elif 80 <= point < 85:
            gpa_result.gradePointTotal += grade.credit * 3.0
        elif 75 <= point < 80:
            gpa_result.gradePointTotal += grade.credit * 2.5
        elif 70 <= point < 75:
            gpa_result.gradePointTotal += grade.credit * 2.0
        elif 65 <= point < 70:
            gpa_result.gradePointTotal += grade.credit * 1.5
        elif 60 <= point < 65:
            gpa_result.gradePointTotal += grade.credit * 1.0
        else:
            gpa_result.gradePointTotal += 0

    if gpa_result.courseCount == 0:
        return gpa_result

    # 计算平均学分绩 GPA
    gpa_result.gradePointAverage = round(gpa_result.gradePointTotal / gpa_result.creditTotal, 4)  # 绩点
    gpa_result.weightedAverage = round(gpa_result.scoreTotal / gpa_result.creditTotal, 4)  # 加权平均分
    return gpa_result
