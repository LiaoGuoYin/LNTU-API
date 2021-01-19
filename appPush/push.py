import base64

import json
import time
from binascii import Error

import jwt
from hyper import HTTPConnection

from app.constants import constantsShared

BUNDLE_ID = constantsShared.config.bundleId
TEAM_ID = constantsShared.config.teamId
APNS_KEY_ID = constantsShared.config.keyId

f = open(constantsShared.config.keyPath)
PRIVATE_KEY = f.read()


def apple_push(title, body, device_token_list: [str]):
    token = jwt.encode(
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
        'authorization': f'bearer {token.decode("ascii")}'
    }

    payload_data = {
        'aps': {
            'alert': {
                'title': title,
                'body': body,
            },
            "badge": 0,
            'sound': "default"
        }
    }

    payload = json.dumps(payload_data).encode('utf-8')

    # Open a connection to the APN server
    conn = HTTPConnection('api.development.push.apple.com:443')

    for device_token in device_token_list:
        try:
            decrypted_device_token = base64.b64decode(device_token).hex()
        except Error:
            continue
        conn.request(
            'POST',
            f'/3/device/{decrypted_device_token}',
            payload,
            headers=request_headers
        )

        response = conn.get_response()
        print(response.__dict__)  # print to log for celery-worker
