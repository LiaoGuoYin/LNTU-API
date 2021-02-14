import unittest

from lxml import etree

from app import schemas
from app.education import parser
from app.constants import constantsShared

app_path = constantsShared.app_path
local_html_file_dict = constantsShared.get_local_html_file_dict()

user_dict = constantsShared.get_education_user_dict()
semester_id = constantsShared.current_semester_id


class TestEducationParser(unittest.TestCase):
    def test_education_parse_info(self):
        with open(local_html_file_dict['info']) as f:
            html_text = f.read()
        self.assertIn('学籍信息', html_text)

        data_dict = parser.parse_stu_info(username='1700000000', html_doc=etree.HTML(html_text))
        self.assertIsInstance(data_dict, schemas.UserInfo)
        print(data_dict)

    def test_education_parse_course_table(self):
        with open(local_html_file_dict['course-table']) as f:
            html_text = f.read()
        self.assertIn('课表格式说明', html_text)

        part_course_dict_list = parser.parse_course_table_bottom(html_doc=etree.HTML(html_text))
        data_list = parser.parse_course_table_body(html_text, part_course_dict_list)
        self.assertIsInstance(part_course_dict_list, list)
        self.assertIsInstance(data_list, list)

        [print(each) for each in part_course_dict_list]

    def test_education_parse_grade(self):
        with open(local_html_file_dict['grade']) as f:
            html_text = f.read()
        self.assertTrue('学年学期' or '所有成绩尚未发布' in html_text)

        grade_list = parser.parse_grade(html_doc=etree.HTML(html_text))
        self.assertIsInstance(grade_list, list)
        [print(each) for each in grade_list]

    def test_education_parse_grade_table(self):
        with open(local_html_file_dict['grade-table']) as f:
            html_text = f.read()
        self.assertIn('个人成绩总表打印', html_text)

        grade_table_list = parser.parse_grade_table(html_doc=etree.HTML(html_text))
        self.assertTrue(len(grade_table_list) != 0)
        self.assertIsInstance(grade_table_list[0], schemas.GradeTable)
        [print(each) for each in grade_table_list]

    def test_education_core_exam(self):
        with open(local_html_file_dict['exam']) as f:
            html_text = f.read()

        exam_list = parser.parse_exam(html_doc=etree.HTML(html_text))
        self.assertIsInstance(exam_list, list)
        print(exam_list)

    def test_education_parse_exam_batch_id(self):
        with open(local_html_file_dict['exam-batch-id']) as f:
            html_text = f.read()

        exam_batch_dict = parser.parse_exam_id(html_doc=etree.HTML(html_text))
        self.assertIsInstance(exam_batch_dict, dict)
        print(exam_batch_dict)

    def test_education_core_other_exam(self):
        with open(local_html_file_dict['other-exam']) as f:
            html_text = f.read()

        other_exam_list = parser.parse_other_exam(html_doc=etree.HTML(html_text))
        self.assertIsInstance(other_exam_list, list)
        print(other_exam_list)

    def test_education_parse_plan(self):
        with open(local_html_file_dict['plan']) as f:
            html_text = f.read()

        plan_result = parser.parse_plan(html_doc=etree.HTML(html_text))
        self.assertIsInstance(plan_result, list)
        print(plan_result)

    def test_education_parse_teacher_evaluation(self):
        with open(local_html_file_dict['evaluation']) as f:
            html_text = f.read()

        plan_result = parser.parse_teacher_evaluation(html_doc=etree.HTML(html_text))
        print(plan_result)
        self.assertIsInstance(plan_result, list)
