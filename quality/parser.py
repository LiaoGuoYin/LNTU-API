class ExpansionParser:

    @staticmethod
    def parse_report(html_doc):
        student_info = html_doc.xpath('string(//*[@id="Table1"])').split()
        print(student_info)

        # 个人成绩单
        report_table_elements = html_doc.xpath('//*[@id="basic1"]/tr')
        for row in report_table_elements[1:]:
            data_list = ["".join(cells.text.split()) for cells in row]
            if len(data_list) == 4:
                data_list.insert(0, "同上")  # TODO
            print(data_list)

        # 个人活动记录
        report_table_elements = html_doc.xpath('//*[@id="Table2"]/tr')
        for row in report_table_elements[1:]:
            print(row.xpath('string(.)').split())

    @staticmethod
    def parse_activity(html_doc):
        table_rows = html_doc.xpath('//*[@id="GridView1"]/tr')
        for row in table_rows[1:]:
            data_list = [td.text for td in row]
            # unPassed record
            if data_list[-1] is not None:
                data_list[-2] = data_list[-2] + "认证失败！"
                data_list[-1] = row[-1].xpath('./@title')[0]
            print(data_list)

    @staticmethod
    def parse_scholarship(html_doc):
        table_rows = html_doc.xpath('//*[@id="GridView1"]/tr')
        for row in table_rows[1:]:
            data_list = [td.text for td in row]
            print(data_list)
