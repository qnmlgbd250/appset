# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 12:36
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : main.py
# @Software: PyCharm
import re
import json
import rsa, base64
import requests
from datetime import datetime
from fastapi import FastAPI, Form, Request
import uvicorn
from typing import Dict
import urllib.parse
import lzstring
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")
# 设置 logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# 添加 middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    if 'static' not in request.url.path:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 设置时区为北京时间
        # 记录请求信息，包括请求方法、URL 和 IP 地址、请求时间
        logging.info(f"{now} | 请求 {request.method} | {request.url} | 请求IP {request.client.host}")
    response = await call_next(request)
    if 'static' not in request.url.path:
        # 记录响应信息，包括响应状态码
        logging.info(f"响应 | {response.status_code}")
    return response


@app.get("/")
def getdate(request: Request):
    return templates.TemplateResponse('main.html', context = {'request': request})

@app.get("/d/{taskid}")
def turn(taskid: str):
    try:
        old_region_list = ['shanxi', 'shenzhen', "henan", 'guangdong', 'anhui', 'jiangsu']
        accname = ['test老地区转苍穹申报表']
        taskid = taskid.strip()
        rule_json = 'static/rule.json'
        with open(rule_json, mode='rb') as f:
            rule_json_list = f.read()
            rule_json_list = json.loads(rule_json_list)

        proxies ={
              "http": None,
              "https": None,
            }
        param = {
            'taskId': taskid
        }
        resp = {}
        if taskid.startswith('1'):

            resp = requests.get('https://mtax.kdzwy.com/taxtask/api/task/history', params=param, proxies=proxies).json()
            if ((not resp['data'].get('defaultRule')) and (resp['data']['region'] not in old_region_list)) or resp['data'].get('accName') in accname:
                resp['data']['defaultRule'] = rule_json_list

        elif taskid.startswith('3'):
            resp = requests.get('https://tax.kdzwy.com/taxtask/api/task/history', params=param, proxies=proxies).json()
            if (not resp['data'].get('defaultRule')) and (resp['data']['region'] not in old_region_list):
                resp['data']['defaultRule'] = rule_json_list

        else:
            pass
    except Exception as e:
        output = str(e)
    else:
        output = json.dumps(resp.get('data'), ensure_ascii=False) if (resp.get('code') == 200 and resp.get('msg') == 'success') else {}
    return {'output': output}


@app.get("/t/{tstr}")
def translate(tstr: str):
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        if not tstr:
            output = {}
        else:
            trans_type = 'auto2zh'
            zh = re.findall('[\u4e00-\u9fa5]', tstr)
            if zh:
                trans_type = 'auto2en'
            url = "http://api.interpreter.caiyunai.com/v1/translator"
            token = "msc7eu66huxs0ukm85m2"
            payload = {
                "source": tstr,
                "trans_type": trans_type,
                "request_id": "demo",
                "detect": True,
            }
            headers = {
                "content-type": "application/json",
                "x-authorization": "token " + token,
            }
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers, proxies=proxies)
            output = json.loads(response.text)["target"]
    except:
        output = {}

    return {'output': output}


@app.post("/o")
async def ocr(request: Request):
    API_KEY = "zaoZ9K2OQIvgNhm9gr8rjjEo"
    SECRET_KEY = "Ov05o1fmdtACt4OI8thRcPZLIjGHcUph"
    output = {}
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        data = await request.json()
        image = data.get("image", "")
        if not image:
            output = {}
        else:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
            access_token = str(requests.post(url, params=params, proxies=proxies).json().get("access_token"))
            url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={access_token}"

            # 对二进制数据进行URL编码
            url_encoded_data = urllib.parse.quote(image.split(",")[1])
            payload = 'image=' + url_encoded_data
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
            if 'error' in str(response.text):
                output = {}
            if 'words_result' in str(response.text):
                output = ''
                res = response.json()
                for line in res['words_result']:
                    output += line['words'] + '\n'

    except Exception as e:
        logging.error(e)

    return {'output': output}

@app.post("/chat")
async def chatapi(request: Request):
    output = {}
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54",
        }
        url = "https://chatapi.javaex.cn/chat"
        proxies = {
            "http": None,
            "https": None,
        }
        data = await request.json()
        chatword = data.get("chatword", "")
        if not chatword:
            output = {}
        else:
            post_data = {
                "questions": [
                    {
                        "role": "user",
                        "content": chatword
                    }
                ],
                "pkey": None
            }
            post_data = json.dumps(post_data, separators=(',', ':'))
            response = requests.post(url, headers=headers, data=post_data, proxies=proxies)
            if '操作成功' in response.json()['message']:
                output = response.json()['data']['choices'][0]['message']['content']
            else:
                logging.error(response.text)
                output = '操作失败,请稍后再试'


    except Exception as e:
        logging.error(e)

    return {'output': output}







if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=20234, reload=True)




