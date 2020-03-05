from core.exceptions import ParserException
from core.util import GetWeek, Logger, search_all


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
        data_dict = {}
        for row in rows:
            cells = row.xpath('./td')
            try:
                """['2', 'H101730023056', '信息系统分析与设计', '3.5', '', '', '杨彤骥', '', '', '', '']"""
                row_data = ["".join(cell.xpath('string(.)').split()) for cell in cells]
                # cid = row_data[1]
                name = row_data[2]
                credit = row_data[3]
                cid = row_data[4]
                teacher = row_data[5]
                data_dict.update({
                    cid: {
                        'name': name,
                        'teacher': teacher,
                        'credit': credit,
                        'timeRoom': [],
                    }
                })
                # 另一种解析
                # row_data = ["".join(cell.text.split()) for cell in cells]
                # print(row_data)
                # print(data_dict)
                return data_dict
            except IndexError:
                Logger().e(tag="parser_class_table_bottom", content="解析课表底部失败，数据越界")
                return "课表底部数组越界"
            except AttributeError:
                return "课表底部解析错误，xpath 失败"

    @staticmethod
    def parse_class_table_body(html_text, all_course_dict):
        course_table_template = "new TaskActivity(actTeacherId.join(','),actTeacherName.join(','),{});"
        courses = search_all(course_table_template, html_text)
        print(len(courses))
        """index = 4*unitCount+0;"""
        # 可能有不配对的风险
        # column = search_all(u"index ={:d}*unitCount+{:d};", html_text)
        # row = search_all("index =unitCount+{}", html_text)[1:]
        # print(column)
        # section_template = 'var teachers = [{}];{}table0.activities[index][table0.activities[index].length]=activity;'
        # sections = search_all(section_template, html_text)
        # print([print(each) for each in sections])
        # print(row)
        try:
            data_lists = [course[0].replace('\"', '').split(',') for course in courses]
            # print(list(courses))
            for each in data_lists:
                id = each[1].split('(')[1][:-1]
                room = each[3]
                time = GetWeek().marshal(each[4], 2, 1, 50)
                timeRoom = F"{time} {room}"
                course_ori = all_course_dict.get(id)
                course_ori.get('timeRoom').append(timeRoom)
            return all_course_dict
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
                'averageGPA': '',
            }],
            'time': ''}
        gpa_dict.get('GPAs').clear()
        for row in gpa_table:
            try:
                cells = [cells.text.strip() for cells in row]
                cell_type = len(cells)
                # print(cells)
                """['2019-2020', '1', '13', '23.5', '3.77']"""
                if cell_type is 1:
                    # 学期类型：1是秋季，2是春季
                    gpa_dict['time'] = cells[0].split('统计时间:')[1]
                elif cell_type is 4:
                    gpa_dict['courseCounts'] = cells[1]
                    gpa_dict['courseCredits'] = cells[2]
                    gpa_dict['GPA'] = cells[3]
                elif cell_type is 5:
                    print(cells[1])
                    # semester_half = '秋' if cells[1] == '1' else '春'
                    gpa_dict['GPAs'].append({
                        'semester': F"{cells[0]}学年第{cells[1]}学期",
                        'courseCount': cells[2],
                        'courseCredit': cells[3],
                        'averageGPA': cells[4],
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
        for row in score_table_rows:
            try:
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
                # print(cells)
                return course_dict
            except IndexError:
                return "成绩详情页数组越界"
            except AttributeError:
                return "成绩详情页结构，xpath 失败"
