from app import schemas


def parse_report(html_doc) -> list:
    report_list = []

    # 个人基本资料
    student_info = html_doc.xpath('string(//*[@id="Table1"])').split()
    report_list.append(student_info)

    # 个人成绩单
    report_table_elements = html_doc.xpath('//*[@id="basic1"]/tr')
    for row in report_table_elements[1:]:
        data_list = ["".join(cells.text.split()) for cells in row]
        if len(data_list) == 4:
            data_list.insert(0, '同上')  # TODO
        report_list.append(data_list)

    # 个人活动记录
    report_table_elements = html_doc.xpath('//*[@id="Table2"]/tr')
    for row in report_table_elements[1:]:
        report_list.append(row.xpath('string(.)').split())
    return report_list


def parse_activity(html_doc, activity_type: str) -> [schemas.QualityActivity]:
    result_list = []
    table_row_list = html_doc.xpath('//*[@id="GridView1"]/tr')
    for row in table_row_list[1:]:
        try:
            data_list = [td.text for td in row]
            if data_list[-1] is not None:  # unPassed record
                data_list[-1] = row[-1].xpath('./@title')[0]
            tmp_activity = schemas.QualityActivity(type=activity_type, id=int(data_list[0]))
            tmp_activity.name = '' if data_list[1] is None else ''.join(data_list[1].split())
            tmp_activity.semester = data_list[2].replace('上', '春').replace('下', '秋')
            tmp_activity.activityDate = data_list[3].replace('下', '秋')
            tmp_activity.location = data_list[4]
            tmp_activity.responsibility = data_list[5]
            tmp_activity.loggingDateTime = data_list[-3]
            tmp_activity.status = data_list[-2]
            tmp_activity.comment = '' if data_list[-1] is None else ''.join(data_list[-1].split())
            if activity_type == 'mind':
                tmp_activity.type = '主题思想教育活动'
            elif activity_type == 'competition':
                tmp_activity.type = '学术科研大创论文'
                tmp_activity.name = data_list[2]
                tmp_activity.responsibility = f'{data_list[1]}，学分 {data_list[3]}'
                tmp_activity.activityDate = '' if tmp_activity.loggingDateTime is None else \
                    tmp_activity.loggingDateTime.split(' ')[0]
                tmp_activity.location = ''
                tmp_activity.semester = ''
            elif activity_type == 'social':
                tmp_activity.type = '社会实践专业实践'
            elif activity_type == 'employment':
                tmp_activity.type = '[选修]学生干部任职'
                tmp_activity.activityDate, tmp_activity.responsibility = tmp_activity.responsibility, tmp_activity.activityDate
            elif activity_type == 'skill':
                tmp_activity.type = '[选修]技能认证'
                tmp_activity.activityDate, tmp_activity.responsibility = tmp_activity.semester, tmp_activity.activityDate
            else:
                tmp_activity.type = '品读经典著作读后感活动'
            result_list.append(tmp_activity)
        except IndexError:
            continue
    return result_list


def parse_scholarship(html_doc) -> [schemas.QualityScholarship]:
    result_list = []
    table_rows = html_doc.xpath('//*[@id="GridView1"]/tr')
    for row in table_rows[1:]:
        data_list = [td.text for td in row]
        tmp_scholarship = schemas.QualityScholarship(id=int(data_list[0]))
        tmp_scholarship.semester = data_list[1]
        tmp_scholarship.activityType = data_list[3]
        tmp_scholarship.activityContent = data_list[4]
        tmp_scholarship.activityLevel = data_list[5]
        tmp_scholarship.creditType = data_list[2]
        tmp_scholarship.credit = data_list[-1]
        result_list.append(tmp_scholarship)
    return result_list
