from lxml import etree

# 调试时用
# os.environ["DJANGO_SETTINGS_MODULE"] = "LNTUME.settings"
# django.setup()
from spider.utils.UrlEnums import UrlEnums
from utils.utils import string_strip
from web.models import CET


def cet_get_html(session):
    url = UrlEnums.CET
    response = session.get(url)
    # 调试 Spider 时用：
    # with open("output.html", 'w+') as fp:
    #     fp.write(response.text)
    #     print("ok HTML")
    return etree.HTML(response.text)


def cet_parser(html_doc, user):
    try:
        cat_tr_elements = html_doc.xpath('/html/body/table[2]/tr')
        for cet_row in cat_tr_elements[1:]:  # 舍弃表头
            cet_td_elements = cet_row.xpath('./td')  # 拿到一行行 tr 内的 td 元素列表
            cet_data = [string_strip(i.text) for i in cet_td_elements]  # 拿到处理后的数据列表
            date = cet_data[1]
            cet = CET.objects.get_or_create(date=date, username=user)[0]
            cet.level = cet_data[0]
            cet.score = cet_data[2]
            # 调试时用
            # print(cet.__dict__)
            # for k, v in cet.__dict__.items():
            #     print(F"{k}: {v}")
            cet.save()
        return True
    except Exception as e:
        print(e)
        return False
