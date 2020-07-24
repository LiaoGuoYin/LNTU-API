import traceback

from core.exceptions import ParserException
from core.util import search_all, GetWeek
from modelset import schemas
from modelset.schemas import ClassTable, ClassTableSchedule, GPA, semesterGPA


class LNTUParser:
    @staticmethod
    def parse_std_info(html_doc):
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
                raise ParserException("个人信息页数据解析缺失")
            data = dict(zip(data_keys, data_values))
            data[
                'photoURL'] = F"http://202.199.224.119:8080/eams/showSelfAvatar.action?user.name={data.get('username', 'None')}"
            return data
        except IndexError:
            return "信息页数组越界"
        except AttributeError:
            return "信息页结构不正常，xpath 解析失败"

    @staticmethod
    def parse_class_table_bottom(html_doc):
        rows = html_doc.xpath('//*[@id="tasklesson"]/div/table/tbody/tr')
        data_list = []
        try:
            for row in rows:
                cells = row.xpath('./td')
                """['2', 'H101730023056', '信息系统分析与设计', '3.5', '', '', '杨彤骥', '', '', '', '']"""
                row_data = ["".join(cell.xpath('string(.)').split()) for cell in cells]
                data_list.append(row_data)
                # 另一种解析 row_data = ["".join(cell.text.split()) for cell in cells]
            return data_list
        except IndexError:
            return "课表底部数组越界"
        except AttributeError:
            return "课表底部解析错误，xpath 失败"

    @staticmethod
    def parse_class_table_body(html_text, course_bottom_list):
        course_table_template = "new TaskActivity(actTeacherId.join(','),actTeacherName.join(','),{});{}index ={:d}*unitCount+{:d};"
        courses = search_all(course_table_template, html_text)
        """<Result ('"206427(H101730023056.01)","信息系统分析与设计(H101730023056.01)","4809","静远楼239(辽宁工大葫芦岛校区)","00111111111100000000000000000000000000000000000000000",null,null,assistantName,"",""', '\n\t\t\t', 4, 0) {}>"""
        """function TaskActivity(teacherId,teacherName,courseId,courseName,roomId,roomName,vaildWeeks,taskId,remark,assistantName,experiItemName,schGroupNo){"""
        # TODO performance optimize
        classTables: [ClassTable] = []
        try:
            course_body_list = []
            for course in courses:
                course_data = course[0].replace('\"', '').split(',')
                course_data.append(course[-2] + 1)  # course_week
                course_data.append(course[-1] + 1)  # course_index
                course_body_list.append(course_data)
            """['206427(H101730023056.01)', '信息系统分析与设计(H101730023056.01)', '4809', '静远楼239(辽宁工大葫芦岛校区)', '00111111111100000000000000000000000000000000000000000', 'null', 'null', 'assistantName', '', '', 5, 1]"""
            for row in course_bottom_list:
                code = row[4]
                course = ClassTable(code=code)
                course.name = row[2]
                course.credit = row[3]
                course.teacher = row[5]
                for each in course_body_list:
                    if each[1].startswith(row[2]):  # 对比字段合并
                        code = each[1].split('(')[1][:-1]
                        schedule = ClassTableSchedule(code=code)
                        schedule.room = each[3],  # room = each[3].split('(')[0]
                        schedule.weeks = GetWeek().marshal(each[4], 2, 1, 50)  # TODO 单1-9 -> [1,3,5,7,9]
                        schedule.weekday = each[-2]
                        schedule.index = each[-1]
                        course.schedule.append(schedule)
                classTables.append(course)
            return classTables
        except IndexError:
            return "课表体数组越界"
        except AttributeError:
            return "课表体解析错误，xpath 失败"

    @staticmethod
    def parse_all_GPAs(html_doc):
        gpa_table = html_doc.xpath('/html/body/table/tbody/tr')
        try:
            gpa = GPA(GPA="-1")  # 初始化
            for row in gpa_table:
                cells = [cells.text.strip() for cells in row]
                row_type = len(cells)  # 判断表头表身表尾
                if row_type == 1:
                    # 表尾元素是统计时间
                    gpa.effectiveTime = cells[0].split('统计时间:')[1]
                elif row_type == 4:
                    # 表头是总体信息
                    gpa.counts = cells[1]
                    gpa.credits = cells[2]
                    gpa.GPA = cells[3]
                elif row_type == 5:
                    # 表身是学期行
                    yearSection = cells[0]
                    singleGPA = semesterGPA(yearSection=yearSection)
                    singleGPA.semester = '秋' if cells[1] == '1' else '春'
                    singleGPA.count = cells[2]
                    singleGPA.credit = cells[3]
                    singleGPA.semesterGPA = cells[4]
                    gpa.GPAs.append(singleGPA)
            return gpa
        except IndexError:
            return "GPA 数组越界"
        except AttributeError:
            return "GPA 解析错误，xpath 失败"

    @staticmethod
    def parse_grades(html_doc):
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
                """['2017-2018 1', 'H271780001036', 'H271780001036.18', '军事理论', '专业必修', '1', '-- (正常)', '47 (正常)', '50 (正常)', '74 (正常)', '74', '1']"""
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
            traceback.format_exc()
            return "成绩详情页数组越界"
        except AttributeError as e:
            return "成绩详情页结构，xpath 失败"
