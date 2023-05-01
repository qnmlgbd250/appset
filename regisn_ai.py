import re
import random
import time
import redis
import os
import requests
import base64
import ddddocr
import json
import string
from requests.utils import dict_from_cookiejar
from dotenv import load_dotenv

load_dotenv(".env")
redis_pool = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))
proxies = {
  'http': 'http://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068',
  # 'https': 'https://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068'
}

session = requests.Session()
session1 = requests.Session()
email_af = ['nqmo.com', 'qabq.com']



for _ in range(200):
    try:

        email_af_str = random.choice(email_af)
        letters = string.ascii_lowercase
        email_be = ''.join(random.choice(letters) for i in range(7))
        email = f"{email_be}@{email_af_str}"
        print(email)



        # 获取验证码
        s = session.get('https://usesless.casdoor.com/signup/usesless.com')

        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://usesless.casdoor.com/signup/usesless.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",

        }

        url = "https://usesless.casdoor.com/api/get-captcha"
        params = {
            "applicationId": "admin/usesless.com",
            "isCurrentProvider": "false"
        }
        response = session.get(url, headers=headers, params=params,proxies=proxies)

        img = response.json().get("data").get("captchaImage")
        caid = response.json().get("data").get("captchaId")

        # 调用dddd识别验证码
        ocr = ddddocr.DdddOcr(show_ad=False)
        image_bytes = base64.b64decode(img)
        res = requests.post("http://106.12.127.131:9898/ocr/file", files={'image': image_bytes}).text

        # res = ocr.classification(image_bytes)
        print(res)
        if len(res) != 5:
            continue

        # 开始注册
        # 验证图像验证码

        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryU5tBOVFTuA69TWF5",
            "Origin": "https://usesless.casdoor.com",
            "Referer": "https://usesless.casdoor.com/signup/usesless.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
        }

        url = "https://usesless.casdoor.com/api/send-verification-code"

        files = {
        'checkType': (None, "Default"), # 当前时间戳
        'captchaToken': (None, res),
        'clientSecret':  (None, caid),
        'method': (None, "signup"),
        'countryCode': (None, ''),
        'dest': (None, email),
        'type': (None, "email"),
        'applicationId': (None, "admin/usesless.com"),
        'checkUser': (None, ""),

    }

        response = session.post(url, headers=headers, files=files,proxies=proxies)

        print(response.text)

        if 'you can only send one code in 60s' in str(response.text):
            print('邮箱发送频繁，等待60s')
            time.sleep(30)
            continue
        if '未发送' in str(response.text):
            time.sleep(10)
            print('发送验证码失败')
            continue
        if '缺少参数' in str(response.text):
            print('发送验证码失败')
            continue

        # 刷新邮件
        time.sleep(3)

        response = session1.get('https://mail.cx/zh/')

        # 获取响应中的cookie字典
        cookie_dict = dict_from_cookiejar(response.cookies)

        authorization = cookie_dict['auth_token'].replace('%22', '').replace('%0A', '')

        headers = {
            "authority": "mail.cx",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "authorization": "bearer " + authorization,
            "referer": "https://mail.cx/zh/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
        }

        url = f"https://mail.cx/api/api/v1/mailbox/{email_be}@{email_af_str}"
        respons = session1.get(url, headers=headers)
        print(respons.text)

        # 取邮件中的值
        mid = respons.json()[0]['id']

        # 查看邮箱信息


        headers = {
            "authority": "mail.cx",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "authorization": "bearer " + authorization,
            "referer": "https://mail.cx/zh/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
        }

        url = f"https://mail.cx/api/api/v1/mailbox/{email}/{mid}/"
        response = requests.get(url, headers=headers)

        print(response.text)
        code = re.findall(r'>(.*?)</h1>请在5分钟内输入该验证码。', response.json()['body']['html'])[0]





        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://usesless.casdoor.com",
            "Referer": "https://usesless.casdoor.com/signup/usesless.com",

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",

        }

        url = "https://usesless.casdoor.com/api/signup"
        data = {
            "application": "usesless.com",
            "organization": "usesless.com",
            "username": email_be,
            "password": "123456",
            "confirm": "123456",
            "email": email,
            "emailCode": code,
            "agreement": True
        }
        data = json.dumps(data, separators=(',', ':'))
        response = session.post(url, headers=headers, data=data, proxies=proxies)

        print(response.text)
        if response.json()['status'] == 'ok':
            print(f'{email}注册成功')
            redis_pool.lpush('emailList', email)
            time.sleep(60)
    except Exception as e:
        print(e)
        continue
