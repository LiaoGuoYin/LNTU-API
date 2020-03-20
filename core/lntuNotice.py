import requests
from lxml import etree

from modelset.schemas import Notice, NoticeDetailAppendix


def get_notice_url_list_from(page_url):
    xpath_str = '/html/body/div[3]/div[2]/div[2]/ul/li'
    response = requests.get(page_url)
    response.encoding = 'utf-8'
    html_doc = etree.HTML(response.text)
    ul_list = html_doc.xpath(xpath_str)
    url_list = []
    for row in ul_list[::-1]:
        url_origin = row.xpath("./a/@href")[0]
        url = ('http://jwzx.lntu.edu.cn/index/' + url_origin) if url_origin.startswith(
            '..') else url_origin
        # notice_dict['title'] = row.xpath("./a/em/text()")[0]
        # notice_dict['date'] = row.xpath("./a/span/text()")[0]
        url_list.append(url)
    return url_list


def notice_detail_spider(notice: Notice):
    xpath_str = '/html/body/div[3]/form/div[1]'
    response = requests.get(notice.url)
    response.encoding = 'utf-8'
    html_doc = etree.HTML(response.text)
    notice_elements = html_doc.xpath(xpath_str)[0]
    notice.detail.title = notice_elements.xpath('./div/h1/text()')[0]
    notice.detail.date = notice_elements.xpath('./div/h3/text()')[1][3:]
    notice.detail.content = notice_elements.xpath('string(./div[@id="vsb_content"]/div)')
    if '附件' in notice.detail.content:
        get_appendix(html_doc, notice)
    return notice


def get_appendix(html_doc, notice: Notice):
    appendix_xpath = '/html/body/div[3]/form/div[1]/ul/li'
    appendix_elements = html_doc.xpath(appendix_xpath)
    for row in appendix_elements:
        name = 'http://jwzx.lntu.edu.cn/' + row.xpath('./a/@href')[0]
        url = row.xpath('./a/text()')[0]
        appendix = NoticeDetailAppendix(url=url, name=name)
        notice.detail.appendix.append(appendix)


def get_public_notice():
    try:
        page_list = ['http://jwzx.lntu.edu.cn/index/jwgg.htm']
        # page_list.extend(['http://jwzx.lntu.edu.cn/index/jwgg/{page}.htm'.format(page=i)
        #                   for i in range(1, 15)])
        url_list = list(map(get_notice_url_list_from, page_list))[0]
        notices: [Notice] = []
        for url in url_list:
            notice = Notice(url=url)
            notice = notice_detail_spider(notice)
            notices.append(notice)
        return notices
    except IndexError:
        return "教务在线通知爬虫爆炸"


if __name__ == '__main__':
    print(get_public_notice())
