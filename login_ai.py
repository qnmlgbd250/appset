import requests
import json
# from acc import *
import redis
import os
import dotenv
from dotenv import load_dotenv
acclist = [] # 用于存放账号
# 加载 .env 文件
load_dotenv(".env")
# 连接Redis数据库
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))
for i in range(438):
    ac = r.lindex("emailList", i)
    ac = ac.decode("utf-8")
    print(f'开始登录第{i}个账号' + ac)
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://usesless.casdoor.com",
        "Referer": "https://usesless.casdoor.com/login/oauth/authorize?client_id=7829f693f059d6f0f9fa&response_type=code&redirect_uri=https%3A%2F%2Fai.usesless.com%2Fcallback&scope=read&state=6n416f3ewzc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
    }
    cookies = {
        "casdoor_session_id": "40d06bd540fbcdd2d4e04982ccd670da"
    }
    url = "https://usesless.casdoor.com/api/login"
    params = {
        "clientId": "7829f693f059d6f0f9fa",
        "responseType": "code",
        "redirectUri": "https://ai.usesless.com/callback",
        "scope": "read",
        "state": "6n416f3ewzc",
        "nonce": "",
        "code_challenge_method": "",
        "code_challenge": ""
    }
    data = {
        "application": "usesless.com",
        "organization": "usesless.com",
        "username": ac,
        "password": "123456",
        "autoSignin": True,
        "type": "code"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

    code = response.json().get("data")

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "https://ai.usesless.com",
        "Referer": "https://ai.usesless.com/callback?code=35182dd766e07e5cc001&state=6n416f3ewzc",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48",
    }

    url = "https://ai.usesless.com/api/signin"
    params = {
        "code": code,
        "state": "6n416f3ewzc"
    }
    response = requests.post(url, headers=headers, params=params)

    cookie_re = requests.utils.dict_from_cookiejar(response.cookies)
    print(cookie_re)
    r.lpush("cookieList", cookie_re.get("connect.sid"))