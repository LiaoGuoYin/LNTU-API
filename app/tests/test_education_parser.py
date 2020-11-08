import os
import unittest

from lxml import etree

from app import schemas
from app.education import parser

APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_file_dict = {
    'config': f'{APP_ABSOLUTE_PATH}/../config.yaml',
    'info': f'{APP_ABSOLUTE_PATH}/tests/static/info.html',
    'course-table': f'{APP_ABSOLUTE_PATH}/tests/static/course-table.html',
    'grade': f'{APP_ABSOLUTE_PATH}/tests/static/grade.html',
    'grade-table': f'{APP_ABSOLUTE_PATH}/tests/static/grade-table.html',
    'exam': f'{APP_ABSOLUTE_PATH}/tests/static/exam.html',
    'other-exam': f'{APP_ABSOLUTE_PATH}/tests/static/other-exam.html',
    'plan': f'{APP_ABSOLUTE_PATH}/tests/static/plan.html',
}


class TestEducationParser(unittest.TestCase):
    def test_education_parse_info(self):
        with open(local_file_dict['info']) as f:
            html_text = f.read()
        self.assertIn('学籍信息', html_text)

        data_dict = parser.parse_stu_info(html_doc=etree.HTML(html_text))
        self.assertIsInstance(data_dict, schemas.UserInfo)
        print(data_dict)

    def test_education_parse_course_table(self):
        with open(local_file_dict['course-table']) as f:
            html_text = f.read()
        self.assertIn('课表格式说明', html_text)

        part_course_dict_list = parser.parse_course_table_bottom(html_doc=etree.HTML(html_text))
        data_list = parser.parse_course_table_body(html_text, part_course_dict_list)
        self.assertIsInstance(part_course_dict_list, list)
        self.assertIsInstance(data_list, list)

        [print(each) for each in part_course_dict_list]

    def test_education_parse_grade(self):
        with open(local_file_dict['grade']) as f:
            html_text = f.read()
        self.assertTrue('学年学期' or '所有成绩尚未发布' in html_text)

        grade_list = parser.parse_grade(html_doc=etree.HTML(html_text))
        self.assertIsInstance(grade_list, list)
        [print(each) for each in grade_list]

    def test_education_parse_grade_table(self):
        with open(local_file_dict['grade-table']) as f:
            html_text = f.read()
        self.assertIn('个人成绩总表打印', html_text)

        grade_table_list = parser.parse_grade_table(html_doc=etree.HTML(html_text))
        self.assertTrue(len(grade_table_list) != 0)
        self.assertIsInstance(grade_table_list[0], schemas.GradeTable)
        [print(each) for each in grade_table_list]

    def test_education_core_exam(self):
        with open(local_file_dict['exam']) as f:
            html_text = f.read()

        exam_list = parser.parse_exam(html_doc=etree.HTML(html_text))
        self.assertIsInstance(exam_list, list)
        print(exam_list)

    def test_education_core_other_exam(self):
        with open(local_file_dict['other-exam']) as f:
            html_text = f.read()

        other_exam_list = parser.parse_other_exam(html_doc=etree.HTML(html_text))
        self.assertIsInstance(other_exam_list, list)
        print(other_exam_list)

    def test_education_parse_plan(self):
        with open(local_file_dict['plan']) as f:
            html_text = f.read()

        plan_result = parser.parse_plan(html_doc=etree.HTML(html_text))
        self.assertIsInstance(plan_result, list)
        print(plan_result)
