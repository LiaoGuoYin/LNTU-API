from spider.utils.utils import string_strip


def detail_parser(html_doc, score):
    try:
        detail_element = html_doc.xpath('/html/body/center/table')[0]
        score.made_up_of = string_strip(detail_element.xpath('./tr[5]/td/p/b')[0].text)
        score.daily_score = string_strip(detail_element.xpath('./tr[7]/td[1]/b')[0].text)
        score.midterm_score = string_strip(detail_element.xpath('./tr[7]/td[2]/b')[0].text)
        score.exam_score = string_strip(detail_element.xpath('./tr[7]/td[3]/b')[0].text)
        score.final_score = string_strip(detail_element.xpath('./tr[7]/td[4]/b')[0].text)
        score.save()
        return True
    except IndexError:
        print(F"{score.name} 成绩有缺失")
    except Exception as e:
        print(e)
        return False
