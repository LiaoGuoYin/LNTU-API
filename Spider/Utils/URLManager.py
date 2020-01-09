import requests
from lxml import etree

edu_url = 'http://jwzx.lntu.edu.cn/'

# 教务通告
notice_url = 'http://jwzx.lntu.edu.cn/index/jwgg.htm'

# 校历
campus_calendar_url = 'http://jwzx.lntu.edu.cn/index/xl.htm'

# 查询空教室
classroom_status_url = 'http://jwzx.lntu.edu.cn/info/1086/1116.htm'


# 外网登陆
# http://202.199.224.24:11189/academic/common/security/login.jsp
# http://202.199.224.24:11089/newacademic/common/security/login.jsp
# /html/body/div[3]/div[2]/div[1]/div[1]/div/p[1]/a/@href
# outer_urls = []

# 内网登陆
# http://10.21.24.120:11089/newacademic/common/security/login.jsp
# /html/body/div[3]/div[2]/div[1]/div[1]/div/p[2]/a/@href
# inner_urls = []

# 选课入口
# /html/body/div[3]/div[2]/div[1]/div[1]/div/p[3]/a/@href
# http://202.199.224.24:11189/academic/student/selectcourse/
# select_urls = []

# 教师登陆
# /html/body/div[3]/div[2]/div[1]/div[1]/div/p[4]/a/@href
# http://202.199.224.121:11080/newacademic/common/security/login.jsp
# http://202.199.224.121:11180/newacademic/common/security/login.jsp
# teacher_urls = []


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

        print(self.__dict__)


client = URLManager()
client.freshURLS()
