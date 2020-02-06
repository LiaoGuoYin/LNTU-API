from enum import Enum, unique

import requests
from lxml import etree


@unique
class UrlEnums(Enum):
    URL_ROOT = "http://202.199.224.24:11189/academic/"
    # URL_ROOT = "http://202.199.224.24:11089/newacademic/"

    # private urls
    LOGIN = URL_ROOT + "j_acegi_security_check"
    STUDENT_INFO = URL_ROOT + "student/studentinfo/studentinfo.jsdo"
    TEACHING_PLAN = URL_ROOT + "student/studyschedule/"
    TEACHING_PLAN_IDS = URL_ROOT + "student/studyschedule/studyschedule.jsdo"
    CLASS_TABLE = URL_ROOT + "student/currcourse/currcourse.jsdo"
    TEACHER_EVALUATE_QUERY = URL_ROOT + "eva/index/resultlist.jsdo"
    TEACHER_EVALUATE = URL_ROOT + "eva/index/putresult.jsdo"
    EXAM_PLAN = URL_ROOT + "student/exam/index.jsdo"
    SCORE = URL_ROOT + "student/queryscore/queryscore.jsdo"
    UN_PASS = URL_ROOT + "student/unpasscourse/unpasscourse.jsdo"
    SCORES_DETAIL = URL_ROOT + "student/queryscore/"
    CET = URL_ROOT + "student/queryscore/skilltestscore.jsdo"
    EDU_PLAN = URL_ROOT + "student/studyschedule/studyschedule_view_byterm.jsdo?studentId=2884962&classId=11611"  # TODO 参数

    # public urls
    EDU_URL = 'http://jwzx.lntu.edu.cn/'
    NOTICE_URL = 'http://jwzx.lntu.edu.cn/index/jwgg.htm'  # 教务通告
    CAMPUS_CALENDAR_URL = 'http://jwzx.lntu.edu.cn/index/xl.htm'  # 校历
    CLASSROOM_STATUS_URL = 'http://jwzx.lntu.edu.cn/info/1086/1116.htm'  # 查询空教室

    def __str__(self):
        return self.value

    # for name, member in UrlEnums.__members__.items():
    #     print(name.lower(), member.value)
    # # print(list(UrlEnums))


class URLManager(object):

    @staticmethod
    def get_all_urls(url_dicts: dict):
        try:
            response = requests.get(UrlEnums.EDU_URL)
            html_doc = etree.HTML(response.text)
            p_elements = html_doc.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div/p')
            data = [each.xpath('a/@href') for each in p_elements]
            url_dicts['outer_urls'] = data[0]
            url_dicts['inner_urls'] = data[1]
            url_dicts['select_course_urls'] = data[2]
            url_dicts['teacher_urls'] = data[3]
        except requests.RequestException as e:
            print(F"请求错误: {e}")
        except IndexError as e:
            print(F"官网爆炸，抓不到: {e}")
        return url_dicts

    @staticmethod
    def ping(url):
        try:
            response = requests.head(url, timeout=(0.1, 2))
            cost_ms = response.elapsed.total_seconds() * 1000
            # print(F"{url} - {cost_ms}ms")
            return cost_ms
        except requests.ConnectionError:
            # print("timeout{} {url}".format("!!!!!!!!!!!!!!" * 5, url=url))
            return 99999


def run():
    url_dicts = URLManager.get_all_urls({})
    # url_dicts.pop("teacher_urls")
    # url_dicts.pop("select_course_urls")
    # url_dicts.pop("inner_urls")
    url_lists = url_dicts["outer_urls"]
    result_lists = []

    # test 3 times
    for url in url_lists[:2]:
        ms_lists = []
        while len(ms_lists) < 3:
            ms_lists.append(URLManager.ping(url))
        result_lists.append([sum(ms_lists) / len(ms_lists), url])
    result_lists.sort(key=lambda x: x[0])
    print(F"{result_lists}")
    return result_lists[0][1].split("common/security/login.jsp")[0]


if __name__ == "__main__":
    print(run())
