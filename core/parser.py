import traceback

from parse import findall

from util import GetWeek, Logger


class LNTUParser:
    @staticmethod
    def parse_class_table_bottom(html):
        xpath_of_table_bottom = '//*[@id="tasklesson"]/div/table/tbody/tr'
        try:
            rows = html.xpath(xpath_of_table_bottom)
            data_lists = []
            data_dict = {}
            for row in rows:
                data_lists.extend([row.text.split()])
                # 老掉牙的解析
                # cells = row.xpath('./td')
                # print(cells.text)
                # data = ["".join(cell.xpath('string(.)').split()) for cell in cells]
            for row in data_lists:
                name = row[2]
                credit = row[3]
                id = row[4]
                teacher = row[5]
                tmp_dict = {
                    id: {
                        'name': name,
                        'teacher': teacher,
                        'credit': credit,
                        'time_room': [],
                    }
                }
                data_dict.update(tmp_dict)
            print(data_dict)
            return data_dict
        except IndexError:
            Logger().e(tag="parser_class_table_bottom", content="课表底部，详细信息解析错误")
        except Exception as e:
            traceback.format_exc(e)
            Logger().e(tag="parser_class_table_bottom", content="课表底部，解析未知错误")

    @staticmethod
    def parse_class_table_body(html_text, course_total_dict):
        try:
            course_table_template = "new TaskActivity(actTeacherId.join(','),actTeacherName.join(','),{});"
            courses = findall(course_table_template, html_text)
            data_lists = [course[0].replace('\"', '').split(',') for course in courses]
            # print(data_lists)
            for each in data_lists:
                id = each[1].split('(')[1][:-1]
                room = each[3]
                time = GetWeek().marshal(each[4], 2, 1, 50)
                room_time = F"{room} {time}"
                course_ori = course_total_dict.get(id)
                course_ori.get('time_room').append(room_time)
            print(course_total_dict)
        except IndexError as e:
            traceback.format_exc(e)
            Logger().e(tag="parser_class_table_body", content="课表体，解析越界")
        except Exception as e:
            traceback.format_exc(e)
            Logger().e(tag="parser_class_table_body", content="课表体，解析未知错误")

    @staticmethod
    def parse_std_info(html):
        try:
            rows = html.xpath('/html/body/div/div[2]/div[1]/table/tr')[1:-1]
            data_keys = ['username', 'name', 'nickname', 'gender', 'photoURL', 'nickname', 'grade', 'gradeYear0',
                         'gradeYear1',
                         'trainFrom', 'college', 'major', 'majorDirection', 'startDate', 'endDate', 'collegeAdmin',
                         'studyForm',
                         'isNowRecording0', 'isSchool', 'campus', 'class', 'recordEffectDate', 'study',
                         'isNowRecording1',
                         'isWorking']
            data_values = [cell.text
                           for row in rows
                           for cell in row.xpath('//td[not(@class="title")]')]
            print(F"{len(data_keys)} - {len(data_values)}")
            assert len(data_keys) == len(data_values), 'data parser error'
            data = dict(zip(data_keys, data_values))
            data[
                'photoURL'] = F"http://202.199.224.119:8080/eams/showSelfAvatar.action?user.name={data.get('username', None)}"
            print(data)
            return data
        except IndexError:
            Logger().e(tag="parse_std_info", content="信息，详细信息解析错误")
        except Exception as e:
            traceback.format_exc(e)
            Logger().e(tag="parse_std_info", content="课表底部，解析未知错误")
