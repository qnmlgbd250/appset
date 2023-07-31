import requests
import string
import random
import time
from requests.utils import dict_from_cookiejar
import re
proxies = {
  'http': 'http://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068',
  # 'https': 'https://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068'
}


web_session = requests.Session()
emil_session = requests.Session()



def send_email(email):
    headers = {
        "authority": "gpt.ciyundata.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": "Bearer",
        "content-length": "0",
        "origin": "https://ai.ciyundata.com",
        "referer": "https://ai.ciyundata.com/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"
    }
    url = "https://gpt.ciyundata.com/api/generate_cap"
    params = {
        "type": "email",
        "email": email
    }
    response = web_session.post(url, headers=headers, params=params, proxies=proxies)
    verify_code = response.json()['data']
    url = "https://gpt.ciyundata.com/api/send_email"
    params = {
        "email": email,
        "verify_code": verify_code
    }
    response = requests.post(url, headers=headers, params=params, proxies=proxies)

    print(response.json())
    if response.json()['status'] == 200:
        return True
    else:
        return False


def get_random_email():
    email_af = ['nqmo.com', 'qabq.com', 'uuf.me', "yzm.de", "end.tw"]
    email_af_str = random.choice(email_af)
    letters = string.ascii_lowercase
    email_be = ''.join(random.choice(letters) for i in range(7))
    email = f"{email_be}@{email_af_str}"
    print(email)
    return email_af_str, email_be, email
def get_emil_verify_code(email_af_str, email_be, email):
    h1 = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }
    # 刷新邮件
    time.sleep(10)

    response = emil_session.get('https://mail.cx/zh/', headers=h1, proxies=proxies)

    # 获取响应中的cookie字典
    cookie_dict = dict_from_cookiejar(response.cookies)

    authorization = cookie_dict['auth_token'].replace('%22', '').replace('%0A', '')

    headers1 = {
        "authority": "mail.cx",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": "bearer " + authorization,
        "referer": "https://mail.cx/zh/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
    }

    url = f"https://mail.cx/api/api/v1/mailbox/{email_be}@{email_af_str}"
    respons = emil_session.get(url, headers=headers1, proxies=proxies)
    print(respons.text)

    # 取邮件中的值
    mid = respons.json()[0]['id']

    # 查看邮箱信息

    headers = {
        "authority": "mail.cx",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "bearer " + authorization,
        "referer": "https://mail.cx/zh/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
    }

    url = f"https://mail.cx/api/api/v1/mailbox/{email}/{mid}/"
    response = emil_session.get(url, headers=headers, proxies=proxies)

    email_code = re.findall(r'请在验证码输入框中输入此次验证码 (\d+) （3分钟内有效）', response.json()['body']['text'])[0]
    return email_code

def regisn(email,email_code,invite_code):
    headers = {
        "authority": "gpt.ciyundata.com",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": "Bearer",
        "content-length": "0",
        "origin": "https://ai.ciyundata.com",
        "referer": "https://ai.ciyundata.com/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"
    }
    url = "https://gpt.ciyundata.com/api/register"
    params = {
        "email": email,
        "password": "88888888",
        "email_code": email_code,
        "invite_code": invite_code
    }
    response = web_session.post(url, headers=headers, params=params, proxies=proxies)

    print(response.json())

def main():
    for i in range(1, 100):
        email_af_str, email_be, email = get_random_email()
        if send_email(email):
            email_code = get_emil_verify_code(email_af_str, email_be, email)
            regisn(email,email_code,"OABGCW")
        else:
            print("发送失败")
            time.sleep(60 * 10)
            continue


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        time.sleep(2)
        main()

# 05fnp8kn@nqmo.com