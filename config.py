# -*- coding: utf-8 -*-
import os
import redis
import json
import send_msg
import logging
import requests
from dotenv import load_dotenv

load_dotenv(".env")

# 读取参数设置全局
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
        "model": "gpt-3.5-turbo-16k-0613",
        "max_retries": 2,
    },
    "2": {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "origin": AISET2,
            "referer": AISET2,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        },
        "url": f"{AISET2}/api/chatgpt/chat-process",
        "model": 3,
        "max_retries": 2,
    },
    "3": {
        "headers": {
            "Host": AISET3,
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": f"https://{AISET3}",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": f"https://{AISET3}",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        },
        "url": f"https://{AISET3}/api/openai/v1/chat/completions",
        "model": "gpt-3.5-turbo-16k-0613",
        "max_retries": 2,
    },
    "4": {
        "headers": {
            "authority": AISET4,
            "accept": "text/event-stream",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "text/plain;charset=UTF-8",
            "origin": AISET4HOME,
            "referer": AISET4HOME,
            "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        },
        "url": f"https://{AISET4}/api/send_bot",
        "model": "gpt-4",
        "max_retries": 5,
    },
    "5": {
        "headers": {
            "authority": AISET5,
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "origin": f"https://{AISET5}",
            "referer": f"https://{AISET5}/",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
        },
        "url": f"https://{AISET5}/api/bots/openai",
        "model": "gpt-4",
        "max_retries": 2,
    },
    "6": {
        "headers": {
            "Accept": "text/event-stream",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Type": "application/json",
            "Origin": AISET6,
            "Referer": AISET6,
            "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
            "X-Requested-With": "XMLHttpRequest"
        },
        "url": f"{AISET6}/api/openai/v1/chat/completions",
        "model": "gpt-3.5-turbo-16k-0613",
        "max_retries": 2,
    },
    "7": {
        "headers": {
            "Host": AISET7,
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": f"https://{AISET7}",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": f"https://{AISET7}",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        },
        "url": f"https://{AISET7}/api/openai/v1/chat/completions",
        "model": "gpt-4-0613",
        "max_retries": 2,
    },
    "8": {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "origin": AISET2,
            "referer": AISET2,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
        },
        "url": f"{AISET2}/api/chatgpt/chat-process",
        "model": 3,
        "max_retries": 2,
    },
    "9": {
        "headers": {
            "Host": AISET7,
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": f"https://{AISET7}",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": f"https://{AISET7}",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        },
        "url": f"https://{AISET7}/api/openai/v1/chat/completions",
        "model": "gpt-4-0613",
        "max_retries": 2,
    },

}
