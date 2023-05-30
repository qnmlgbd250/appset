# -*- coding: utf-8 -*-
# @Time    : 2022/5/8 12:36
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : main.py
# @Software: PyCharm
import re
import json
import requests
import os
import redis
import asyncio
import threading
from httpx import AsyncClient
import httpx
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
import uvicorn
import urllib.parse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from dotenv import load_dotenv
import ujson

# 加载 .env 文件
load_dotenv(".env")
# 连接Redis数据库
redis_pool = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.json_loads = ujson.loads
app.json_dumps = ujson.dumps

# 创建线程锁
lock = threading.Lock()

app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = "templates")
# 设置 logging
logging.basicConfig(filename = 'app.log', level = logging.INFO)


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
        taskid = taskid.strip()
        rule_json = 'static/rule.json'
        with open(rule_json, mode = 'rb') as f:
            rule_json_list = f.read()
            rule_json_list = json.loads(rule_json_list)

        proxies = {
            "http": None,
            "https": None,
        }
        param = {
            'taskId': taskid
        }
        resp = {}
        if taskid.startswith('1'):

            resp = requests.get(os.getenv('ZWYMOCK'), params = param,
                                proxies = proxies).json()
            if not resp['data'].get('defaultRule'):
                resp['data']['defaultRule'] = rule_json_list

        elif taskid.startswith('3'):
            resp = requests.get(os.getenv('ZWYPROD'), params = param,
                                proxies = proxies).json()
            if not resp['data'].get('defaultRule'):
                resp['data']['defaultRule'] = rule_json_list

        else:
            pass
    except Exception as e:
        output = str(e)
    else:
        output = json.dumps(resp.get('data'), ensure_ascii = False) if (
                    resp.get('code') == 200 and resp.get('msg') == 'success') else {}
    return {'output': output}


@app.post("/t")
async def translate(request: Request):
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        data = await request.json()
        tstr = data.get("input_str", "")
        if not tstr:
            output = {}
        else:
            logging.info(f"翻译 | {tstr}")
            trans_type = 'auto2zh'
            zh = re.findall('[\u4e00-\u9fa5]', tstr)
            if zh:
                trans_type = 'auto2en'
            url = os.getenv('CAIYUNURL')
            token = os.getenv('CAIYUNTOKEN')
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
            response = requests.request("POST", url, data = json.dumps(payload), headers = headers, proxies = proxies)
            output = json.loads(response.text)["target"]
    except:
        output = {}

    return {'output': output}


@app.post("/o")
async def ocr(request: Request):
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
            params = {"grant_type": "client_credentials", "client_id": os.getenv('OCRAPIKEY'), "client_secret": os.getenv('OCRSECRETKEY')}
            access_token = str(requests.post(url, params = params, proxies = proxies).json().get("access_token"))
            url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={access_token}"

            # 对二进制数据进行URL编码
            url_encoded_data = urllib.parse.quote(image.split(",")[1])
            payload = 'image=' + url_encoded_data
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }

            response = requests.request("POST", url, headers = headers, data = payload, proxies = proxies)
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


@app.post("/c")
async def curl2requests(request: Request):
    output = {}
    try:
        proxies = {
            "http": None,
            "https": None,
        }
        data = await request.json()
        input_str = data.get("input_str", "")
        if not input_str:
            output = {}
        else:
            url = 'https://spidertools.cn/spidertools/tools/format'

            post_data = {
                "format_type": "curl_to_request",
                "input_str": str(input_str)
            }
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"}

            response = requests.post(url, data = json.dumps(post_data), headers = headers, proxies = proxies)
            if 'import requests' in str(response.text):
                output = response.text.replace('\\nprint(response)"', '')
                output = output.replace('"import', 'import')
                output = re.sub(r'(?<!\\)\\(?=")', '', output)
                output = output.replace('\\\\\\', '\\')

            else:
                output = "转换失败"

    except Exception as e:
        logging.error(e)

    return {'output': output}


