from time import sleep

import requests
from lxml import etree


class URLManager(object):
    outer_urls = None
    inner_urls = None
    selectCourse_urls = None
    teacher_urls = None

    def __init__(self):
        pass

    def freshURLS(self):
        JWZX_URL = 'http://jwzx.lntu.edu.cn/'
        response = requests.get(JWZX_URL)
        html_doc = etree.HTML(response.text)

        student_xpath_inner = '/html/body/div[3]/div[2]/div[1]/div[1]/div/p[2]/a/@href'
        student_xpath_outer = '/html/body/div[3]/div[2]/div[1]/div[1]/div/p[1]/a/@href'
        selectCourse_xpath = '/html/body/div[3]/div[2]/div[1]/div[1]/div/p[3]/a/@href'
        teacher_xpath_outer = '/html/body/div[3]/div[2]/div[1]/div[1]/div/p[4]/a/@href'

        self.outer_urls = html_doc.xpath(student_xpath_outer)
        self.inner_urls = html_doc.xpath(student_xpath_inner)
        self.selectCourse_urls = html_doc.xpath(selectCourse_xpath)
        self.teacher_urls = html_doc.xpath(teacher_xpath_outer)

        return self.outer_urls


def ping(urls):
    for url in urls:
        try:
            response = requests.head(url, timeout=(0.1, 2))
            if response.status_code == 200:
                form_data = "url: {}, <br>delay: {}ms".format(url, response.elapsed.total_seconds() * 1000)

                print(form_data)
                # requests.post(
                #     url="https://sc.ftqq.com/SCU35195T397c1fd31ef693c6b5f6230d608a877c5e020dea74197.send?text=教务在线外网复活了{}".format(
                #         url.split(":")[2].encode("UTF-8")),
                #     data={"desp": form_data})
        except Exception as e:
            pass
            # print(e)


def main():
    URL_ROOT = "http://202.199.224.24"
    ports = [11080, 11081, 11180, 11181, 11182, 11189, 11089]
    uris = ["/newacademic/", "/academic/"]
    urls = ["{URL_ROOT}:{port}{uri}".format(URL_ROOT=URL_ROOT, port=str(port), uri=uri)
            for port in ports
            for uri in uris
            ]

    # URI = "/academic/client/default/image/login_sub1.gif"
    # URI = "/newacademic/client/default/image/login_sub1.gif"

    while True:
        client = URLManager()
        spider_urls = client.freshURLS()
        urls.extend(spider_urls)
        print(urls)
        ping(urls)
        sleep(100)


if __name__ == "__main__":
    main()
