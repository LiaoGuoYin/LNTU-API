import requests
from lxml import etree

from modelset import schemas


def get_notice_url_list():
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

    try:
        page_list = ['http://jwzx.lntu.edu.cn/index/jwgg.htm']
        # page_list.extend(['http://jwzx.lntu.edu.cn/index/jwgg/{page}.htm'.format(page=i)
        #                   for i in range(1, 15)])
        notice_url_list = list(map(get_notice_url_list_from, page_list))[0]
        return notice_url_list
    except IndexError as e:
        return "教务在线通知爬虫爆炸：" + str(e)


def get_notice_detail(notice: schemas.Notice):
    def get_appendix(html_doc, notice: schemas.Notice):
        appendix_xpath = '/html/body/div[3]/form/div[1]/ul/li'
        appendix_elements = html_doc.xpath(appendix_xpath)
        for row in appendix_elements:
            name = 'http://jwzx.lntu.edu.cn/' + row.xpath('./a/@href')[0]
            url = row.xpath('./a/text()')[0]
            appendix = schemas.NoticeDetail.NoticeDetailAppendix(url=url, name=name)
            notice.appendix.append(appendix)

    xpath_str = '/html/body/div/form/div[1]'
    response = requests.get(notice.url)
    response.encoding = 'utf-8'
    html_doc = etree.HTML(response.text)
    notice_elements = html_doc.xpath(xpath_str)[0]
    notice.title = notice_elements.xpath('./div/h1/text()')[0]
    # date = notice_elements.xpath('./div/h3/text()')[1][3:]
    # notice.date = datetime.strptime(date, '%Y-%m-%d')
    notice.date = notice_elements.xpath('./div/h3/text()')[1][3:]
    notice.content = notice_elements.xpath('string(./div[@id="vsb_content"]/div)')
    if '附件' in notice.content:
        get_appendix(html_doc, notice)
    return notice


def run():
    # 通过页面获取 url 列表
    notice_url_list = get_notice_url_list()

    # 通过 url 获取详情
    notices: [schemas.Notice] = []
    for url in notice_url_list:
        notice = schemas.Notice(url=url)
        if notice.url.endswith('htm'):
            notice = get_notice_detail(notice)
            notices.append(notice)
    # print(notices)
    return notices


if __name__ == '__main__':
    run()
