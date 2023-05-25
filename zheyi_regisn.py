# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import requests
import json
import string
import random
import time
from requests.utils import dict_from_cookiejar
import re
proxies = {
  'http': 'http://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068',
  # 'https': 'https://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068'
}
session = requests.Session()
session1 = requests.Session()
email_af = ['nqmo.com', 'qabq.com', 'uuf.me', "yzm.de"]
for _ in range(200):
    try:
        email_af_str = random.choice(email_af)
        letters = string.ascii_lowercase
        email_be = ''.join(random.choice(letters) for i in range(7))
        email = f"{email_be}@{email_af_str}"
        print(email)
        headers = {
            "authority": "888gpt.top",
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json",
            "origin": "https://888gpt.top",
            "referer": "https://888gpt.top/",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        }

        url = "https://888gpt.top/api/auth/register"
        data = {
            "username": email_be,
            "password": "88888888",
            "email": email,
            "invitedBy": "QHKTQMLPTO "
        }
        data = json.dumps(data, separators=(',', ':'))
        response = session.post(url, headers=headers,  data=data, proxies=proxies)

        print(response.text)

        # 刷新邮件
        time.sleep(8)

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
        respons = session1.get(url, headers=headers,proxies=proxies)
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
        response = session1.get(url, headers=headers,proxies=proxies)

        print(response.text)
        jihuo = re.findall(r"点此激活您的账号 \( (.*?) \)", response.json()['body']['text'])[0]
        headers = {
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
          "accept-encoding": "gzip, deflate, br",
          "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
          "referer": "https://mail.cx/",
          "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "sec-fetch-dest": "document",
          "sec-fetch-mode": "navigate",
          "sec-fetch-site": "cross-site",
          "sec-fetch-user": "?1",
          "upgrade-insecure-requests": "1",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        }
        response = session1.get(jihuo, headers=headers, proxies=proxies)
        print(response.text)
    except Exception as e:
        print(e)
        continue


