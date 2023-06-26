# -*- coding: utf-8 -*-
import re
import json
import requests
from typing import Dict, Optional, Any
from urllib.parse import urlencode
import random
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
import ujson
from config import *

custom_timeout = httpx.Timeout(read=10, write=10, connect=10, pool=None)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.json_loads = ujson.loads
app.json_dumps = ujson.dumps

# 创建线程锁
lock = threading.Lock()

app.mount("/static", StaticFiles(directory="static"), name="static")
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
    return templates.TemplateResponse('main.html', context={'request': request})


@app.get("/d/{taskid}")
def turn(taskid: str):
    try:
        taskid = taskid.strip()
        rule_json = 'static/rule.json'
        with open(rule_json, mode='rb') as f:
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

            resp = requests.get(ZWYMOCK, params=param,
                                proxies=proxies).json()
            if not resp['data'].get('defaultRule'):
                resp['data']['defaultRule'] = rule_json_list

        elif taskid.startswith('3'):
            resp = requests.get(ZWYPROD, params=param,
                                proxies=proxies).json()
            if not resp['data'].get('defaultRule'):
                resp['data']['defaultRule'] = rule_json_list

        else:
            pass
    except Exception as e:
        output = str(e)
    else:
        output = json.dumps(resp.get('data'), ensure_ascii=False) if (
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
            url = CAIYUNURL
            token = CAIYUNTOKEN
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
            params = {"grant_type": "client_credentials", "client_id": OCRAPIKEY, "client_secret": OCRSECRETKEY}
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

            response = requests.post(url, data=json.dumps(post_data), headers=headers, proxies=proxies)
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


async def get_chat1(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    headers.update({"Authorization": "Bearer " + token})
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
                "model": model
            }
        }
    }
    if lastid:
        data = {"openaiKey": "", "prompt": msg,
                "options": {"parentMessageId": lastid,
                            "systemMessage": f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: {datetime.today().strftime('%Y-%m-%d')}",
                            "completionParams": {"presence_penalty": 0.8, "temperature": 1, "model": model}}}

    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=5) as response:
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
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return
                        if "内容涉及敏感词汇，请遵守相关法律法规~" in str(data):
                            yield {"choices": [{"delta": {"content": '触发敏感词，尝试把提问语句转成"your question + 请用中文回答"的形式'}}]}
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return
                        if "detail" in data and (
                                data['detail'].get('choices') is None or data['detail'].get('choices')[0].get(
                                'finish_reason') is not None):
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return
                        try:
                            yield data['detail']
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "连接失败,刷新试试或请联系管理员"}}]}
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break


async def get_chat2(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    headers.update({"authorization": "Bearer " + token})
    msg = msgdict.get('text')
    lastid = msgdict.get('miniid')

    data = {"prompt": msg,
            "options": {"temperature": 1, "model": model},
            "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."}
    if lastid:
        data = {"prompt": msg,
                "options": {"parentMessageId": lastid,
                            "temperature": 1, "model": model},
                "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."}
    context_too_long = False
    for attempt in range(max_retries):
        if context_too_long:
            data = {
                "prompt": msg,
                "options": {"temperature": 1, "model": 3},
                "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."
            }
            context_too_long = False
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=8) as response:
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
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return
                        if "detail" in data and (data['detail'].get('choices') is None or data['detail'].get('choices')[0].get(
                                'finish_reason') is not None):
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return
                        try:
                            yield data['detail']
                        except Exception as e:
                            logging.error(e)
                            if '[OpenAI] 当前请求上下文过长' in str(data):
                                context_too_long = True
                                logging.info('上下文超限')
                                break
                            yield {"choices": [{"delta": {"content": "连接失败,刷新试试或请联系管理员"}}]}
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        if not context_too_long:
            break


async def get_chat3(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    msg = msgdict.get('text')
    lastmsg3list = msgdict.get('lastmsg3list')
    messages = [
        {"role": "system", "content": "IMPRTANT: You are a virtual assistant powered by the {} model, now time is 2023/5/27 22:47:30}}".format(model)}
    ]
    currenttext = {"role": "user", "content": msg}
    if lastmsg3list:
        lastmsg3list.append(currenttext)
        messages += lastmsg3list
    else:
        messages.append(currenttext)
    if len(messages) > 10:
        messages = messages[0:1] + messages[-7:]
    data = {"messages": messages, "stream": True, "model": model, "temperature": 0.8, "presence_penalty": 1}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=8) as response:
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
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break


