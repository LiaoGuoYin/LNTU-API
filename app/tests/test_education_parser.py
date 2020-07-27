import json
import unittest

from lxml import etree

from app import schemas
from app.education.parser import parse_stu_info, parse_grades, parse_class_table_bottom, parse_class_table_body


class TestEducationParser(unittest.TestCase):
    def test_education_parse_info(self):
        with open('app/tests/static/info.html', 'r') as f:
            html_text = f.read()
        self.assertIn('学籍信息', html_text)

        data_dict = parse_stu_info(html_doc=etree.HTML(html_text))
        self.assertIsInstance(data_dict, schemas.UserInfo)
        print(data_dict)

    def test_education_parse_class_table(self):
        with open('app/tests/static/class-table.html', 'r') as f:
            html_text = f.read()
        self.assertIn('课表格式说明', html_text)

        part_course_dict_list = parse_class_table_bottom(html_doc=etree.HTML(html_text))
        data_list = parse_class_table_body(html_text, part_course_dict_list)
        self.assertIsInstance(part_course_dict_list, list)
        self.assertIsInstance(data_list, list)

        [print(each) for each in part_course_dict_list]
        [print(json.dumps(each.self_dict(), ensure_ascii=False)) for each in data_list]

    def test_education_parse_grades(self):
        with open('app/tests/static/grades.html', 'r') as f:
            html_text = f.read()
        self.assertIn('学年学期', html_text)

        grades_list = parse_grades(html_doc=etree.HTML(html_text))
        self.assertIsInstance(grades_list, list)
        print(grades_list)
