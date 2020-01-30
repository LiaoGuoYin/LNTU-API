import requests
from lxml import etree

# os.environ["DJANGO_SETTINGS_MODULE"] = "LNTUME.settings"
# django.setup()
from web.models import ClassRoom


def classroom_fresh(room_data):
    try:
        response = requests.get(
            "http://202.199.224.121:11180/newacademic/manager/teachresource/schedule/export_room_schedule_detail.jsp",
            params=room_data)
        html_doc = etree.HTML(response.text)
        classrooms = html_doc.xpath('/html/body/center/div/table/tr')
        for each in classrooms[1:]:  # 舍弃表头
            info_elements = each.xpath('./td')
            results = ["".join(td.text.split()) for td in info_elements]
            capacity = results[1]
            if capacity == "0":
                continue
            room_name = results[0]
            room = ClassRoom.objects.get_or_create(name=room_name)[0]
            room.buildingId = room_data['buildingid1']
            room.week = room_data['weeks']
            room.capacity = results[1]
            room.category = results[2]
            room.monday = results[3]
            room.tuesday = results[4]
            room.wednesday = results[5]
            room.thursday = results[6]
            room.friday = results[7]
            room.saturday = results[8]
            room.sunday = results[9]
            room.save()
        return True
    except Exception as e:
        print(e.with_traceback())
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
