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
    print("mini token活性状态：", islive)
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



def get_gpt4_by_redis():
    try:
        for key in redis_pool.hkeys("gpt4plus"):
            value = redis_pool.hget("gpt4plus", key)
            value_dict = json.loads(value)
            token = value_dict['token']
            islive = check_4plus_token(token)
            print("gpt4plus token活性状态：", islive)
            if not islive:
                token = login_gpt4p_token(key.decode('utf-8'), MINIPASSWORD)
            value_dict['token'] = token
            value_dict['info'] = get_4plus_limit(token)
            redis_pool.hset("gpt4plus", key, json.dumps(value_dict))
        return True
    except Exception as e:
        logging.error(f"获取gpt4plus账号异常: {repr(e)}")
        return False

def login_gpt4p_token(email,password):
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

def check_4plus_token(token):
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
    url = f"https://{AISET5}/api/user/info"
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES)
        if response.json()['status'] == 0:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"检测token异常: {repr(e)}")
        return False

def get_4plus_limit(token):
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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79"
    }
    url1 = f"https://{AISET5}/api/user/info/rate-limit"
    url2 = f"https://{AISET5}/api/user/info/subscription"
    try:
        response = requests.get(url1, headers=headers, proxies=PROXIES)
        remaining_gpt4 = response.json()['data']['remaining_gpt4']
        response = requests.get(url2, headers=headers, proxies=PROXIES)
        gpt4ptime = response.json()['data']
        return [remaining_gpt4, gpt4ptime]
    except Exception as e:
        logging.error(f"获取剩余次数异常: {repr(e)}")
        return 0


def get_gpt4199_token():
    try:
        for key in redis_pool.hkeys("chat199oken"):
            value = redis_pool.hget("chat199oken", key)
            value_dict = json.loads(value)
            token = value_dict['token']
            islive,vip = check_4_token(token)
            print("gpt4p token活性状态：", islive)
            if not islive:
                token = login_4_token(key.decode('utf-8'), MINIPASSWORD)
                islive, vip = check_4_token(token)
            value_dict['token'] = token
            value_dict['vip'] = vip
            redis_pool.hset("chat199oken", key, json.dumps(value_dict))
        return True
    except Exception as e:
        logging.error(f"获取gpt4账号异常: {repr(e)}")
        return False

def check_4_token(token):
    headers = {
        "authority": AISET10,
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "Bearer " + token,
        "origin": AISET10HOME,
        "referer": AISET10HOME,
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    url = f"https://{AISET10}/api/get_user"
    try:
        response = requests.post(url, headers=headers, proxies=PROXIES)
        if response.json()['status'] == 200:
            resjson = response.json()
            vip = resjson['vip']
            vip.update({'last_msg': resjson["last_msg"]})
            return True, vip
        else:
            return False, None
    except Exception as e:
        logging.error(f"检测token异常: {repr(e)}")
        return False

def login_4_token(email,password):
    headers = {
        "authority": AISET10,
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-length": "0",
        "origin": AISET10HOME,
        "referer": AISET10HOME,
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    url = f"https://{AISET10}/api/web_login"
    params = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(url, headers=headers, params=params, proxies=PROXIES)
        token = response.json()['token']
        return token
    except Exception as e:
        logging.error(f"登录获取token异常: {repr(e)}")
        return None



def get_gptciyun_token():
    try:
        for key in redis_pool.hkeys("ciyuntoken"):
            value = redis_pool.hget("ciyuntoken", key)
            value_dict = json.loads(value)
            token = value_dict['token']
            islive,vip = check_ciyun_token(token)
            print("gpt4p token活性状态：", islive)
            if not islive:
                token = login_ciyun_token(key.decode('utf-8'), MINIPASSWORD)
                islive, vip = check_ciyun_token(token)
            value_dict['token'] = token
            value_dict['vip'] = vip
            redis_pool.hset("ciyuntoken", key, json.dumps(value_dict))
        return True
    except Exception as e:
        logging.error(f"获取慈云账号异常: {repr(e)}")
        return False

def check_ciyun_token(token):
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Length": "0",
    "authorization": "Bearer " + token,
    "Origin": f"https://ai.{AISET15}",
    "Referer": f"https://ai.{AISET15}/",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"
}
    url = f"https://gpt.{AISET15}/api/get_user"
    try:
        response = requests.post(url, headers=headers, proxies=PROXIES)
        if response.json()['status'] == 200:
            resjson = response.json()
            vip = resjson['vip']
            vip.update({'last_msg': resjson["last_msg"]})
            return True, vip
        else:
            return False, None
    except Exception as e:
        logging.error(f"检测token异常: {repr(e)}")
        return False

def login_ciyun_token(email,password):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Authorization": "Bearer",
        "Content-Length": "0",
        "Origin": f"https://ai.{AISET15}",
        "Referer": f"https://ai.{AISET15}/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"
    }
    url = f"https://gpt.{AISET15}/api/web_login"
    params = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(url, headers=headers, params=params, proxies=PROXIES)
        token = response.json()['token']
        return token
    except Exception as e:
        logging.error(f"登录获取token异常: {repr(e)}")
        return None






if __name__ == '__main__':
    if not get_minitoken():
        send_msg.send_dingding('小号token过期，请及时处理')
    if not get_gpt4_by_redis():
        send_msg.send_dingding('gpt4plus token过期，请及时处理')
    if not get_gpt4199_token():
        send_msg.send_dingding('gpt4 token过期，请及时处理')
    if not get_gptciyun_token():
        send_msg.send_dingding('gpt4p token过期，请及时处理')