async def get_chat4(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    headers.update({"authorization": "Bearer " + token})
    msg = msgdict.get('text')
    data = {
        "info": msg,
        "session_id": 688,
        "scene_preset": [{"key": 1, "value": "", "sel": "system"}],
        "model_is_select": model
    }
    for attempt in range(max_retries):
        try:
            async with AsyncClient() as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=8) as response:
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                        try:
                            start_index = line.find("data:") + len("data:")
                            json_str = line[start_index:].strip()
                            data = json.loads(json_str)
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return
                        if data.get('choices') is None or data.get('choices')[0].get(
                                'finish_reason') is not None:
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return
                        try:
                            yield {"choices": data.get('choices')}
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break


async def get_chat5(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    headers.update({"authorization": token})
    msg = msgdict.get('text')
    lastmsg5list = msgdict.get('lastmsg5list')
    messages = [
        {"role": "assistant", "content": "有什么可以帮你的吗"}
    ]
    currenttext = {"role": "user", "content": msg}
    if lastmsg5list:
        lastmsg5list.append(currenttext)
        messages += lastmsg5list
    else:
        messages.append(currenttext)
    if len(messages) > 10:
        messages = messages[0:1] + messages[-7:]
    data = {"conversation": messages, "stream": True, "model": model, "temperature": 0.8, "presence_penalty": 1}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=custom_timeout) as response:
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
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break

async def get_chat6(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    msg = msgdict.get('text')
    lastmsg6list = msgdict.get('lastmsg6list')
    messages = [
        {"role": "system",
         "content": "IMPORTANT: You are a virtual assistant powered by the {}, now time is 2023/6/11 21:15:34}}".format(model)}
    ]
    currenttext = {"role": "user", "content": msg}
    if lastmsg6list:
        lastmsg6list.append(currenttext)
        messages += lastmsg6list
    else:
        messages.append(currenttext)
    if len(messages) > 10:
        messages = messages[0:1] + messages[-7:]
    data = {"messages": messages, "stream": True, "model": model, "temperature": 0.9, "presence_penalty": 1}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=custom_timeout) as response:
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                        try:
                            start_index = line.find("data:") + len("data:")
                            json_str = line[start_index:].strip()
                            data = json.loads(json_str)
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return
                        if data.get('choices') is None or data.get('choices')[0].get(
                                'finish_reason') is not None:
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return
                        try:
                            yield {"choices": data.get('choices')}
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {str(e)}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break


async def get_chat7(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    msg = msgdict.get('text')
    lastmsg7list = msgdict.get('lastmsg7list')
    messages = [
        {"role": "system", "content": "IMPRTANT: You are a virtual assistant powered by the {} model, now time is 2023/5/27 22:47:30}}".format(model)}
    ]
    currenttext = {"role": "user", "content": msg}
    if lastmsg7list:
        lastmsg7list.append(currenttext)
        messages += lastmsg7list
    else:
        messages.append(currenttext)
    if len(messages) > 10:
        messages = messages[0:1] + messages[-7:]
    data = {"messages": messages, "stream": True, "model": model, "temperature": 0.8, "presence_penalty": 1}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=8) as response:
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                        try:
                            start_index = line.find("data:") + len("data:")
                            json_str = line[start_index:].strip()
                            data = json.loads(json_str)
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return
                        if data.get('choices') is None or data.get('choices')[0].get(
                                'finish_reason') is not None:
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return
                        try:
                            yield {"choices": data.get('choices')}
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break

async def generate_random_number():
    first_digit = 8
    remaining_digits = [random.randint(1, 9) for _ in range(7)]
    return int(str(first_digit) + ''.join(map(str, remaining_digits)))
async def get_chat8(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    msg = msgdict.get('text')
    data = {
        "msg": msg,
        "id": await generate_random_number(),
        "type": "true"
    }
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, data=data,timeout=custom_timeout) as response:
                    if response.status_code != 200:
                        yield {"choices": [{"delta": {"content": "服务器连接失败"}}]}
                        yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                        return
                    else:
                        async for line in response.aiter_lines():
                            if line.strip() == "":
                                continue
                            try:
                                yield {"choices": [{"delta": {"content": line}}]}
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            except Exception as e:
                                logging.error(e)
                                yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break

