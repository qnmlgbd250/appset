# -*- coding: utf-8 -*-
from config import *
def check_token(token):
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
        return False


def get_minitoken():
    tdict = redis_pool.hget("minigpt", MINIACCOUNT)
    tdict = json.loads(tdict)
    token = tdict['token']
    # 检测token是否过期
    islive = check_token(token)
    if islive:
        return True
    else:
        token = login_get_token(MINIACCOUNT, MINIPASSWORD)
        if token:
            tdict['token'] = token
            redis_pool.hset("minigpt", MINIACCOUNT, json.dumps(tdict))
            return True


def login_get_token(miniaccount, minipassword):
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
    if not get_minitoken():
        send_msg.send_dingding('小号token过期，请及时处理')