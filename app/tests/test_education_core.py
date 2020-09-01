import unittest
import os

from lxml import etree
from requests import Session

from app.education.core import login, get_stu_info, get_class_table, get_grade, check_education_online, get_grade_table
from app.education.gpa import gpa_util
from app.education.parser import parse_grade, parse_grade_table
from app.exceptions import TokenException, FormException

APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_file_dict = {
    'config': f'{APP_ABSOLUTE_PATH}/../config.yaml',
    'info': f'{APP_ABSOLUTE_PATH}/tests/static/info.html',
    'class-table': f'{APP_ABSOLUTE_PATH}/tests/static/class-table.html',
    'grade': f'{APP_ABSOLUTE_PATH}/tests/static/grade.html',
    'grade-table': f'{APP_ABSOLUTE_PATH}/tests/static/grade-table.html',
}


def get_test_users():
    import yaml
    with open(local_file_dict['config']) as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    return config['account']


user_dict = get_test_users()


class TestEducationCore(unittest.TestCase):
    # 只检测作为一个正常 User 的操作情况，不检验解析
    def test_education_core_is_education_online(self):
        self.assertEqual(check_education_online(), True)

    def test_education_core_login_valid_user(self):
        response = login(**user_dict['valid'])
        self.assertIsInstance(response, Session)

    def test_education_core_login_invalid_user(self):
        self.assertRaises(TokenException, login, **user_dict['invalid'])
        username = 10000000
        self.assertRaises(FormException, login, username, 'test')

    def test_education_core_get_info(self):
        get_stu_info(**user_dict['valid'], is_save=True)
        with open(local_file_dict['info']) as f:
            html_text = f.read()
        self.assertIn('学籍信息', html_text)

    def test_education_core_class_table(self):
        class_table_list = get_class_table(**user_dict['valid'], is_save=True)
        with open(local_file_dict['class-table']) as f:
            html_text = f.read()
        self.assertIn('课表格式说明', html_text)
        self.assertTrue(len(class_table_list) > 0)

    def test_education_core_grade(self):
        grade_list = get_grade(**user_dict['valid'], is_save=True)
        with open(local_file_dict['grade']) as f:
            html_text = f.read()
        self.assertIn('学年学期', html_text)
        self.assertTrue(len(parse_grade(etree.HTML(html_text))) > 0)
        print(parse_grade(etree.HTML(html_text)))
        self.assertTrue(len(grade_list) > 0)

    def test_education_core_grade_table(self):
        grade_table_list = get_grade_table(**user_dict['valid'], is_save=True)
        with open(local_file_dict['grade-table']) as f:
            html_text = f.read()
        self.assertIn('个人成绩总表打印', html_text)
        self.assertTrue(len(grade_table_list) > 0)

    def test_gpa_grade(self):
        with open(local_file_dict['grade']) as f:
            html_text = f.read()
        grade_list = parse_grade(html_doc=etree.HTML(html_text))
        gpa_result = gpa_util(grade_list)
        self.assertTrue(len(gpa_result) != 0)
        print(gpa_result)

    def test_gpa_grade_table(self):
        with open(local_file_dict['grade-table']) as f:
            html_text = f.read()
        grade_list = parse_grade_table(html_doc=etree.HTML(html_text))
        gpa_result = gpa_util(grade_list)
        self.assertTrue(len(gpa_result) != 0)
        print(gpa_result)
