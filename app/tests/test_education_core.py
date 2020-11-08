import unittest
import os

from lxml import etree
from requests import Session

from app.education import parser, core
from app.exceptions import FormException

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


def get_test_users():
    import yaml
    with open(local_file_dict['config']) as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    return config['education-account']


user_dict = get_test_users()


class TestEducationCore(unittest.TestCase):
    # 只检测作为一个正常 User 的操作情况，不检验解析
    def test_education_core_is_education_online(self):
        self.assertEqual(core.is_education_online(), True)

    def test_education_core_login_valid_user(self):
        response = core.login(**user_dict)
        self.assertIsInstance(response, Session)

    def test_education_core_login_invalid_user(self):
        invalid_user = user_dict.copy()
        invalid_user['password'] += '000'
        self.assertRaises(FormException, core.login, **invalid_user)
        username = 10000000
        self.assertRaises(FormException, core.login, username, 'test')

    def test_education_core_get_info(self):
        core.get_stu_info(**user_dict, is_save=True)
        with open(local_file_dict['info']) as f:
            html_text = f.read()
        self.assertIn('学籍信息', html_text)

    def test_education_core_course_table(self):
        course_table_list = core.get_course_table(**user_dict, is_save=True)
        with open(local_file_dict['course-table']) as f:
            html_text = f.read()
        self.assertIn('课表格式说明', html_text)
        self.assertTrue(len(course_table_list) > 0)
        print(course_table_list)

    def test_education_core_grade(self):
        grade_list = core.get_grade(**user_dict, is_save=True)
        with open(local_file_dict['grade']) as f:
            html_text = f.read()
        self.assertTrue('学年学期' or '所有成绩尚未发布' in html_text)
        self.assertTrue(len(parser.parse_grade(etree.HTML(html_text))) > 0)
        print(parser.parse_grade(etree.HTML(html_text)))
        self.assertTrue(len(grade_list) > 0)

    def test_education_core_grade_table(self):
        grade_table_list = core.get_grade_table(**user_dict, is_save=True)
        with open(local_file_dict['grade-table']) as f:
            html_text = f.read()
        self.assertIn('个人成绩总表打印', html_text)
        self.assertTrue(len(grade_table_list) > 0)

    def test_gpa_grade(self):
        with open(local_file_dict['grade']) as f:
            html_text = f.read()
        grade_list = parser.parse_grade(html_doc=etree.HTML(html_text))
        gpa_result = core.calculate_gpa(grade_list, is_including_optional_course='1')
        self.assertIsInstance(gpa_result.courseCount, int)
        print(gpa_result)

    def test_gpa_grade_table(self):
        with open(local_file_dict['grade-table']) as f:
            html_text = f.read()
        grade_list = parser.parse_grade_table(html_doc=etree.HTML(html_text))
        gpa_result = core.calculate_gpa(grade_list, is_including_optional_course='1')
        self.assertIsInstance(gpa_result.courseCount, int)
        print(gpa_result)

    def test_education_core_exam(self):
        exam_list = core.get_exam(**user_dict, semester_id=627, is_save=True)
        with open(local_file_dict['exam']) as f:
            html_text = f.read()
        self.assertIsInstance(exam_list, list)
        self.assertIn('课程序号', html_text)

    def test_education_core_other_exam(self):
        other_exam_list = core.get_other_exam(**user_dict, is_save=True)
        with open(local_file_dict['other-exam']) as f:
            html_text = f.read()
        self.assertIsInstance(other_exam_list, list)
        self.assertIn('资格考试', html_text)

    def test_education_core_plan(self):
        exam_list = core.get_plan(**user_dict, is_save=True)
        with open(local_file_dict['plan']) as f:
            html_text = f.read()
        self.assertIsInstance(exam_list, list)
        self.assertIn('计划完成情况', html_text)
