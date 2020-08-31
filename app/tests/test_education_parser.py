import json
import unittest

from lxml import etree

from app import schemas
from app.education.parser import parse_stu_info, parse_grade, parse_class_table_bottom, parse_class_table_body, \
    parse_grade_table


class TestEducationParser(unittest.TestCase):
    def test_education_parse_info(self):
        with open('static/info.html', 'r') as f:
            html_text = f.read()
        self.assertIn('学籍信息', html_text)

        data_dict = parse_stu_info(html_doc=etree.HTML(html_text))
        self.assertIsInstance(data_dict, schemas.UserInfo)
        print(data_dict)

    def test_education_parse_class_table(self):
        with open('static/class-table.html', 'r') as f:
            html_text = f.read()
        self.assertIn('课表格式说明', html_text)

        part_course_dict_list = parse_class_table_bottom(html_doc=etree.HTML(html_text))
        data_list = parse_class_table_body(html_text, part_course_dict_list)
        self.assertIsInstance(part_course_dict_list, list)
        self.assertIsInstance(data_list, list)

        [print(each) for each in part_course_dict_list]
        [print(json.dumps(each.self_dict(), ensure_ascii=False)) for each in data_list]

    def test_education_parse_grade(self):
        with open('static/grade.html', 'r') as f:
            html_text = f.read()
        self.assertIn('学年学期', html_text)

        grade_list = parse_grade(html_doc=etree.HTML(html_text))
        self.assertIsInstance(grade_list, list)
        print(grade_list)

    def test_education_parse_grade_table(self):
        with open('static/grade-table.html', 'r') as f:
            html_text = f.read()
        self.assertIn('个人成绩总表打印', html_text)

        grade_table_list = parse_grade_table(html_doc=etree.HTML(html_text))
        self.assertIsInstance(grade_table_list, list)
        print(grade_table_list)
