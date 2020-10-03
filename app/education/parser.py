import parse

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
        return course_list
    except IndexError:
        raise SpiderParserException("课表页，底部数组越界")
    except AttributeError:
        raise SpiderParserException("课表页，底部解析失败")


def parse_course_table_body(html_text, course_dict_list: [schemas.CourseTable]) -> [schemas.CourseTable]:
    def decrypt_week(week: str) -> schemas.CourseTableSchedule:
        """"
            转换周为列表：
            单 1-9 -> [1, 3, 5, 7, 9]
            双 2-10 -> [2, 4, 6, 8, 10]
            2-15 -> [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        week: 00001111111100000000000000000000000000000000000000000
        """
        schedule = CourseTableSchedule()
        schedule.room = info_result.get('room')
        tmp_weeks = GetWeek().marshal(week, 2, 1, 50)
        if tmp_weeks.startswith('双') or tmp_weeks.startswith('单'):  # '单1-9' or '双2-10'
            for each in tmp_weeks.split(' '):  # '单1-9 双2-14'
                start_week, end_week = map(int, each[1:].split('-'))
                schedule.weeks.extend(list(range(start_week, end_week + 1, 2)))
        elif '-' in tmp_weeks:  # '2-15' or '1-12 14-17'
            for each in tmp_weeks.split(' '):  # '2-12 14-17'
                start_week, end_week = map(int, each.split('-'))
                schedule.weeks.extend(list(range(start_week, end_week + 1)))
        else:  # '10'
            schedule.weeks = [int(tmp_weeks)]
        return schedule

    try:
        course_list_pattern_str = "activity = new TaskActivity({});{}var teacher"
        body_course_list = parse.findall(course_list_pattern_str, html_text)
        for course in body_course_list:
            original_info, original_schedule = course  # 将课程基本信息和时间信息解包
            # 解析基本信息
            # js example: function TaskActivity(teacherId,teacherName,courseId,courseName,roomId,roomName,vaildWeeks,taskId,remark,assistantName,experiItemName,schGroupNo){"""
            info_pattern_str = '''actTeacherId.join(\',\'),actTeacherName.join(\',\'),"{}","{name}({code})","{room_id}","{room}","{encrypted_week}",null,null,assistantName,{course_content},"","{}"'''
            info_all_result = parse.parse(info_pattern_str, original_info)
            if not info_all_result:
                raise SpiderParserException("课表为空，解析失败")
            info_result = info_all_result.named

            # 解析课程时间
            schedule_pattern_str = 'index ={:d}*unitCount+{:d};'
            schedule_all_result = parse.findall(schedule_pattern_str, original_schedule)
            schedule_day_index_tuple_list = [tuple(map(lambda x: x + 1, each)) for each in schedule_all_result]
            # [(2, 3),(2, 4)] 周二第三、四小节

            schedule_list = []
            for (day, index) in schedule_day_index_tuple_list:
                schedule = decrypt_week(info_result.get('encrypted_week'))
                if index % 2 == 0:  # 抛弃偶数节课方便转换为大节课，TODO 可能有单节偶数小课的 bug
                    continue
                odd_index = index
                schedule.weekday = day
                schedule.index = odd_index - (odd_index // 2)  # 小节课转大节课（十节课转五节课）
                schedule_list.append(schedule)

            for i in schedule_list:
                [course.schedules.append(i) for course in course_dict_list if
                 info_result.get('code') == course.code]
        return course_dict_list
    except IndexError:
        return "课表体数组越界"
    except AttributeError:
        return "课表体解析错误，xpath 失败"


def parse_grade_table(html_doc) -> [schemas.GradeTable]:
    course_grade_list: [schemas.GradeTable] = []
    course_grade_table_rows = html_doc.xpath('/html/body/table[2]/tr')
    try:
        cells_element = []
        cells = []
        for row in course_grade_table_rows[1:]:
            cells_element.append(row[:4])
            if row[-1].text != '\xa0':
                # 处理一行多个成绩的情况
                cells_element.append(row[4:])
        for tr in cells_element:
            tmp_course_grade_info = []
            for td in tr:
                tmp_course_grade_info.append(td.text)
            course_grade_style = tr[2].xpath('./@style')
            # 重修、补考、正常 元素的样式不同:
            # 斜线为补考成绩: ['font-style:italic; ']
            # 下划线为重新学习成绩: ['text-decoration:underline; ']
            if len(course_grade_style) != 0:
                course_grade_style = course_grade_style[0]
                course_grade_style = schemas.GradeTable.CourseStatusEnum.reStudy if (
                        'underline' in course_grade_style) else schemas.GradeTable.CourseStatusEnum.makeUp
            else:
                course_grade_style = schemas.GradeTable.CourseStatusEnum.normal
            tmp_course_grade_info.append(course_grade_style)
            cells.append(tmp_course_grade_info)
        for each in cells:
            # each: ['数据结构与算法分析', '4', '95', '2018-2019(1)', '重修']
            course_grade_table = schemas.GradeTable(name=each[0])
            course_grade_table.credit = each[1]
            course_grade_table.result = each[2]
            course_grade_table.semester = each[3]
            course_grade_table.status = each[4]
            course_grade_list.append(course_grade_table)
        return course_grade_list
    except Exception as e:
        return e


def parse_grade_table_gpa(html_doc) -> str:  # TODO
    try:
        course_grade_table_tail_row_all_credit = html_doc.xpath('string(/html/body/table[3]/tr[1]/td[1])')
        course_grade_table_tail_row_gpa = html_doc.xpath('string(/html/body/table[3]/tr[1]/td[2])').strip()
        return course_grade_table_tail_row_gpa.split(":")[1]
    except Exception as e:
        return e


def parse_grade(html_doc) -> [schemas.CourseTable]:
    course_list: [schemas.CourseTable] = []
    score_table_rows = html_doc.xpath('/html/body/div[@class="grid"]/table/tbody/tr')
    try:
        for row in score_table_rows:
            cells = []
            for td in row:
                if td.text is not None:
                    cells.append(''.join(td.xpath('string(.)').split()))
                else:
                    cells.append('')
            # cells: ['2019-20202', 'H101730023056', 'H101730023056.01', '信息系统分析与设计', '专业必修', '3.5', '95', '94', '89', '93.3', '93.3', '4', '查卷申请']
            if len(cells) == 0:
                return []
            course = schemas.Grade(name=cells[3], code=cells[2])
            course.credit = cells[5]
            course.semester = cells[0]
            course.courseType = cells[4]
            course.usual = cells[8]
            course.midTerm = cells[6]
            course.endTerm = cells[7]
            course.result = cells[-3]  # 忽略总评成绩
            course.point = cells[-2]
            if '补考' in course.name:
                course.status = schemas.GradeTable.CourseStatusEnum.makeUp.value
                course.makeUpScore = cells[-6]
                course.makeUpScoreResult = cells[-5]
            elif '重学' in course.name:
                course.status = schemas.GradeTable.CourseStatusEnum.reStudy.value
            else:
                course.status = schemas.GradeTable.CourseStatusEnum.normal
            course_list.append(course)
        return course_list
    except IndexError as e:
        raise SpiderParserException(f"成绩详情页，数组越界: {e}")
    except AttributeError as e:
        raise SpiderParserException(f"成绩详情页，结构解析失败: {e}")
