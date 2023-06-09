# -*- coding: utf-8 -*-
import requests
import json
import os
import re
import random
import time
import string
from dotenv import load_dotenv
load_dotenv(".env")

PROXIES = {'http://': os.getenv('HTTPROXY')}

session_em = requests.session()
session_send = requests.session()

def init_email():
    for _ in range(10):
        try:
            em_str = generate_random_string()
            headers_em = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
            }
            url = "http://24mail.chacuo.net/"
            headers = {
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "http://24mail.chacuo.net",
                "Referer": "http://24mail.chacuo.net/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }
            response = session_em.get(url, headers=headers_em, verify=False)



            url = "http://24mail.chacuo.net/"
            data = {
                "data": em_str,
                "type": "set",
                "arg": "d=chacuo.net_f="
            }
            response = session_em.post(url, headers=headers, data=data, verify=False)

            print(response.text)

            send_em(em_str)

            time.sleep(30)
            data = {
                "data": em_str,
                "type": "refresh",
                "arg": ""
            }
            response = session_em.post(url, headers=headers, data=data, verify=False)
            mid = response.json()['data'][0]['list'][0]['MID']

            headers_mid = {
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": url,
                "Referer": url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }
            data = {
                "data": em_str,
                "type": "mailinfo",
                "arg": f"f={mid}"
            }
            response = session_em.post(url, headers=headers_mid, data=data, verify=False)

            print(response.text)
            jihuo = re.findall(r'<a href="(.*?)"', response.json()['data'][-1][-1][0]['DATA'][0])[0]

            response = session_em.get(jihuo, headers=headers, proxies=PROXIES)
            print(response.text)
        except Exception as e:
            print(e)
            continue


def send_em(em_str):
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
        "username": em_str,
        "password": "88888888",
        "email": em_str + "@chacuo.net",
        "invitedBy": "RIMNGURQYJ"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = session_send.post(url, headers=headers, data=data, proxies=PROXIES)

    print(response.text)

def generate_random_string():
    letters = ''.join(random.choices(string.ascii_letters, k=6)).lower()
    numbers = ''.join(random.choices(string.digits, k=5))
    return letters + numbers

if __name__ == '__main__':
    print(init_email())
