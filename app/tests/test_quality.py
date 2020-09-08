import os

from lxml import etree

from app.quality.parser import parse_report, parse_activity

APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_file_dict = {
    'quality-report': f'{APP_ABSOLUTE_PATH}/tests/static/quality-report.html',
    'quality-activity': f'{APP_ABSOLUTE_PATH}/tests/static/quality-activity.html',
}


def test_parse_expansion_report():
    with open(local_file_dict['quality-report']) as fp:
        html_text = fp.read()
        html_doc = etree.HTML(html_text)
    parse_report(html_doc)


def test_parse_expansion_mind_activity():
    with open(local_file_dict['quality-activity']) as fp:
        html_text = fp.read()
        html_doc = etree.HTML(html_text)
    parse_activity(html_doc)


test_parse_expansion_report()
# test_parse_expansion_mind_activity()
