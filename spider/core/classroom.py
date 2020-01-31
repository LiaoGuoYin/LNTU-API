import requests
from lxml import etree

from utils.utils import string_strip
from web.models import ClassRoom


def classroom_fresh(room_data):
    try:
        response = requests.get(
            "http://202.199.224.121:11180/newacademic/manager/teachresource/schedule/export_room_schedule_detail.jsp",
            params=room_data)
        html_doc = etree.HTML(response.text)
        classroom_tr_elements = html_doc.xpath('/html/body/center/div/table/tr')
        for classroom_row in classroom_tr_elements[1:]:
            classroom_td_elements = classroom_row.xpath('./td')
            data = [string_strip(i.text) for i in classroom_td_elements]
            capacity = data[1]
            if capacity == "0":
                continue
            room_name = data[0]
            room = ClassRoom.objects.get_or_create(name=room_name)[0]
            room.buildingId = room_data['buildingid1']
            room.week = room_data['weeks']
            room.capacity = data[1]
            room.category = data[2]
            room.monday = data[3]
            room.tuesday = data[4]
            room.wednesday = data[5]
            room.thursday = data[6]
            room.friday = data[7]
            room.saturday = data[8]
            room.sunday = data[9]
            room.save()
        return True
    except Exception as e:
        print(e)
        return False


buildings = [
    [{'buildingid1': '4', 'buildingname': '新华楼'},
     {'buildingid1': '5', 'buildingname': '博雅楼'},
     {'buildingid1': '8', 'buildingname': '主楼机房'},
     {'buildingid1': '10', 'buildingname': '物理实验室'},
     {'buildingid1': '12', 'buildingname': 'null'},
     {'buildingid1': '15', 'buildingname': '育龙主楼'},
     {'buildingid1': '16', 'buildingname': 'null'},
     {'buildingid1': '1913', 'buildingname': 'null'}],
    [{'buildingid1': '6', 'buildingname': '尔雅楼'},
     {'buildingid1': '7', 'buildingname': '耘慧楼'},
     {'buildingid1': '9', 'buildingname': '葫芦岛机房'},
     {'buildingid1': '11', 'buildingname': '葫芦岛物理实验室'},
     {'buildingid1': '14', 'buildingname': '静远楼'}]
]
