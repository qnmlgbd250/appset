# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json

import time
import hmac
import hashlib
import base64
import urllib.parse


def send_dingding(msg):
    timestamp = str(round(time.time() * 1000))
    secret = os.environ.get('DD_BOT_SECRET')
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url2 = F'https://oapi.dingtalk.com/robot/send?access_token={os.environ.get("DD_BOT_TOKEN")}&timestamp={timestamp}&sign={sign}'
    data = {
        "at": {
            "atMobiles": [
                ""
            ],
            "atUserIds": [
                ""
            ],
            "isAtAll": False
        },
        "text": {
            "content": msg
        },
        "msgtype": "text"
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url2, data=json.dumps(data), headers=headers).json()
    if response['errcode'] == 0:
        print('钉钉群消息通知成功')
    else:
        print(f'发送失败{response}')


#send_dingding('测试')

