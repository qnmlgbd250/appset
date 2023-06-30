# -*- coding: utf-8 -*-
import requests
import string
import random
import time
from requests.utils import dict_from_cookiejar
import re
import json
import os
import redis
from dotenv import load_dotenv
acclist = [] # 用于存放账号
# 加载 .env 文件
load_dotenv(".env")
# 连接Redis数据库
redis_pool = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))



proxies = {
  'http': 'http://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068',
  # 'https': 'https://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068'
}

h1_e = {
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

h1_f = {
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
#登录获取邀请码
def get_invitecode(token):

    headers = {
        "authority": "www.chatgptenhanced.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": token,
        "referer": "https://www.chatgptenhanced.com/profile",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }
    url = "https://www.chatgptenhanced.com/api/user/info/invite-code"
    response = session.get(url, headers=headers)
    inviteCode = response.json().get('inviteCode')
    return inviteCode

#升级计划
def upgrade_plan(inviteCode):
    conut = 0
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
            res = session.get(send_url, headers = h1_f, params = params, proxies = proxies)

            print(res.text)

            # 刷新邮件
            time.sleep(5)

            response = session1.get('https://mail.cx/zh/', headers = h1_e, proxies = proxies)

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
            respons = session1.get(url, headers = headers1, proxies = proxies)
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
            response = session1.get(url, headers = headers, proxies = proxies)

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
                "invitation_code": inviteCode
            }
            data = json.dumps(data, separators = (',', ':'))
            response = session.post(url, headers = headers, data = data, proxies = proxies)

            if 'sessionToken' in response.json():
                conut += 1
                print(response.json())
            if conut == 10:
                return True
        except:
            print("error")
            continue

#把订阅账号存到redis
def save_redis(data):
    for k, v in data.items():
        token = v.get('sessionToken')
        inviteCode = get_invitecode(token)
        if upgrade_plan(inviteCode):
            print("升级成功")
            hash_name = 'gpt4plus'
            n_v = {
                "token": token,
                "count": 20
            }
            redis_pool.hset(hash_name, k, json.dumps(n_v))
            # 验证数据是否已经存储在 Redis 中
            print(redis_pool.hget(hash_name, k))

def check_plus(user,token):

    headers = {
        "authority": "www.chatgptenhanced.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": token,
        "referer": "https://www.chatgptenhanced.com/profile",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }
    url = "https://www.chatgptenhanced.com/api/user/info"
    response = requests.get(url, headers=headers, proxies=proxies)

    print(response.text)
    if not response.json():
        token = login_(user.decode('utf-8'), '88888888')
        hash_name = 'gpt4plus'
        n_v = {
            "token": token,
            "count": 20
        }
        redis_pool.hset(hash_name,user, json.dumps(n_v))
        # 验证数据是否已经存储在 Redis 中
        print(redis_pool.hget(hash_name, user))



def login_(user,pwd):
    headers = {
        "authority": "www.chatgptenhanced.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.chatgptenhanced.com",
        "referer": "https://www.chatgptenhanced.com/login",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37"
    }
    url = "https://www.chatgptenhanced.com/api/user/login"
    data = {
        "email": user,
        "password": pwd
    }
    data = json.dumps(data, separators = (',', ':'))
    response = requests.post(url, headers = headers, data = data)

    sessionToken = response.json().get('sessionToken')
    return sessionToken

if __name__ == '__main__':

    #升级计划
    # data = {
    #     "tbyekkb@uuf.me":
    #         {'status': 0, 'sessionToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRieWVra2JAdXVmLm1lIiwiZXhwIjoxNjg4NzIxMDkxLCJpYXQiOjE2ODgxMTYyOTEsIm5iZiI6MTY4ODExNjI5MX0.HOuSUMJfBPzQLN6v7aSwt0Scriybl1MY-YaJR9lkYDk', 'exp': 1688721091}


    # }
    # save_redis(data)

    #检查是否升级成功
    for key in redis_pool.hkeys("gpt4plus"):
        value = redis_pool.hget("gpt4plus", key)
        if value:
            value_dict = json.loads(value)
            token = value_dict.get('token')
            check_plus(key,token)




