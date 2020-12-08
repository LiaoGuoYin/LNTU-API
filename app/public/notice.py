import requests
from lxml import etree

from app import schemas, exceptions


def get_notice_url_list_from(page_url: str = 'https://jwzx.lntu.edu.cn/index/jwgg.htm') -> [schemas.Notice]:
    try:
        url_list = []
        response = requests.get(page_url)
        response.encoding = 'utf-8'
        html_doc = etree.HTML(response.text)
        ul_list = html_doc.xpath('/html/body/div[3]/div[2]/div[2]/ul/li')
        for row in ul_list:
            title = row.xpath("./a/em/text()")[0]
            date = row.xpath("./a/span/text()")[0]
            url_origin = row.xpath("./a/@href")[0]
            url = ('https://jwzx.lntu.edu.cn/index/' + url_origin) if url_origin.startswith('..') else url_origin
            notice_data_row = schemas.Notice(url=url, title=title, date=date)
            url_list.append(notice_data_row)
    except (requests.exceptions.RequestException, requests.exceptions.RequestException,
            exceptions.NetworkException) as e:
        raise exceptions.AccessException(f'教务在线通知爬虫爆炸：{e}')
    return url_list


# def get_notice_detail(notice: schemas.Notice) -> schemas.Notice:
#     class NoticeDetail(BaseModel):
#         class NoticeDetailAppendix(BaseModel):
#             url: str
#             name: str
#
#         title: str = None
#         date: str = None
#         content: str = None
#         appendix: List[NoticeDetailAppendix] = []
#
#
#     class Notice(NoticeDetail):
#         url: str
#
#     def get_appendix(ori_html_doc, ori_notice: schemas.Notice):
#         appendix_xpath = '/html/body/div[3]/form/div[1]/ul/li'
#         appendix_elements = ori_html_doc.xpath(appendix_xpath)
#         for row in appendix_elements:
#             name = 'http://jwzx.lntu.edu.cn/' + row.xpath('./a/@href')[0]
#             url = row.xpath('./a/text()')[0]
#             appendix = schemas.NoticeDetail.NoticeDetailAppendix(url=url, name=name)
#             ori_notice.appendix.append(appendix)
#
#     xpath_str = '/html/body/div/form/div[1]'
#     response = requests.get(notice.url)
#     response.encoding = 'utf-8'
#     html_doc = etree.HTML(response.text)
#     notice_elements = html_doc.xpath(xpath_str)[0]
#     notice.title = notice_elements.xpath('./div/h1/text()')[0]
#     notice.date = notice_elements.xpath('./div/h3/text()')[1][3:]
#     notice.content = notice_elements.xpath('string(./div[@id="vsb_content"]/div)')
#     if '附件' in notice.content:
#         get_appendix(html_doc, notice)
#     return notice


if __name__ == '__main__':
    page_list = ['https://jwzx.lntu.edu.cn/index/jwgg.htm']
    # page_list.extend(['http://jwzx.lntu.edu.cn/index/jwgg/{page}.htm'.format(page=i)
    #                   for i in range(1, 55)])
    for page in page_list:
        notice_list = get_notice_url_list_from(page)
        print(notice_list)
