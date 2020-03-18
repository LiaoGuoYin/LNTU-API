import requests
from lxml import etree


def get_notice_url_list_from(page_url, notice_url_list: list):
    xpath_str = '/html/body/div[3]/div[2]/div[2]/ul/li'
    response = requests.get(page_url)
    response.encoding = 'utf-8'
    html_doc = etree.HTML(response.text)
    ul_list = html_doc.xpath(xpath_str)
    notice_list = []
    for row in ul_list[::-1]:
        url_origin = row.xpath("./a/@href")[0]
        page_url = ('http://jwzx.lntu.edu.cn/index/' + url_origin) if url_origin.startswith(
            '..') else url_origin
        # notice_dict['title'] = row.xpath("./a/em/text()")[0]
        # notice_dict['date'] = row.xpath("./a/span/text()")[0]
        notice_list.append({'url': page_url})
    notice_url_list.extend(notice_list)


def text_spider(notice: dict):
    url = notice['url']
    xpath_str = '/html/body/div[3]/form/div[1]'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_doc = etree.HTML(response.text)
    notice_elements = html_doc.xpath(xpath_str)[0]
    notice['title'] = notice_elements.xpath('./div/h1/text()')[0]
    notice['date'] = notice_elements.xpath('./div/h3/text()')[1][3:]
    notice_detail_dict = {}
    notice_detail_dict['body'] = notice_elements.xpath('string(./div[@id="vsb_content"]/div)')
    notice_detail_dict['appendix'] = 'None'
    if '附件' in notice_detail_dict['body']:
        notice_detail_dict['appendix'] = get_appendix(html_doc)
    notice['detail'] = notice_detail_dict
    return notice


def get_appendix(html_doc):
    appendix_xpath = '/html/body/div[3]/form/div[1]/ul/li'
    appendix_elements = html_doc.xpath(appendix_xpath)
    appendix_list = []
    for row in appendix_elements:
        appendix_dict = {}
        appendix_dict['name'] = 'http://jwzx.lntu.edu.cn/' + row.xpath('./a/@href')[0]
        appendix_dict['url'] = row.xpath('./a/text()')[0]
        appendix_list.append(appendix_dict)
    return appendix_list


def get_public_notice():
    # page_list = ['http://jwzx.lntu.edu.cn/index/jwgg/{page}.htm'.format(page=i)
    # for i in range(1, 15)]  # TODO
    # url_list.append('http://jwzx.lntu.edu.cn/index/jwgg.htm')
    # for page_url in page_list:
    #     get_notice_url_list_from(page_url, notice_url_dict_list)
    try:
        notice_url_list = []
        notice_data_list = []
        page_list = ['http://jwzx.lntu.edu.cn/index/jwgg.htm']
        get_notice_url_list_from(page_list[0], notice_url_list)
        for url_dict in notice_url_list:
            notice = {
                'url': url_dict['url'],
                'detail': {
                    'title': '',
                    'date': '',
                    'content': '',
                    'appendix': [],
                }
            }
            notice = text_spider(notice)
            notice_data_list.append(notice)
        return notice_data_list
    except IndexError:
        return "教务在线通知爬虫爆炸"


if __name__ == '__main__':
    print(get_public_notice())
