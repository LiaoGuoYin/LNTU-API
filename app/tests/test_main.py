import os
import unittest

from fastapi.testclient import TestClient

from app.main import app

APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_test_users():
    import yaml
    with open(f'{APP_ABSOLUTE_PATH}/../config.yaml') as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    return config['education-account'], config['quality-account']


user_dict, quality_user_dict = get_test_users()


class TestMainAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_education_info(self):
        response = self.client.post('/education/info', json=user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_data(self):
        response = self.client.post('/education/data', json=user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_course_table(self):
        payload = {'semester': '2020-2'}
        response = self.client.post('/education/course-table', params=payload, json=user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_grade(self):
        payload = {
            'semester': '2020-1',
            'isIncludingOptionalCourse': 1,
        }
        payload.update(user_dict)
        response = self.client.get('/education/grade', params=payload)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_gpa_all(self):
        response = self.client.get('/education/gpa-all', params=user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_notice(self):
        response = self.client.get('/education/notice', params=user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_class_room(self):
        payload = {
            'week': 10,
            'name': 'eyl'
        }
        response = self.client.get('/education/classroom', params=payload, json=user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_quality_data(self):
        payload = {
            'year': '2020'
        }
        response = self.client.post('quality/data', params=payload, json=quality_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_quality_report(self):
        response = self.client.post('/quality/report', json=quality_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
    unittest.main()