async def get_chat9(msgdict: Dict[str, Any],token: Optional[str] = None,max_retries: Optional[int] = None,
                   headers: Optional[Dict[str, str]] = None,url: Optional[str] = None,
                   model: Optional[str] = None) -> Any:
    msg = msgdict.get('text')
    lastmsg9list = msgdict.get('lastmsg9list')
    messages = [
        {"role": "system", "content": "IMPORTANT: You are a virtual assistant powered by the {} model, now time is 2023/6/25 21:02:45}}".format(model)}
    ]
    currenttext = {"role": "user", "content": msg}
    if lastmsg9list:
        lastmsg9list.append(currenttext)
        messages += lastmsg9list
    else:
        messages.append(currenttext)
    if len(messages) > 10:
        messages = messages[0:1] + messages[-7:]
    data = {"messages": messages, "stream": True, "model": model, "temperature": 0.8, "presence_penalty": 1}
    for attempt in range(max_retries):
        try:
            async with AsyncClient(proxies=PROXIES) as client:
                async with client.stream('POST', url, headers=headers, json=data, timeout=custom_timeout) as response:
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                        try:
                            start_index = line.find("data:") + len("data:")
                            json_str = line[start_index:].strip()
                            data = json.loads(json_str)
                        except Exception as e:
                            logging.error(e)
                            if 'line 1 column' in str(e):
                                return
                            else:
                                yield {"choices": [{"delta": {"content": "OpenAI服务器连接失败,请联系管理员"}}]}
                                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                                return
                        if data.get('choices') is None or data.get('choices')[0].get(
                                'finish_reason') is not None:
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return
                        try:
                            yield {"choices": data.get('choices')}
                        except Exception as e:
                            logging.error(e)
                            yield {"choices": [{"delta": {"content": "非预期错误,请联系管理员"}}]}
                            yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
                            return

        except httpx.HTTPError as e:
            logging.error(f"WebSocket ReadError: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避策略
                continue
            else:
                yield {"choices": [{"delta": {"content": "服务器连接失败，请稍后重试。"}}]}
                yield {"choices": [{"delta": {"content": "THE_END_哈哈哈"}}]}
        break


async def send_message(websocket, message):
    # await asyncio.sleep(0.03)
    await websocket.send_json(message)

async def get_chat_with_token(site, data, selected_site,client_ip, **kwargs):
    if selected_site == "1":
        token = await get_token_by_redis()
    elif selected_site == "2":
        token = await get_minitoken()
    elif selected_site == "4":
        token = await get_hash_by_redis()
    elif selected_site == "5":
        token = await get_gpt4_by_redis()
    else:
        token = None
    logging.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {client_ip} | {str(data)}')

    return site(data, token=token, **kwargs)


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    chat_functions = {
        "1": get_chat1,
        "2": get_chat2,
        "3": get_chat3,
        "4": get_chat4,
        "5": get_chat5,
        "6": get_chat6,
        "7": get_chat7,
        "8": get_chat8,
        "9": get_chat9
    }
    client_ip = websocket.scope["client"][0]
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            lastmsg3 = ''
            lastmsg4 = ''
            lastmsg5 = ''
            lastmsg6 = ''
            lastmsg7 = ''
            lastmsg9 = ''

            selected_site = data.get("site", "1")
            site_config = SITE_CONFIF_DICT[selected_site]
            selected_function = chat_functions.get(selected_site)
            chat_generator = await get_chat_with_token(selected_function, data, selected_site, client_ip,
                                                       **site_config)

            async for i in chat_generator:
                if i['choices'][0].get('delta').get('content'):
                    # logging.info(i['choices'][0].get('delta'))
                    response_text = i['choices'][0].get('delta').get('content')
                    if selected_site == "2":
                        response_data = {"text": response_text, "miniid": i.get('id')}
                    else:
                        response_data = {"text": response_text, "id": i.get('id')}
                    if selected_site == "3" and 'THE_END_哈哈哈' not in response_text:
                        lastmsg3 += response_text
                    elif selected_site == "4":
                        lastmsg4 += response_text
                    elif selected_site == "5" and 'THE_END_哈哈哈' not in response_text:
                        lastmsg5 += response_text
                    elif selected_site == "6" and 'THE_END_哈哈哈' not in response_text:
                        lastmsg6 += response_text
                    elif selected_site == "7" and 'THE_END_哈哈哈' not in response_text:
                        lastmsg7 += response_text
                    elif selected_site == "9" and 'THE_END_哈哈哈' not in response_text:
                        lastmsg9 += response_text
                    await send_message(websocket, response_data)
            if selected_site == "3":
                response_data = {"lastmsg3list": [{"role": "user", "content": data.get('text')}, {"role": "assistant", "content": lastmsg3}]}
                await send_message(websocket, response_data)
            elif selected_site == "4":
                response_data = {"lastmsg4list": [{"role": "user", "content": data.get('text')}, {"role": "assistant", "content": lastmsg4}]}
                await send_message(websocket, response_data)
            elif selected_site == "5":
                response_data = {"lastmsg5list": [{"role": "user", "content": data.get('text')}, {"role": "assistant", "content": lastmsg5}]}
                await send_message(websocket, response_data)
            elif selected_site == "6":
                response_data = {"lastmsg6list": [{"role": "user", "content": data.get('text')}, {"role": "assistant", "content": lastmsg6}]}
                await send_message(websocket, response_data)
            elif selected_site == "7":
                response_data = {"lastmsg7list": [{"role": "user", "content": data.get('text')}, {"role": "assistant", "content": lastmsg7}]}
                await send_message(websocket, response_data)
            elif selected_site == "9":
                response_data = {"lastmsg9list": [{"role": "user", "content": data.get('text')}, {"role": "assistant", "content": lastmsg9}]}
                await send_message(websocket, response_data)
        except WebSocketDisconnect as e:
            break
        except Exception as e:
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


async def get_gpt4_by_redis():
    for key in redis_pool.hkeys("gpt4plus"):
        value = redis_pool.hget("gpt4plus", key)
        if value:
            value_dict = json.loads(value)
            if value_dict["count"] > 0:
                value_dict["count"] -= 1
                redis_pool.hset("gpt4plus", key, json.dumps(value_dict))
                token = value_dict['token']
                islive = await check_4plus_token(token)
                if not islive:
                    token = await login_gpt4p_token(key.decode('utf-8'), MINIPASSWORD)
                    if token:
                        value_dict['token'] = token
                        redis_pool.hset("gpt4plus", key, json.dumps(value_dict))
                return token
    return None

async def login_gpt4p_token(email,password):
    headers = {
        "authority": AISET5,
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "origin": f"https://{AISET5}",
        "referer": f"https://{AISET5}/login",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
    }
    url = f"https://{AISET5}/api/user/login"
    data = {
        "email": email,
        "password": password
    }
    data = json.dumps(data, separators=(',', ':'))
    try:
        response = requests.post(url, headers=headers, data=data, proxies=PROXIES)
        token = response.json()['sessionToken']
        return token
    except Exception as e:
        logging.error(f"登录获取token异常: {repr(e)}")
        return None

async def check_4plus_token(token):
    headers = {
        "authority": AISET5,
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": token,
        "referer": f"{AISET5}/profile",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
    }
    url = f"{AISET5}/api/user/info"
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES)
        if response.json()['status'] == 0:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"检测token异常: {repr(e)}")
        return False


