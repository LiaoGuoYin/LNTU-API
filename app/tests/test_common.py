import unittest

from app import schemas
from app.common.notice import get_notice_url_list, get_notice_detail
from app.common.room import get_building_html, process_building_html, get_class_room_html, parse_class_room_html


class TestEducationParser(unittest.TestCase):
    def test_room_get_building_html(self):
        html_text = get_building_html(is_save=True)
        self.assertIn('教室占用查询-辽宁工程技术大学教务处', html_text)

    def test_room_process_building_html(self):
        with open('static/class-room-building.html', 'r') as fp:
            html_text = fp.read()
        building_dict = process_building_html(html_text)
        self.assertTrue(len(building_dict.get('fuxin')) != 0)
        self.assertTrue(len(building_dict.get('huludao')) != 0)
        print(building_dict)

    def test_room_get_class_room_html(self):
        request_room_params = {
            'semesterId': 627,
            'iWeek': 1,
            'room.building.id': 14,
            'buildingname': '耘慧楼'
        }
        html_text = get_class_room_html(request_room_params=request_room_params, is_save=True)
        self.assertIn('2020-2021学年第1学期教室占用情况', html_text)

    def test_room_parse_class_room_html(self):
        with open('static/class-room.html', 'r') as fp:
            html_text = fp.read()
        class_room_list = parse_class_room_html(html_text)
        self.assertTrue(len(class_room_list) != 0)
        print(class_room_list)

    def test_notice_get_notice_url_list(self):
        notice_url_list = get_notice_url_list()
        self.assertTrue(len(notice_url_list) > 0)
        print(notice_url_list)

    def test_notice_get_notice_detail(self):
        # TODO
        url = 'http://jwzx.lntu.edu.cn/index/../info/1103/1503.htm'
        notice = schemas.Notice(url=url)
        notice = get_notice_detail(notice)
        self.assertTrue(len(notice.title) > 0)
        self.assertTrue(len(notice.content) > 0)
