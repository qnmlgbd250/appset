# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv(".env")
import os
web = os.getenv('AISET')
from datetime import datetime
import requests

token = 's%3AxQ7VgsDh9Z8HRZLAq_Gr_6_-gwPCOQZt.NVCU1AUqwkakuPS%2BGNf0AHNSbzvMSrqvkWGfk1Vqtu0'
headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "origin": f"https://{web}",
        "referer": f"https://{web}/chat/1681217446562",
        'cookie': f'connect.sid={token}',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    }
url = f"https://{web}/api/chat-process"
msg = '你好'
lastid = ''

data = {
    "openaiKey": "",
    "prompt": msg,
    "options": {
        "systemMessage": f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\
Knowledge cutoff: 2021-09-01\
Current date: {datetime.today().strftime('%Y-%m-%d')}",
        "completionParams": {
            "presence_penalty": 0.8,
            "temperature": 1,
            "model": "gpt-3.5-turbo"
        }
    }
}

data = requests.post(url, headers=headers, json=data)
print(data.text)
