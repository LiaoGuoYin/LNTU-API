import requests
from lxml import etree

from app import schemas, exceptions
from app.education.utils import save_html_to_file
from app.constants import constantsShared


def initialize_to_get_building_id_html(is_save=False) -> str:
    """
    初始化，获取所有教学楼 ID
    """
    url = 'http://jwzx.lntu.edu.cn/info/1086/1116.htm'
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        raise exceptions.SpiderParserException('获取教学楼列表失败')
    else:
        if is_save:
            save_html_to_file(response.text, 'class-room-building')
        return response.text


def process_building_html(html_text) -> dict:
    def parse_building_html(html_doc, xpath_str: str) -> dict:
        tmp_building_dict = {}
        building_list_row = html_doc.xpath(xpath_str)
        for building in building_list_row[1:]:
            name = ''.join(building.xpath('./td/text()')[0].split())
            url_field = building.xpath('./td/a/@href')[0].split('&')
            building_id = int(url_field[-2].split('=')[1])
            tmp_building_dict.update({name: building_id})
        return tmp_building_dict

    html_doc = etree.HTML(html_text)
    fuxin_building_dict = parse_building_html(html_doc, '//*[@id="table14"]/tbody/tr')  # 阜新校区表单：//*[@id="table14"]
    huludao_building_dict = parse_building_html(html_doc, '//*[@id="table16"]/tbody/tr')  # 葫芦岛校区表单：//*[@id="table16"]
    return {
        'fuxin': fuxin_building_dict,
        'huludao': huludao_building_dict
    }


def get_class_room_html(week: int, building_id: int, is_save=False) -> str:
    request_room_params = {
        'semesterId': constantsShared.current_semester_id,
        'iWeek': week,
        'room.building.id': building_id,
    }
    response = requests.get('http://202.199.224.119:8080/eams/classroom/occupy/class-details!unitDetail.action',
                            params=request_room_params)
    if response.status_code != 200:
        raise exceptions.SpiderParserException('获取教学楼教室失败')
    else:
        if is_save:
            save_html_to_file(response.text, 'class-room')
        return response.text


def parse_class_room_html(html_text: str) -> [schemas.Classroom]:
    html_doc = etree.HTML(html_text)
    class_room_row = html_doc.xpath('/html/body/table[2]/tr')
    room_list: [schemas.Classroom] = []
    for data in class_room_row[1:]:
        if int(data[1].text) <= 0:
            continue
        room = schemas.Classroom(
            room=data[0].text,
            capacity=data[1].text,
            type=data[2].text
        )
        mini_index_list = []
        for table_column_index in range(3, 10):
            # 处理每一行: monday, tuesday, wednesday, thursday, friday, saturday...
            room_single_day_index_list = data[table_column_index].xpath('string(.)').split()  # 每一天单个教室情况 ['3', '4']
            # 12345678910 小节课转大节课 12345
            room_single_day = map(int, filter(lambda x: int(x) % 2 != 0, room_single_day_index_list))  # 清除偶数小节课
            mini_index_tmp = list(map(lambda x: (x - (x // 2)), room_single_day))  # 大课转小课
            mini_index = list('00000')
            for i in mini_index_tmp:
                mini_index[i - 1] = '1'
            mini_index_list.append(''.join(mini_index))
        else:
            room.scheduleList = mini_index_list
            room_list.append(room)
    return room_list


def run(week, building_id) -> [schemas.Classroom]:
    html_text = get_class_room_html(week=week, building_id=building_id)
    return parse_class_room_html(html_text)


if __name__ == '__main__':
    building_id = constantsShared.building.get('eyl')
    if not building_id:
        raise exceptions.FormException("参数错误：请输入正确的教学楼")
    result = run(week=11, building_id=building_id)
    [print(i, '\n') for i in result]
