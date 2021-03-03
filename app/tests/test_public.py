import unittest

from app import schemas
from app.public.room import initialize_to_get_building_id_html, process_building_html, get_class_room_html, \
    parse_class_room_html
from app.public import helper
from app.constants import constantsShared
from app.public import notice

app_path = constantsShared.app_path
local_html_file_dict = constantsShared.get_local_html_file_dict()


class TestPublic(unittest.TestCase):
    def test_room_initialize_to_get_building_id_html(self):
        html_text = initialize_to_get_building_id_html(is_save=True)
        self.assertIn('教室占用查询-辽宁工程技术大学教务处', html_text)

    def test_room_process_building_html(self):
        with open(local_html_file_dict['class-room-building']) as fp:
            html_text = fp.read()
        building_dict = process_building_html(html_text)
        print(building_dict)
        self.assertTrue(len(building_dict.get('fuxin')) != 0)
        self.assertTrue(len(building_dict.get('huludao')) != 0)

    def test_room_get_class_room_html(self):
        html_text = get_class_room_html(1, 14, is_save=True)
        self.assertIn('教室占用情况', html_text)

    def test_room_parse_class_room_html(self):
        with open(local_html_file_dict['class-room'], 'r') as fp:
            html_text = fp.read()
        class_room_list = parse_class_room_html(html_text)
        print(class_room_list)
        self.assertTrue(len(class_room_list) != 0)

    def test_notice_get_notice_url_list_from(self):
        notice_list = notice.get_notice_url_list_from(page_url='http://jwzx.lntu.edu.cn/index/jwgg.htm')
        self.assertTrue(len(notice_list) != 0)
        self.assertIsInstance(notice_list[0], schemas.Notice)
        self.assertTrue(notice_list[0].title != '')
        print(notice_list)

    def test_helper_message(self):
        self.assertIsInstance(helper.refresh_helper_message().__class__, schemas.HelperMessage.__class__)
