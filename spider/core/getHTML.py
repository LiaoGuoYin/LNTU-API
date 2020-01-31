from lxml import etree


def get_html_doc(session, url, **kwargs):
    response = session.get(url, **kwargs)
    html_doc = etree.HTML(response.text)
    return html_doc


def score_get_html_doc(session, url):
    """special html structure"""
    response = session.get(url)
    html = response.text.replace('<font color="#CC0000">', '').replace('</font>', '').replace(
        '<a target="_blank" href="', '').replace('">打印</a>', '')  # 破坏指定元素的结构，方便有效率地统一提取
    # 调试 Spider 时用：
    # with open("output.html", 'w+') as fp:
    #     fp.write(response.text)
    #     print("ok HTML")
    return etree.HTML(html)
