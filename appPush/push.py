import base64

import json
import time
from binascii import Error

import jwt
from hyper import HTTPConnection

from app import schemas
from app.constants import constantsShared

BUNDLE_ID = constantsShared.config.bundleId
TEAM_ID = constantsShared.config.teamId
APNS_KEY_ID = constantsShared.config.keyId

f = open(constantsShared.config.keyPath)
PRIVATE_KEY = f.read()


def apple_push(category: schemas.NotificationSubscriptionEnum, body: str, device_token: str):
    if category == schemas.NotificationSubscriptionEnum.GRADE:
        title = '出新成绩啦!'
    elif category == schemas.NotificationSubscriptionEnum.NOTICE:
        title = '教务在线发新通知啦!'
    else:
        title = '有新通知啦!'

    request_token = jwt.encode(
        {
            'iss': TEAM_ID,
            'iat': time.time()
        },
        PRIVATE_KEY,
        algorithm='ES256',
        headers={
            'alg': 'ES256',
            'kid': APNS_KEY_ID,
        }
    )

    request_headers = {
        'apns-expiration': '0',
        'apns-priority': '10',
        'apns-topic': BUNDLE_ID,
        'authorization': f'bearer {request_token.decode("ascii")}'
    }

    payload_data = {
        'aps': {
            'alert': {
                'title': title,
                'body': body,
            },
            "badge": 0,
            'sound': "default",
            "category": category.value
        }
    }
    payload = json.dumps(payload_data).encode('utf-8')

    # Open a connection to the APN server
    conn = HTTPConnection('api.development.push.apple.com:443')

    try:
        decrypted_device_token = base64.b64decode(device_token).hex()
        conn.request(
            'POST',
            f'/3/device/{decrypted_device_token}',
            payload,
            headers=request_headers
        )
    except Error:
        # 设备号可能错误
        pass

    response = conn.get_response()
    print(response.__dict__)
