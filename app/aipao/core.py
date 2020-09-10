from random import uniform, randint

import requests

from app import exceptions
from app.aipao.url import AIPAOURLEnum


def check_imei_code(code: str) -> dict:
    data_result = {}
    url = AIPAOURLEnum.CHECK_IMEI_CODE_URL.value
    params = {
        'IMEICode': code
    }
    response = requests.get(url, params=params)
    if response.json()['Success']:
        # Invalid: {'Success': False, 'ErrCode': 7, 'ErrMsg': '验证码过期'}
        # Valid:{'Success': True, 'Data': {'Token': 'b1b884347188409ea273c02072f9d551', 'UserId': 699560, 'IMEICode': 'd584b33e9a3e484da5e13eb38e73fc24', 'AndroidVer': 2.4, 'AppleVer': 1.24, 'WinVer': 1.0}}
        data_result = {
            'token': response.json()['Data']['Token'],
            'id': response.json()['Data']['UserId'],
            'code': response.json()['Data']['IMEICode'],
        }
        data_result['validCount'] = get_record(data_result['id'], is_valid=True)['AllCount']
        data_result['inValidCount'] = get_record(data_result['id'], is_valid=False)['AllCount']
    if not len(data_result):
        raise exceptions.FormException("IMEICode 无效")
    return data_result


def get_record(user_id: int, page: int = 1, offsets: int = 10, is_valid: bool = True) -> dict:
    record_result = {}
    if is_valid:
        url = AIPAOURLEnum.VALID_URL.value
    else:
        url = AIPAOURLEnum.INVALID_URL.value
    params = {
        'UserId': user_id,
        'pageIndex': page,
        'pageSize': offsets
    }
    response = requests.get(url, params=params)
    response_data = response.json()
    if response_data['Success']:
        record_result = response_data
    return record_result


def run_sunny(imei_code: str) -> dict:
    data_dict = check_imei_code(code=imei_code)
    if not len(data_dict):
        raise exceptions.FormException("IMEICode 无效")
    token = data_dict['token']

    client = AiPaoClient(token=token)
    if not client.get_info():
        raise exceptions.SpiderParserException("获取个人跑步规则信息失败")
    if not client.get_run_id():
        raise exceptions.SpiderParserException("开始跑步失败")

    run_response = client.upload_record()
    if not run_response:
        raise exceptions.SpiderParserException("结束跑步失败（上传成绩失败）")
    run_response['uploaded'] = client
    return run_response


class AiPaoClient(object):
    def __init__(self, token):
        self.token = token
        self.userName = ''
        self.userId = ''
        self.schoolName = ''
        self.runId = ''
        self.distance = 2400
        self.minSpeed = 2.0
        self.maxSpeed = 3.0

    def __str__(self):
        return str(self.__dict__).replace('\"', '\'')

    def get_info(self) -> bool:
        token = self.token

        url: str = AIPAOURLEnum.GET_STU_REGULATION_URL.value.replace('{token}', token)
        response = requests.get(url)
        try:
            if response.json()['Success']:
                response_json = response.json()
                self.userName = response_json['Data']['User']['NickName']
                self.schoolName = response_json['Data']['SchoolRun']['SchoolName']
                self.minSpeed = response_json['Data']['SchoolRun']['MinSpeed']
                self.maxSpeed = response_json['Data']['SchoolRun']['MaxSpeed']
                self.distance = response_json['Data']['SchoolRun']['Lengths']
                return True
        except KeyError:
            return False

    def get_run_id(self) -> str:
        token = self.token
        distance = self.distance

        url = AIPAOURLEnum.START_RUN_URL.value.replace('{token}', token)
        params = {
            'S1': '40.62828',
            'S2': '120.79108',
            'S3': distance
        }
        response = requests.get(url, params=params)
        try:
            if response.json()['Success']:
                self.runId = response.json()['Data']['RunId']
                return response.json()['Data']['RunId']
            else:
                return ''
        except KeyError:
            return ''

    def upload_record(self) -> dict:
        def encrypt(number):
            key = 'xfvdmyirsg'
            numbers = list(map(int, list(str(number))))
            return_key = ''.join([key[i] for i in numbers])
            return return_key

        token = self.token
        distance = self.distance
        run_id = self.runId
        min_speed = self.minSpeed
        max_speed = self.maxSpeed

        url = AIPAOURLEnum.FINISHED_RUN_URL.value.replace('{token}', token)
        speed = round(uniform(min_speed + 0.3, max_speed - 0.5), 2)
        distance = distance + randint(1, 5)
        cost_time = int(distance // speed)
        step = randint(1555, 2222)
        params = {
            'S1': run_id,
            'S4': encrypt(cost_time),
            'S5': encrypt(distance),
            'S6': 'A0A2A1A3A0',
            'S7': '1',
            'S8': 'xfvdmyirsg',
            'S9': encrypt(step)
        }
        response = requests.get(url, params=params)
        return response.json()
