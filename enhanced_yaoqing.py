# -*- coding: utf-8 -*-
import requests
import string
import random
import time
from requests.utils import dict_from_cookiejar
import re
import json

proxies = {
  'http': 'http://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068',
  # 'https': 'https://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068'
}
h1 = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
  "cache-control": "max-age=0",
  "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "same-origin",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
}

headers = {
    "authority": "www.chatgptenhanced.com",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/json",
    "referer": "https://www.chatgptenhanced.com/register?code=ad3374",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
}
session = requests.Session()
session1 = requests.Session()

email_af = ['nqmo.com', 'qabq.com', 'uuf.me', "yzm.de", "end.tw"]
for _ in range(100):
    try:
        email_af_str = random.choice(email_af)
        letters = string.ascii_lowercase
        email_be = ''.join(random.choice(letters) for i in range(7))
        email = f"{email_be}@{email_af_str}"
        print(email)


        send_url = "https://www.chatgptenhanced.com/api/user/register/code"
        params = {
            "email": email
        }
        res = session.get(send_url, headers=headers,params = params,proxies=proxies)

        print(res.text)

        # 刷新邮件
        time.sleep(5)

        response = session1.get('https://mail.cx/zh/', headers=h1, proxies=proxies)

        # 获取响应中的cookie字典
        cookie_dict = dict_from_cookiejar(response.cookies)

        authorization = cookie_dict['auth_token'].replace('%22', '').replace('%0A', '')

        headers1 = {
            "authority": "mail.cx",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "authorization": "bearer " + authorization,
            "referer": "https://mail.cx/zh/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
        }

        url = f"https://mail.cx/api/api/v1/mailbox/{email_be}@{email_af_str}"
        respons = session1.get(url, headers=headers1, proxies=proxies)
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
        response = session1.get(url, headers=headers, proxies=proxies)

        email_code = re.findall(r'您的激活码是：(\d+)，', response.json()['body']['text'])[0]

        headers = {
            "authority": "www.chatgptenhanced.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.chatgptenhanced.com",
            "referer": "https://www.chatgptenhanced.com/register",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
        }
        url = "https://www.chatgptenhanced.com/api/user/register"
        data = {
            "email": email,
            "password": "88888888",
            "code": email_code,
            "code_type": "email",
            "invitation_code": "a18498"
        }
        data = json.dumps(data, separators=(',', ':'))
        response = session.post(url, headers=headers, data=data, proxies=proxies)

        print(response.text)
    except:
        print("error")
        continue

# import requests
# import json
#
#
# headers = {
#     "authority": "www.chatgptenhanced.com",
#     "accept": "*/*",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InExeW5wbXJmQHFhYnEuY29tIiwiZXhwIjoxNjg1OTc0ODI0LCJpYXQiOjE2ODUzNzAwMjQsIm5iZiI6MTY4NTM3MDAyNH0.y75XRPLVqRmt1wMro_4f7XhBz9J9ddNgjfrzmKTeDpY",
#     "content-type": "application/json",
#     "origin": "https://www.chatgptenhanced.com",
#     "referer": "https://www.chatgptenhanced.com/",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
# }
# url = "https://www.chatgptenhanced.com/api/bots/openai"
# data = {
#     "model": "gpt-4",
#     "conversation": [
#         {
#             "role": "assistant",
#             "content": "有什么可以帮你的吗"
#         },
#         {
#             "role": "user",
#             "content": "说说三体"
#         }
#     ],
#     "stream": True,
#     "temperature": 0.7,
#     "max_tokens": 500,
#     "presence_penalty": 0
# }
# data = json.dumps(data, separators=(',', ':'))
# response = requests.post(url, headers=headers, data=data)
#
# print(response.text)
#q1ynpmrf@qabq.com


#登录
# import requests
# import json
#
#
# headers = {
#     "authority": "www.chatgptenhanced.com",
#     "accept": "*/*",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "content-type": "application/json",
#     "origin": "https://www.chatgptenhanced.com",
#     "referer": "https://www.chatgptenhanced.com/login",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
# }
# url = "https://www.chatgptenhanced.com/api/user/login"
# data = {
#     "email": "agkkybt@yzm.de",
#     "password": "88888888"
# }
# data = json.dumps(data, separators=(',', ':'))
# response = requests.post(url, headers=headers, data=data)
#
# print(response.text)


