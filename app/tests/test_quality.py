import unittest

from lxml import etree

from app.quality import core
from app.quality.parser import parse_report, parse_activity
from app.quality.urls import QualityExpansionURLEnum
from app.constants import constantsShared

local_html_file_dict = constantsShared.get_local_html_file_dict()
quality_user_dict = constantsShared.get_quality_user_dict()


class TestQuality(unittest.TestCase):
    cookie = ''

    def setUp(self) -> None:
        self.cookie = core.get_cookie(**quality_user_dict)
        core.get_report(self.cookie, is_save=True)
        core.get_single_activity(QualityExpansionURLEnum.MIND.value, 'mind', self.cookie, is_save=True)

    def test_quality_get_cookie(self):
        self.assertTrue(self.cookie.startswith('ASP'))

    def test_quality_parse_report(self):
        with open(local_html_file_dict['quality-report']) as fp:
            html_text = fp.read()
            html_doc = etree.HTML(html_text)
        self.assertTrue(len(parse_report(html_doc)) != 0)

    def test_quality_get_single_activity(self):
        with open(local_html_file_dict['quality-activity']) as fp:
            html_text = fp.read()
            html_doc = etree.HTML(html_text)
        self.assertTrue(parse_activity(html_doc, 'mind')[0].type == 'mind')


if __name__ == '__main__':
    unittest.main()
