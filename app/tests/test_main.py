import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.constants import constantsShared

education_user_dict = constantsShared.get_education_user_dict()
quality_user_dict = constantsShared.get_quality_user_dict()
current_year = constantsShared.current_semester[:4]


class TestMainAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_education_info(self):
        response = self.client.post('/education/info', json=education_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_course_table(self):
        payload = {'semester': '2020-秋'}
        response = self.client.post('/education/course-table', params=payload, json=education_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_grade(self):
        payload = {
            'isIncludingOptionalCourse': 1,
        }
        response = self.client.post('/education/grade', json=education_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_exam(self):
        payload = {'semester': constantsShared.current_semester}
        response = self.client.post('/education/exam', params=payload, json=education_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_data(self):
        response = self.client.post('/education/data', json=education_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_notice(self):
        response = self.client.get('/education/notice', params=education_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_education_class_room(self):
        payload = {
            'week': 10,
            'name': 'eyl'
        }
        response = self.client.get('/education/classroom', params=payload, json=education_user_dict)
        print(response.text)
        self.assertTrue(response.status_code == 200)

    def test_quality_data(self):
        payload = {
            'year': current_year,
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
