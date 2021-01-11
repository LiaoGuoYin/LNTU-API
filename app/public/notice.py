import requests
from lxml import etree

from app import schemas, exceptions


def get_notice_url_list_from(page_url: str = 'https://jwzx.lntu.edu.cn/index/jwgg.htm') -> [schemas.Notice]:
    try:
        url_list = []
        response = requests.get(page_url, timeout=(1, 3))
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
    except (requests.exceptions.RequestException, requests.exceptions.RequestException) as e:
        raise exceptions.NetworkException(f'教务在线通知爬虫爆炸：{e}')
    return url_list


if __name__ == '__main__':
    page_list = ['https://jwzx.lntu.edu.cn/index/jwgg.htm']
    # page_list.extend(['http://jwzx.lntu.edu.cn/index/jwgg/{page}.htm'.format(page=i)
    #                   for i in range(1, 55)])
    for page in page_list:
        notice_list = get_notice_url_list_from(page)
        print(notice_list)
