import json
import time
import jwt
from hyper import HTTPConnection

from app.constants import constantsShared

BUNDLE_ID = constantsShared.config.bundleId
TEAM_ID = constantsShared.config.teamId
APNS_KEY_ID = constantsShared.config.keyId

f = open(constantsShared.config.keyPath)
PRIVATE_KEY = f.read()


def apple_push(content: str, device_token_list: [str]):
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
            'alert': content,
            "badge": 0,
            'sound': "default"
        }
    }

    payload = json.dumps(payload_data).encode('utf-8')

    # Open a connection to the APN server
    conn = HTTPConnection('api.development.push.apple.com:443')

    for device_token in device_token_list:
        conn.request(
            'POST',
            f'/3/device/{device_token}',
            payload,
            headers=request_headers
        )

        response = conn.get_response()
        print(response.__dict__)  # Display for celery worker
