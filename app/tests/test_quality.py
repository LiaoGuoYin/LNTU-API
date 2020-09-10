import os
import unittest

from lxml import etree

from app.quality import core
from app.quality.parser import parse_report, parse_activity
from app.quality.urls import QualityExpansionURLEnum

APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_file_dict = {
    'config': f'{APP_ABSOLUTE_PATH}/../config.yaml',
    'quality-report': f'{APP_ABSOLUTE_PATH}/tests/static/quality-report.html',
    'quality-activity': f'{APP_ABSOLUTE_PATH}/tests/static/quality-activity.html',
}


def get_test_users():
    import yaml
    with open(local_file_dict['config']) as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    return config['quality-account']


user_dict = get_test_users()


class TestQuality(unittest.TestCase):
    cookie = ''

    def setUp(self) -> None:
        self.cookie = core.get_cookie(**user_dict)
        # Download some html file to local
        core.get_report(self.cookie, is_save=True)
        core.get_single_activity(QualityExpansionURLEnum.MIND.value, self.cookie, is_save=True)

    def test_quality_get_cookie(self):
        self.assertTrue(self.cookie.startswith('ASP'))

    def test_quality_parse_report(self):
        with open(local_file_dict['quality-report']) as fp:
            html_text = fp.read()
            html_doc = etree.HTML(html_text)
        self.assertTrue(len(parse_report(html_doc)) != 0)

    def test_quality_get_single_activity(self):
        with open(local_file_dict['quality-activity']) as fp:
            html_text = fp.read()
            html_doc = etree.HTML(html_text)
        self.assertTrue(len(parse_activity(html_doc)) != 0)


if __name__ == '__main__':
    unittest.main()