async def get_chat(msgdict,token=None,max_retries=8):
    web = os.getenv('AISET')
    proxies = {
        'http://': os.getenv('HTTPROXY'),
    }
    headers = {
          "Accept": "application/json, text/plain, */*",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.9",
          "Authorization": "Bearer " + token,
          "Connection": "keep-alive",
          "Content-Type": "application/json",
          "Host": web,
          "Origin": f"https://{web}",
          "Referer": f"https://{web}/chat/1683609658988",
          "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-origin",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
    url = f"https://{web}/api/chat-process"
    msg = msgdict.get('text')
    lastid = msgdict.get('id')

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
    if lastid:
        data = {"openaiKey": "", "prompt": msg,
                "options": {"parentMessageId": lastid,
                            "systemMessage": f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: {datetime.today().strftime('%Y-%m-%d')}",
                            "completionParams": {"presence_penalty": 0.8, "temperature": 1, "model": "gpt-3.5-turbo"}}}

    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies = proxies) as client:
                async with client.stream('POST', url, headers = headers, json = data, timeout =5) as response:
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                        try:
                            data = json.loads(line)
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                return
                        if '刷新试试~' in str(data):
                            yield {"choices": [{"delta": {"content": "连接失败,重新键入试试~"}}]}
                            return
                        if 'ChatGPT error' in str(data):
                            yield {"choices": [{"delta": {"content": "OpenAI错误,请联系管理员"}}]}
                            return
                        if "Can't create more than max_prepared_stmt_count statements (current value: 99999)" in str(data):
                            yield {"choices": [{"delta": {"content": "token用尽,请联系管理员"}}]}
                            return
                        if '今日剩余回答次数为0' in str(data):
                            yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                            return
                        if '网站今日总共的免费额度已经用完' in str(data):
                            yield {"choices": [{"delta": {"content": "网站今日回答次数已达上限"}}]}
                            return
                        if '今日免费额度10000已经用完啦' in str(data):
                            yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                            return
                        if data['detail'].get('choices') is None or data['detail'].get('choices')[0].get(
                                'finish_reason') is not None:
                            return
                        try:
                            yield data['detail']
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
        break

async def get_chat2(msgdict,token=None,max_retries=8):
    web = os.getenv('AISET2')
    proxies = {
        'http://': os.getenv('HTTPROXY'),
    }
    headers = {
      "accept": "application/json, text/plain, */*",
      "accept-encoding": "gzip, deflate, br",
      "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
      "authorization": "Bearer " + token,
      "content-type": "application/json",
      "origin": web,
      "referer": web,
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
    }
    url = f"{web}/api/chatgpt/chat-process"
    msg = msgdict.get('text')
    lastid = msgdict.get('id')

    data = {"prompt": msg,
            "options": {"temperature": 0.8, "model": 3},
            "systemMessage":"You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."}
    if lastid:
        data = {"prompt": msg,
                "options": {"parentMessageId": lastid,
                            "temperature": 0.8, "model": 3},
                "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies = proxies) as client:
                async with client.stream('POST', url, headers = headers, json = data, timeout =8) as response:
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                        try:
                            data = json.loads(line)
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                return
                        if '刷新试试~' in str(data):
                            yield {"choices": [{"delta": {"content": "连接失败,重新键入试试~"}}]}
                            return
                        if 'ChatGPT error' in str(data):
                            yield {"choices": [{"delta": {"content": "OpenAI错误,请联系管理员"}}]}
                            return
                        if "Can't create more than max_prepared_stmt_count statements (current value: 99999)" in str(data):
                            yield {"choices": [{"delta": {"content": "token用尽,请联系管理员"}}]}
                            return
                        if '今日剩余回答次数为0' in str(data):
                            yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                            return
                        if '网站今日总共的免费额度已经用完' in str(data):
                            yield {"choices": [{"delta": {"content": "网站今日回答次数已达上限"}}]}
                            return
                        if '今日免费额度10000已经用完啦' in str(data):
                            yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                            return
                        if "detail" in data and (data['detail'].get('choices') is None or data['detail'].get('choices')[0].get(
                                'finish_reason') is not None):
                            return
                        try:
                            yield data['detail']
                            await asyncio.sleep(0.05)
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "连接失败,刷新试试或请联系管理员"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
        break

async def get_chat3(msgdict,max_retries=8):
    web = os.getenv('AISET3')
    proxies = {
        'http://': os.getenv('HTTPROXY'),
    }
    headers = {
          "Host": web,
          "Connection": "keep-alive",
          "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
          "sec-ch-ua-platform": "\"Windows\"",
          "sec-ch-ua-mobile": "?0",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
          "Content-Type": "application/json",
          "Accept": "*/*",
          "Origin": f"https://{web}",
          "Sec-Fetch-Site": "same-origin",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Dest": "empty",
          "Referer": f"https://{web}",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }
    url = f"https://{web}/api/openai/v1/chat/completions"
    msg = msgdict.get('text')
    lastmsg = msgdict.get('lastmsg3')
    messages = [
        {"role": "system", "content": "IMPRTANT: You are a virtual assistant powered by the gpt-3.5-turbo model, now time is 2023/5/27 22:47:30}"}
        ]
    currenttext = {"role": "user", "content": msg}
    if lastmsg:
        lastmessage = {"role": "assistant", "content": lastmsg}
        messages.append(lastmessage)
    messages.append(currenttext)
    if len(messages) > 10:
        messages[0:1].extend(messages[-2:])
    data = {"messages": messages, "stream": True, "model": "gpt-3.5-turbo", "temperature": 0.8, "presence_penalty": 1}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies = proxies) as client:
                async with client.stream('POST', url, headers = headers, json = data, timeout =8) as response:
                    async for line in response.aiter_bytes():
                        if line.strip() == "":
                            continue
                        try:
                            decoded_chunk = line.decode("utf-8")
                            yield {"choices": [{"delta": {"content": decoded_chunk}}]}
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
        break

