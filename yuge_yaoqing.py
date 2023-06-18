# -*- coding: utf-8 -*-
import requests
import string
import random
import time
from requests.utils import dict_from_cookiejar
import re
proxies = {
  'http': 'http://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068',
  # 'https': 'https://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068'
}
cou = 0
headers = {
  "Host": "yuge-admin.orence.cn",
  "Connection": "keep-alive",
  "Content-Length": "0",
  "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "Authorization": "Bearer undefined",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42",
  "sec-ch-ua-platform": "\"Windows\"",
  "Accept": "*/*",
  "Origin": "https://yuge.orence.cn",
  "Sec-Fetch-Site": "same-site",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Dest": "empty",
  "Referer": "https://yuge.orence.cn/",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.9"
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

session = requests.Session()
session1 = requests.Session()

email_af = ['nqmo.com', 'qabq.com', 'uuf.me', "yzm.de", "end.tw"]
for _ in range(200):
    try:
        email_af_str = random.choice(email_af)
        letters = string.ascii_lowercase
        email_be = ''.join(random.choice(letters) for i in range(7))
        email = f"{email_be}@{email_af_str}"
        print(email)

        send_url = f'https://yuge-admin.orence.cn/api/send_email?email={email}'
        res = session.post(send_url, headers=headers,proxies=proxies)

        print(res.json())

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

        email_code = re.findall(r'输入此次验证码 (\d+) （3分钟内有效）', response.json()['body']['text'])[0]

        url = f"https://yuge-admin.orence.cn/api/register?name={email_be}&email={email}&password=88888888&email_code={email_code}&invite_code=QXG6PA"

        res = session.post(url, headers=headers,proxies=proxies)
        print(res.json())
        if '注册成功' in str(res.text):
            print('注册成功')
            cou += 1
        if cou == 81:
            break
    except:
        continue

