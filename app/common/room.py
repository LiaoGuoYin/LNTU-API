import re

import requests
from lxml import etree

from app import schemas, exceptions
from app.education.utils import save_html_to_file


def get_building_html(is_save=False) -> str:
    url = 'http://jwzx.lntu.edu.cn/info/1086/1116.htm'
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        return "获取教学楼列表失败"
    else:
        if is_save:
            save_html_to_file(response.text, 'class-room-building')
        return response.text


def process_building_html(html_text) -> dict:
    building_dict = {}
    html_doc = etree.HTML(html_text)
    fuxin_building_dict = parse_building_html(html_doc, '//*[@id="table14"]/tbody/tr')  # 阜新校区表单：//*[@id="table14"]
    huludao_building_dict = parse_building_html(html_doc, '//*[@id="table16"]/tbody/tr')  # 葫芦岛校区表单：//*[@id="table16"]
    building_dict.update({
        'fuxin': fuxin_building_dict,
        'huludao': huludao_building_dict
    })
    return building_dict


def parse_building_html(html_doc, xpath_str: str) -> dict:
    tmp_building_dict = {}
    building_list_row = html_doc.xpath(xpath_str)
    for building in building_list_row[1:]:
        name = ''.join(building.xpath('./td/text()')[0].split())
        url_field = building.xpath('./td/a/@href')[0].split('&')
        building_id = int(url_field[-2].split('=')[1])
        tmp_building_dict.update({name: building_id})
    return tmp_building_dict


def get_class_room_html(week: int, building_id: int, is_save=False) -> str:
    request_room_params = {
        'semesterId': 627,
        'iWeek': week,
        'room.building.id': building_id,
        # 'buildingname': '耘慧楼',
    }
    response = requests.get(
        'http://202.199.224.119:8080/eams/classroom/occupy/class-details!unitDetail.action',
        params=request_room_params)
    if response.status_code != 200:
        return '获取自习室失败'
    else:
        if is_save:
            save_html_to_file(response.text, 'class-room')
        return response.text


def parse_class_room_html(html_text: str) -> [schemas.ClassRoom]:
    room_list: [schemas.ClassRoom] = []
    html_doc = etree.HTML(html_text)
    class_room_row = html_doc.xpath('/html/body/table[2]/tr')
    for data in class_room_row[1:]:
        capacity = int(data[1].text)
        if capacity <= 0:
            continue
        room_week_str = html_doc.xpath('/html/body/table[1]/tr[2]/td')[0].text
        room_week = int(re.findall(r"第(\d+)周教室占用情况:", room_week_str)[0])
        room = schemas.ClassRoom(
            address=data[0].text,
            num=int(data[1].text),
            type=data[2].text
        )
        mini_index_list = []
        for i in range(3, 10):
            # monday, tuesday, wednesday, thursday, friday, saturday...
            room_single_day_index_list = data[i].xpath('string(.)').split()  # 每一天单个教室情况 ['3', '4']
            # 12345678910 小节课转大节课 12345
            room_single_day = filter(lambda x: int(x) % 2 != 0, room_single_day_index_list)  # 清除偶数小节课
            mini_index_tmp = list(map(lambda x: (int(x) - (int(x) // 2)), room_single_day))  # 大课转小课
            index_dict = dict(zip(list('12345'), list('abcde')))
            mini_index = schemas.ClassRoom.MiniIndex()
            for j in mini_index_tmp:
                setattr(mini_index, index_dict.get(str(j)), 1)
            mini_index_list.append(mini_index)
        room.data = mini_index_list
        room_list.append(room)
    return room_list


def run(week, building_name) -> [schemas.ClassRoom]:
    building_id = building_dict.get(building_name)
    if not building_id:
        raise exceptions.FormException("参数错误：请输入正确的教学楼")

    html_text = get_class_room_html(
        week=week,
        building_id=building_id
    )
    return parse_class_room_html(html_text)


# building_dict = {'fuxin': {'博文楼': 7, '博雅楼': 13, '新华楼': 19, '中和楼': 17, '致远楼': 18, '知行楼': 8, '物理实验室': 15, '主楼机房': 9},
#                  'huludao': {'尔雅楼': 20, '静远楼': 11, '葫芦岛物理实验室': 16, '葫芦岛机房': 21, '耘慧楼': 14}}

building_dict = {'eyl': 20, 'jyl': 11, 'hldwlsys': 16, 'hldjf': 21, 'yhl': 14, 'bwl': 7, 'byl': 13, 'xhl': 19,
                 'zhl': 17, 'zyl': 18, 'zxl': 8, 'wlsys': 15, 'zljf': 9}

if __name__ == '__main__':
    print(run(week=1, building_name='yhl'))
