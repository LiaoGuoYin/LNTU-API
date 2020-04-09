from lxml import etree

from quality.parser import ExpansionParser


def test_parse_expansion_report():
    with open('../testHTML/expansion-report.html', encoding='utf-8') as fp:
        html_text = fp.read()
        html_doc = etree.HTML(html_text)
    ExpansionParser.parse_report(html_doc)


def test_parse_expansion_mind_activity():
    with open('../testHTML/expansion-mind-activity.html', encoding='utf-8') as fp:
        html_text = fp.read()
        html_doc = etree.HTML(html_text)
    ExpansionParser.parse_activity(html_doc)


test_parse_expansion_report()
# test_parse_expansion_mind_activity()
