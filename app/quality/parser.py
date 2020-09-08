def parse_report(html_doc) -> list:
    report_list = []
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


def parse_activity(html_doc) -> list:
    result_list = []
    table_row_list = html_doc.xpath('//*[@id="GridView1"]/tr')
    for row in table_row_list[1:]:
        data_list = [td.text for td in row]
        # unPassed record
        if data_list[-1] is not None:
            data_list[-2] = data_list[-2]
            try:
                data_list[-1] = row[-1].xpath('./@title')[0]
            except IndexError:
                pass
        result_list.append(data_list)
    return result_list


def parse_scholarship(html_doc) -> list:
    result_list = []
    table_rows = html_doc.xpath('//*[@id="GridView1"]/tr')
    for row in table_rows[1:]:
        data_list = [td.text for td in row]
        result_list.append(data_list)
    return result_list
