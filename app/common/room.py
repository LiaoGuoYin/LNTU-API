import re

import requests
from lxml import etree

from app import schemas
from app.education.utils import save_html_to_file


def get_building_html(is_save=False):
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


def get_class_room_html(request_room_params, is_save=False):
    '''
    :param request_room_params:
     request_room_params = {
        'semesterId': 627,
        'iWeek': 11,
        'room.building.id': 14,
        'buildingname': '耘慧楼',
    }
    :return:
    '''
    response = requests.get(
        'http://202.199.224.119:8080/eams/classroom/occupy/class-details!unitDetail.action',
        params=request_room_params)
    if response.status_code != 200:
        return '获取自习室失败'
    else:
        if is_save:
            save_html_to_file(response.text, 'class-room')
        return response.text


def parse_class_room_html(html_text: str) -> list:
    room_list = []
    html_doc = etree.HTML(html_text)
    class_room_row = html_doc.xpath('/html/body/table[2]/tr')
    for data in class_room_row[1:]:
        capacity = int(data[1].text)
        if capacity <= 0:
            continue
        room_week_str = html_doc.xpath('/html/body/table[1]/tr[2]/td')[0].text
        room_week = int(re.findall(r"第(\d+)周教室占用情况:", room_week_str)[0])
        room_name = data[0].text
        room = schemas.ClassRoom(name=room_name, week=room_week)
        room.capacity = int(data[1].text)
        room.category = data[2].text
        room.monday = data[3].xpath('string(.)').split()
        room.tuesday = data[4].xpath('string(.)').split()
        room.wednesday = data[5].xpath('string(.)').split()
        room.thursday = data[6].xpath('string(.)').split()
        room.friday = data[7].xpath('string(.)').split()
        room.saturday = data[8].xpath('string(.)').split()
        room.sunday = data[9].xpath('string(.)').split()
        print(room)
        room_list.append(room)
    return room_list


def run(room_params):
    html_text = get_class_room_html(room_params)
    parse_class_room_html(html_text)


if __name__ == '__main__':
    building_dict = {'fuxin': {'博文楼': 7, '博雅楼': 13, '新华楼': 19, '中和楼': 17, '致远楼': 18, '知行楼': 8, '物理实验室': 15, '主楼机房': 9},
                     'huludao': {'尔雅楼': 20, '静远楼': 11, '葫芦岛物理实验室': 16, '葫芦岛机房': 21, '耘慧楼': 14}}
    request_room_params = {
        'semesterId': 627,
        'iWeek': 11,
        'room.building.id': 14,
        'buildingname': '耘慧楼',
    }
    run(request_room_params)
