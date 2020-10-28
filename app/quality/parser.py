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
        data_list = [td.text for td in row]
        if data_list[-1] is not None:  # unPassed record
            data_list[-1] = row[-1].xpath('./@title')[0]
        tmp_activity = schemas.QualityActivity(type=activity_type, id=int(data_list[0]))
        tmp_activity.name = data_list[1]
        tmp_activity.semester = data_list[2]
        tmp_activity.activityDate = data_list[3]
        tmp_activity.location = data_list[4]
        tmp_activity.responsibility = data_list[5]
        tmp_activity.loggingDateTime = data_list[-3]
        tmp_activity.status = data_list[-2]
        tmp_activity.comment = data_list[-1]
        if activity_type == 'mind' or activity_type == 'social':
            pass
        elif activity_type == 'employment':
            tmp_activity.activityDate, tmp_activity.responsibility = tmp_activity.responsibility, tmp_activity.activityDate
        elif activity_type == 'skill':
            tmp_activity.activityDate, tmp_activity.responsibility = tmp_activity.responsibility, tmp_activity.activityDate
        elif activity_type == 'competition':
            tmp_activity.responsibility = data_list[2]
            tmp_activity.location = tmp_activity.activityDate
            tmp_activity.semester = ''
            tmp_activity.activityDate = ''
        result_list.append(tmp_activity)
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