async def get_chat4(msgdict,token=None,max_retries=8):
    web = os.getenv('AISET4')
    home = os.getenv('AISET4HOME')
    headers = {
        "authority": web,
        "accept": "text/event-stream",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "Bearer " + token,
        "content-type": "text/plain;charset=UTF-8",
        "origin": home,
        "referer": home,
        "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    url = f"https://{web}/api/send_bot"
    msg = msgdict.get('text')
    data = {
        "info": msg,
        "session_id": 688
    }
    for attempt in range(max_retries):
        try:
            async with AsyncClient() as client:
                async with client.stream('POST', url, headers = headers, json = data, timeout =8) as response:
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                        try:
                            # 查找 "data:" 的位置
                            start_index = line.find("data:") + len("data:")

                            # 提取 JSON 字符串
                            json_str = line[start_index:].strip()

                            # 将 JSON 字符串转换为 Python 字典
                            data = json.loads(json_str)
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                return
                        if '刷新试试~' in str(data):
                            yield {"choices": [{"delta": {"content": "连接失败,重新键入试试~"}}]}
                            return
                        if 'ChatGPT error' in str(data):
                            yield {"choices": [{"delta": {"content": "OpenAI错误,请联系管理员"}}]}
                            return
                        if "Can't create more than max_prepared_stmt_count statements (current value: 99999)" in str(data):
                            yield {"choices": [{"delta": {"content": "token用尽,请联系管理员"}}]}
                            return
                        if '今日剩余回答次数为0' in str(data):
                            yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                            return
                        if '网站今日总共的免费额度已经用完' in str(data):
                            yield {"choices": [{"delta": {"content": "网站今日回答次数已达上限"}}]}
                            return
                        if '今日免费额度10000已经用完啦' in str(data):
                            yield {"choices": [{"delta": {"content": "今日回答次数已达上限"}}]}
                            return
                        if data.get('choices') is None or data.get('choices')[0].get(
                                'finish_reason') is not None:
                            return
                        try:
                            yield {"choices": data.get('choices')}
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
        break

async def get_chat5(msgdict,token=None,max_retries=8):
    web = os.getenv('AISET5')
    proxies = {
        'http://': os.getenv('HTTPROXY'),
    }
    headers = {
        "authority": web,
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": token,
        "content-type": "application/json",
        "origin": f"https://{web}",
        "referer": f"https://{web}/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }
    url = f"https://{web}/api/bots/openai"
    msg = msgdict.get('text')
    lastmsg = msgdict.get('lastmsg5')
    messages = [
        {"role": "assistant", "content": "有什么可以帮你的吗"}
        ]
    currenttext = {"role": "user", "content": msg}
    if lastmsg:
        lastmessage = {"role": "assistant", "content": lastmsg}
        messages.append(lastmessage)
    messages.append(currenttext)
    if len(messages) > 10:
        messages[0:1].extend(messages[-2:])
    data = {"conversation": messages, "stream": True, "model": "gpt-4", "temperature": 0.8, "presence_penalty": 1}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies = proxies) as client:
                async with client.stream('POST', url, headers = headers, json = data, timeout =8) as response:
                    async for line in response.aiter_bytes():
                        if line.strip() == "":
                            continue
                        try:
                            decoded_chunk = line.decode("utf-8")
                            yield {"choices": [{"delta": {"content": decoded_chunk}}]}
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
        break

async def get_tmpIntegral(token=None):
    proxies = {
        'http': os.getenv('HTTPROXY'),
    }
    web = os.getenv('AISET')
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": "Bearer " + token,
        "Connection": "keep-alive",
        "Referer": f"https://{web}/account",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = f"https://{web}/api/cms/users/me"
    try:
        response = requests.get(url, headers=headers, timeout=30, proxies=proxies)

        tmpIntegral = response.json().get('tmpIntegral')
        return tmpIntegral
    except Exception as e:
        logging.error(e)
        return 0

async def send_message(websocket, message):
    # 发送消息之前等待 1 秒钟
    await asyncio.sleep(0.03)
    await websocket.send_json(message)


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    client_ip = websocket.scope["client"][0]
    await websocket.accept()
    last_text = ''
    language = ["python", "java", "c", "cpp", "c#", "javascript", "html", "css", "go", "ruby", "swift", "kotlin"]
    lastmsg3 = ''
    lastmsg5 = ''
    while True:
        try:
            data = await websocket.receive_json()
            #测试代码
            # await websocket.send_json({"text": '你好，有什么可以帮助您的吗?', "id": ''})

            selected_site = data.get("site", "1")  # 默认为站点1 # 默认值为1
            if selected_site == "1":
                token = await get_token_by_redis()
                # tmpIntegral = await get_tmpIntegral(token = token)
                logging.info(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {client_ip} | {str(data)}')
                chat_generator = get_chat(data, token = token)
            elif selected_site == "2":
                token = os.getenv('TOKEN')
                logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {client_ip} | {str(data)}')
                chat_generator = get_chat2(data, token = token)

            elif selected_site == "3":
                logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {client_ip} | {str(data)}')
                chat_generator = get_chat3(data)

            elif selected_site == "4":
                # token = os.getenv('GPT4TOKEN')
                token = await get_hash_by_redis()
                logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {client_ip} | {str(data)}')
                chat_generator = get_chat4(data, token = token)

            elif selected_site == "5":
                token = os.getenv('GPT4TOKEN2')
                # token = await get_hash_by_redis()
                logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {client_ip} | {str(data)}')
                chat_generator = get_chat5(data, token = token)

            async for i in chat_generator:
                if i['choices'][0].get('delta').get('content'):
                    # logging.info(i['choices'][0])
                    response_text = i['choices'][0].get('delta').get('content')
                    if response_text.strip() == '``':
                        last_text = '``'
                        response_text = ''
                    if '`' in response_text and last_text == '``':
                        response_text = response_text.strip().replace('`', '```')
                        last_text = '```'
                    if response_text.strip() == '```':
                        last_text = '```'
                    if last_text == '```' and any([i in response_text for i in language]):
                        for j in language:
                            if j == response_text:
                                response_text = response_text.replace(j, '')
                                if j == 'c':
                                    last_text = 'c'
                                else:
                                    last_text = ''
                                break
                    if last_text == 'c' and '++' in response_text:
                        response_text = response_text.replace('++', '')
                        last_text = ''
                    response_data = {"text": response_text, "id": i.get('id')}
                    if selected_site == "3":
                        lastmsg3 += response_text
                    if selected_site == "5":
                        lastmsg5 += response_text
                    await send_message(websocket, response_data)
            if selected_site == "3":
                response_data = {"lastmsg3": lastmsg3}
                await send_message(websocket, response_data)
            if selected_site == "5":
                response_data = {"lastmsg5": lastmsg5}
                await send_message(websocket, response_data)
        except WebSocketDisconnect as e:
            # 处理断开连接的情况
            break
        except Exception as e:
            # 记录其他异常
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.error(f"{now} | WebSocket 异常: {repr(e)}")
            break


async def get_token_by_redis():
    reset = False
    list_length = redis_pool.llen('cookieList')
    tokenindex = int(redis_pool.get('tokenindex'))
    if tokenindex == list_length:
        tokenindex = 0
        reset = True
    token = redis_pool.lindex('cookieList', tokenindex)
    token = token.decode('utf-8')
    if tokenindex == 0 and reset:
        tokenindex_reset = tokenindex
    else:
        tokenindex_reset = tokenindex + 1

    redis_pool.set('tokenindex', str(tokenindex_reset))
    return token

async def get_hash_by_redis():
    for key in redis_pool.hkeys("hash_db"):
        value = redis_pool.hget("hash_db", key)
        if value:
            value_dict = json.loads(value)
            if value_dict["count"] > 0:
                value_dict["count"] -= 1
                redis_pool.hset("hash_db", key, json.dumps(value_dict))
                return value_dict['token']
    return None


if __name__ == '__main__':
    uvicorn.run('main:app', host = "0.0.0.0", port = 20235, reload = True)
