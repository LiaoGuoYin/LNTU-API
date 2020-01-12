from urllib.parse import urlencode

import requests
from lxml import etree

URL_ROOT = 'http://s2.natfrp.com:7792/academic/'


def is_all_evaluate(html_doc):
    evaluate_statuses = html_doc.xpath('/html/body/center/table[2]/tr/td[3]/span')
    status = [each.text for each in evaluate_statuses if each.text != '已评估']
    if len(status) == 0:
        return True
    else:
        return False


def evaluate_form(cookie, url):
    response = requests.get(url, headers={'Cookie': cookie})
    html_doc = etree.HTML(response.text)
    data_lists = []
    input_xpath = '/html/body/center/table[2]/tr/td/form/input'
    input_datas = html_doc.xpath(input_xpath)
    for each in input_datas:
        name = each.xpath('@name')[0]
        value = each.xpath('@value')[0]
        data_lists.append(urlencode({name: value}))
    evaluate_xpath = '/html/body/center/table[2]/tr/td/form/table[1]/tr/td[3]'
    evaluate_result = html_doc.xpath(evaluate_xpath)
    for each in evaluate_result:
        inputs = each.xpath('input')
        for i in inputs[:5]:
            name = i.xpath('@name')[0]
            value = i.xpath('@value')[0]
            data_lists.append(urlencode({name: value}))
    return '&'.join(data_lists)


def evaluate(cookie, form_data):
    url = URL_ROOT + 'eva/index/putresult.jsdo'
    headers = {'Cookie': cookie, 'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=form_data, headers=headers)
    if response.status_code == 200:
        print("评课完成")
    # print(response.request.headers)
    # print(response.headers)
    # print(response.text)


def run(cookie):
    url = URL_ROOT + 'eva/index/resultlist.jsdo'
    response = requests.get(url, headers={"Cookie": cookie})
    html_doc = etree.HTML(response.text)
    if is_all_evaluate(html_doc):
        print("已经完成评课！")
    else:
        print("尚未完成，不能查成绩，马上开始评课...")
        evaluate_elements = html_doc.xpath('/html/body/center/table[2]/tr/td[4]/a/@href')
        evaluate_urls = [URL_ROOT + 'eva/index/' + each for each in evaluate_elements]
        print(evaluate_urls)
        for url in evaluate_urls:
            form_data = evaluate_form(cookie, url)
            evaluate(cookie, form_data)

# run("JSESSIONID=913241AB7DA3B204760EED3A2D205CC4.T55; Path=/academic")
