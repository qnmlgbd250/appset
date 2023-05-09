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

        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://ai.usesless.com",
            "Referer": "https://ai.usesless.com/register",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        }
        url = "https://ai.usesless.com/api/cms/auth/local/register"
        data = {
            "username": email_be,
            "password": "88888888",
            "email": email
        }
        data = json.dumps(data, separators=(',', ':'))
        response = session.post(url, headers=headers, data=data, proxies=proxies)

        print(response.text)





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
        code = re.findall(r'confirmation=(.*?)<', response.json()['body']['html'])[0]
        jihuo = f'http://ai.usesless.com/api/cms/auth/email-confirmation?confirmation={code}'
        headers = {
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
              "Accept-Encoding": "gzip, deflate",
              "Accept-Language": "zh-CN,zh;q=0.9",
              "Connection": "keep-alive",
              "Host": "ai.usesless.com",
              "Upgrade-Insecure-Requests": "1",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            }
        response = session1.get(jihuo, headers=headers,proxies=proxies)
        if response.status_code == 200:
            print(f'{email}：激活成功')
            redis_pool.lpush('emailList', email)







    except Exception as e:
        print(e)
        continue
