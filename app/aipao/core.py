import datetime
from random import uniform, randint

import requests

from app import exceptions, schemas
from app.aipao.url import AIPAOURLEnum


def check_imei_code(code: str) -> schemas.AiPaoUser:
    url = AIPAOURLEnum.CHECK_IMEI_CODE_URL.value
    response = requests.get(url, params={'IMEICode': code})
    user = schemas.AiPaoUser(id=-1, code=code)
    if response.json()['Success']:
        user.isCodeValid = True
        # Invalid: {'Success': False, 'ErrCode': 7, 'Errmessage': '验证码过期'}
        # Valid:{'Success': True, 'Data': {'Token': 'b1b884347188409ea273c02072f9d551', 'UserId': 699560, 'IMEICode': 'd584b33e9a3e484da5e13eb38e73fc24', 'AndroidVer': 2.4, 'AppleVer': 1.24, 'WinVer': 1.0}}
        user.token = response.json()['Data']['Token']
        user.id = response.json()['Data']['UserId']
        user.failureCount = get_record(user.id, is_valid=False)['AllCount']
        success_response = get_record(user.id, is_valid=True)
        user.successCount = success_response['AllCount']
        user.isDoneToday = check_is_done_today_with_record_list(record_list=success_response.get('listValue'))
        get_basic_info_with_token(user, user.token)
    else:
        pass
    return user


def get_basic_info_with_token(user: schemas.AiPaoUser, token: str):
    url = AIPAOURLEnum.GET_STU_REGULATION_URL.value.replace('{token}', token)
    response = requests.get(url)
    if response.json()['Success']:
        response_json = response.json()
        user.name = response_json['Data']['User']['NickName']
        user.gender = response_json['Data']['User']['Sex']
        user.schoolName = response_json['Data']['SchoolRun']['SchoolName']


def check_is_done_today_with_record_list(record_list: list) -> bool:
    if not record_list:
        return False
    latest_run_date = record_list[0].get('ResultDate')
    today_date = datetime.date.today().strftime('%Y年%m月%d日')
    if today_date != latest_run_date:
        return False
    else:
        return True


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
    record_result = response.json()
    if record_result['Success'] and is_valid:
        record_result['isDoneToday'] = check_is_done_today_with_record_list(record_result['listValue'])
    return record_result


def run_sunny(imei_code: str) -> dict:
    # Checking the status of IMEICode
    token = check_imei_code(code=imei_code).token
    if token == '':
        raise exceptions.FormException("IMEICode 无效")

    # Getting basic user info
    client = AiPaoClient(token=token)
    if not client.get_info():
        raise exceptions.SpiderParserException("获取个人跑步规则信息失败")
    if client.get_run_id() == '':
        raise exceptions.SpiderParserException("开始跑步失败")

    # Uploading the final record
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
        self.gender = ''

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
                self.userId = response_json['Data']['User']['UserID']
                self.gender = response_json['Data']['User']['Sex']
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
