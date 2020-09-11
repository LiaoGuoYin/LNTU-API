import json
import os
import unittest

from lxml import etree

from app import schemas
from app.education.parser import parse_stu_info, parse_grade, parse_course_table_bottom, parse_course_table_body, \
    parse_grade_table

APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_file_dict = {
    'config': f'{APP_ABSOLUTE_PATH}/../config.yaml',
    'info': f'{APP_ABSOLUTE_PATH}/tests/static/info.html',
    'course-table': f'{APP_ABSOLUTE_PATH}/tests/static/course-table.html',
    'grade': f'{APP_ABSOLUTE_PATH}/tests/static/grade.html',
    'grade-table': f'{APP_ABSOLUTE_PATH}/tests/static/grade-table.html',
}


class TestEducationParser(unittest.TestCase):
    def test_education_parse_info(self):
        with open(local_file_dict['info']) as f:
            html_text = f.read()
        self.assertIn('学籍信息', html_text)

        data_dict = parse_stu_info(html_doc=etree.HTML(html_text))
        self.assertIsInstance(data_dict, schemas.UserInfo)
        print(data_dict)

    def test_education_parse_course_table(self):
        with open(local_file_dict['course-table']) as f:
            html_text = f.read()
        self.assertIn('课表格式说明', html_text)

        part_course_dict_list = parse_course_table_bottom(html_doc=etree.HTML(html_text))
        data_list = parse_course_table_body(html_text, part_course_dict_list)
        self.assertIsInstance(part_course_dict_list, list)
        self.assertIsInstance(data_list, list)

        [print(each) for each in part_course_dict_list]
        [print(json.dumps(each.self_dict(), ensure_ascii=False)) for each in data_list]

    def test_education_parse_grade(self):
        with open(local_file_dict['grade']) as f:
            html_text = f.read()
        self.assertIn('学年学期', html_text)

        grade_list = parse_grade(html_doc=etree.HTML(html_text))
        self.assertIsInstance(grade_list, list)
        print(grade_list)

    def test_education_parse_grade_table(self):
        with open(local_file_dict['grade-table']) as f:
            html_text = f.read()
        self.assertIn('个人成绩总表打印', html_text)

        grade_table_list = parse_grade_table(html_doc=etree.HTML(html_text))
        self.assertTrue(len(grade_table_list) != 0)
        self.assertIsInstance(grade_table_list[0], schemas.GradeTable)
        print(grade_table_list)
