import traceback

from util import GetWeek, Logger, search_all


class LNTUParser:
    @staticmethod
    def parse_class_table_bottom(html_doc):
        try:
            xpath_of_table_bottom = '//*[@id="tasklesson"]/div/table/tbody/tr'
            rows = html_doc.xpath(xpath_of_table_bottom)
            data_dict = {}
            for row in rows:
                cells = row.xpath('./td')
                row_data = ["".join(cell.xpath('string(.)').split()) for cell in cells]
                # 另一种解析
                # row_data = ["".join(cell.text.split()) for cell in cells]
                # print(row_data)
                """['2', 'H101730023056', '信息系统分析与设计', '3.5', '', '', '杨彤骥', '', '', '', '']"""
                name = row_data[2]
                credit = row_data[3]
                # cid = row_data[1]
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
                # print(data_dict)
            return data_dict
        except IndexError as e:
            traceback.format_exc(e)
            Logger().e(tag="parser_class_table_bottom", content="课表底部，详细信息解析错误")
            return {}
        except Exception as e:
            traceback.format_exc(e)
            Logger().e(tag="parser_class_table_bottom", content="课表底部，解析未知错误")
            return {}

    @staticmethod
    def parse_class_table_body(html_text, all_course_dict):
        try:
            course_table_template = "new TaskActivity(actTeacherId.join(','),actTeacherName.join(','),{});"
            courses = search_all(course_table_template, html_text)
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
        except IndexError as e:
            traceback.format_exc(e)
            Logger().e(tag="parser_class_table_body", content="课表体，解析越界")
            return {}
        except Exception as e:
            traceback.format_exc(e)
            Logger().e(tag="parser_class_table_body", content="课表体，解析未知错误")
            return {}

    @staticmethod
    def parse_std_info(html_doc):
        try:
            rows = html_doc.xpath('/html/body/div/div[2]/div[1]/table/tr')[1:-1]
            data_keys = [
                'username', 'name', 'photoURL', 'nickname', 'gender', 'grade', 'duration', 'project',
                'diplomas', 'studentType', 'college', 'major', 'direction', 'entranceDate', 'graduateDate',
                'collegeAdmin', 'trainForm', 'isRecordingNow', 'isInSchool', 'campus', 'studentClass',
                'recordEffectDate', 'isOwnRecord', 'recordStatus', 'isWorking']
            data_values = [cell.text
                           for row in rows
                           for cell in row.xpath('./td[not(@class="title")]')]
            # 另一种解析
            # for cell in row.xpath('./td[not(@class="title")]')]
            # print(F"{len(data_keys)} - {len(data_values)}")
            assert len(data_keys) == len(data_values), 'data parser error'
            data = dict(zip(data_keys, data_values))
            data[
                'photoURL'] = F"http://202.199.224.119:8080/eams/showSelfAvatar.action?user.name={data.get('username', 'None')}"
            # print(data)
            return data
        except IndexError:
            Logger().e(tag="parse_std_info", content="信息，详细信息解析错误")
        except Exception as e:
            traceback.format_exc(e)
            Logger().e(tag="parse_std_info", content="课表底部，解析未知错误")
