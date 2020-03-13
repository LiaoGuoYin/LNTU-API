from core.exceptions import ParserException
from core.util import search_all, GetWeek


class LNTUParser:
    @staticmethod
    def parse_std_info(html_doc):
        rows = html_doc.xpath('/html/body/div/div[2]/div[1]/table/tr')[1:-1]
        data_keys = [
            'username', 'name', 'photoURL', 'nickname', 'gender', 'grade', 'duration', 'project',
            'diplomas', 'studentType', 'college', 'major', 'direction', 'entranceDate', 'graduateDate',
            'collegeAdmin', 'trainForm', 'isRecordingNow', 'isInSchool', 'campus', 'studentClass',
            'recordEffectDate', 'isOwnRecord', 'recordStatus', 'isWorking']
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
        course_list = []
        try:
            course_body_list = []
            for course in courses:
                course_data = course[0].replace('\"', '').split(',')
                course_data.append(course[-2] + 1)  # course_week
                course_data.append(course[-1] + 1)  # course_index
                course_body_list.append(course_data)
            """['206427(H101730023056.01)', '信息系统分析与设计(H101730023056.01)', '4809', '静远楼239(辽宁工大葫芦岛校区)', '00111111111100000000000000000000000000000000000000000', 'null', 'null', 'assistantName', '', '', 5, 1]"""
            for row in course_bottom_list:
                single_course_dict = {}
                single_course_dict['name'] = row[2]
                single_course_dict['credit'] = row[3]
                single_course_dict['code'] = row[4]
                single_course_dict['teacher'] = row[5]
                single_course_dict['schedules'] = []
                for each in course_body_list:
                    if each[1].startswith(row[2]):
                        single_course_dict.get('schedules').append({
                            'code': each[1].split('(')[1][:-1],
                            'room': each[3],  # room = each[3].split('(')[0]
                            'weeks': GetWeek().marshal(each[4], 2, 1, 50),
                            'days': each[-2],
                            'sections': each[-1],
                        })
                course_list.append(single_course_dict)
            return {"results:": course_list}
        except IndexError:
            return "课表体数组越界"
        except AttributeError:
            return "课表体解析错误，xpath 失败"

    @staticmethod
    def parse_all_GPAs(html_doc):
        gpa_table = html_doc.xpath('/html/body/table/tbody/tr')
        gpa_dict = {
            'GPA': '',
            'courseCounts': '',
            'courseCredits': '',
            'GPAs': [{
                'semester': '',
                'courseCount': '',
                'courseCredit': '',
                'annualGPA': '',
            }],
            'time': ''}
        gpa_dict.get('GPAs').clear()
        try:
            for row in gpa_table:
                cells = [cells.text.strip() for cells in row]
                cell_type = len(cells)
                """['2019-2020', '1', '13', '23.5', '3.77']"""
                if cell_type is 1:
                    # 学期类型：1是秋季，2是春季
                    gpa_dict['time'] = cells[0].split('统计时间:')[1]
                elif cell_type is 4:
                    gpa_dict['courseCounts'] = cells[1]
                    gpa_dict['courseCredits'] = cells[2]
                    gpa_dict['GPA'] = cells[3]
                elif cell_type is 5:
                    # semester_half = '秋' if cells[1] == '1' else '春'
                    gpa_dict['GPAs'].append({
                        'yearSection': cells[0],
                        'semester': cells[1],
                        'courseCount': cells[2],
                        'courseCredit': cells[3],
                        'semesterGPA': cells[4],
                    })
            return gpa_dict
        except IndexError:
            return "GPA 数组越界"
        except AttributeError:
            return "GPA 解析错误，xpath 失败"

    @staticmethod
    def parse_all_scores(html_doc):
        course_dict = {
            "courses": [{
                "name": "高等数学1",
                "courseCode": "H271780001036.18",
                "credit": '2.0',
                "grade": '99',
                "extraData": [
                    {
                        "key": "平时成绩",
                        "value": "99"
                    }, {
                        "key": "期中 (实验) 成绩",
                        "value": "96"
                    }, {
                        "key": "期末成绩",
                        "value": "93"
                    }, {
                        "key": "总评成绩",
                        "value": "99",
                    }, {
                        "key": "学期学年",
                        "value": "2017-2018 1",
                    }, {
                        "key": "课程类别",
                        "value": "专业必修"
                    }
                ]
            }]
        }
        course_dict['courses'].clear()  # 以上字典示例用，清空
        score_table_rows = html_doc.xpath('/html/body/div[@class="grid"]/table/tbody/tr')
        try:
            for row in score_table_rows:
                cells = [td.text.strip() for td in row]
                # print(cells)
                """['2017-2018 1', 'H271780001036', 'H271780001036.18', '军事理论', '专业必修', '1', '-- (正常)', '47 (正常)', '50 (正常)', '74 (正常)', '74', '1']"""
                course_dict['courses'].append({
                    'name': cells[3],
                    'courseCode': cells[2],
                    'credit': cells[5],
                    'grade': cells[-2],
                    'extraData': [{
                        "key": "平时成绩",
                        "value": cells[8]
                    }, {
                        "key": "期中 (实验) 成绩",
                        "value": cells[6]
                    }, {
                        "key": "期末成绩",
                        "value": cells[7]
                    }, {
                        "key": "总评成绩",
                        "value": cells[9],
                    }, {
                        "key": "学期学年",
                        "value": cells[0],
                    }, {
                        "key": "课程类别",
                        "value": cells[4]
                    }]
                })
            return course_dict
        except IndexError:
            return "成绩详情页数组越界"
        except AttributeError:
            return "成绩详情页结构，xpath 失败"