async def get_minitoken():
    tdict = redis_pool.hget("minigpt", MINIACCOUNT)
    tdict = json.loads(tdict)
    token = tdict['token']
    # 检测token是否过期
    islive = await check_token(token)
    if not islive:
        token = await login_get_token(MINIACCOUNT, MINIPASSWORD)
        if token:
            tdict['token'] = token
            redis_pool.hset("minigpt", MINIACCOUNT, json.dumps(tdict))
    return token


async def check_token(token):
    headers = {
        "authority": AISET2HOME,
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": "Bearer " + token,
        "if-none-match": "W/\"221-syoJ9BkYqkwZhgUeAacHt6kZqtg\"",
        "referer": f"https://{AISET2HOME}/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }
    url = f"https://{AISET2HOME}/api/auth/getInfo"
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES)
        if '请求成功' in response.text:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"检测token异常: {repr(e)}")
        return False


async def login_get_token(miniaccount, minipassword):
    headers = {
        "authority": AISET2HOME,
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "origin": f"https://{AISET2HOME}",
        "referer": f"https://{AISET2HOME}/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }
    url = f"https://{AISET2HOME}/api/auth/login"
    data = {
        "username": miniaccount,
        "password": minipassword
    }
    data = json.dumps(data, separators=(',', ':'))
    try:
        response = requests.post(url, headers=headers, data=data, proxies=PROXIES)
        token = response.json()['data']
        return token
    except Exception as e:
        logging.error(f"登录获取token异常: {repr(e)}")
        return None



if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=20235, reload=True)
