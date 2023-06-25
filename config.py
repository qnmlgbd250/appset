# -*- coding: utf-8 -*-
import os
import redis
from dotenv import load_dotenv

load_dotenv(".env")

#读取参数设置全局
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')
REDIS_PASS = os.getenv('REDIS_PASS')

ZWYMOCK = os.getenv('ZWYMOCK')
ZWYPROD = os.getenv('ZWYPROD')
CAIYUNURL = os.getenv('CAIYUNURL')
CAIYUNTOKEN = os.getenv('CAIYUNTOKEN')
OCRAPIKEY = os.getenv('OCRAPIKEY')
OCRSECRETKEY = os.getenv('OCRSECRETKEY')
AISET = os.getenv('AISET')
AISET2 = os.getenv('AISET2')
AISET2HOME = os.getenv('AISET2HOME')
AISET3 = os.getenv('AISET3')
AISET4 = os.getenv('AISET4')
AISET4HOME = os.getenv('AISET4HOME')
AISET5 = os.getenv('AISET5')
AISET6 = os.getenv('AISET6')
AISET7 = os.getenv('AISET7')
AISET8 = os.getenv('AISET8')
AISET9 = os.getenv('AISET9')
MINIACCOUNT = os.getenv('MINIACCOUNT')
MINIPASSWORD = os.getenv('MINIPASSWORD')

PROXIES = {'http://': os.getenv('HTTPROXY')}

redis_pool = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB), password=REDIS_PASS)

SITE_CONFIF_DICT = {
    "1": {
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": AISET,
            "Origin": f"https://{AISET}",
            "Referer": f"https://{AISET}/chat/1683609658988",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        },
        "url": f"https://{AISET}/api/chat-process",
        "model":"gpt-3.5-turbo-16k-0613",
        "max_retries": 2,
    }



}

