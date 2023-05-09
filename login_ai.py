import requests
import json
# from acc import *
import redis
import os
import dotenv
from dotenv import load_dotenv
acclist = [] # 用于存放账号
# 加载 .env 文件
load_dotenv(".env")
# 连接Redis数据库
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))
proxies = {
  'http': 'http://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068',
  # 'https': 'https://taxtask:UQwpzAZ+WiQb@proxy.kdzwy.com:9068'
}
def get_accounts():
    batch_size = 100  # 每个批次的大小
    last_index_key = 'last_index'  # 存储上一个批次结束的索引的Redis键名

    # 获取上一个批次结束的索引值
    last_index = int(r.get(last_index_key) or -1)
    if last_index == 999:
        last_index = -1

    # 计算这一批次的起始和结束索引
    start_index = last_index + 1
    end_index = start_index + batch_size - 1

    # 从Redis中获取对应的账号信息
    accounts = []
    for i in range(start_index, end_index + 1):
        account = r.lindex('emailList', i)
        if account is not None:
            accounts.append({i: account.decode('utf-8')})

    # 处理账号信息...
    print(f"调用一批账号信息，起始索引: {start_index}，结束索引: {end_index}")
    print(f"账号信息: {accounts}")


    # 将结束索引存回Redis中
    r.set(last_index_key, end_index)
    return accounts

def _login(index_ac,ac):
    try:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://ai.usesless.com",
            "Referer": "https://ai.usesless.com/login",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://ai.usesless.com/api/cms/auth/local"
        data = {
            "identifier": ac,
            "password": "88888888"
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=headers, data=data, proxies=proxies)
        token = response.json()['jwt']
        print(token)
        r.lset('cookieList', index_ac, token)
    except Exception as e:
        print(e)
        r.lset('cookieList', index_ac, ac)

if __name__ == '__main__':
    acclist = get_accounts()
    for ac_dic in acclist:
        for key in ac_dic:
            _login(key,ac_dic[key])
    # _login(0,'sosvoao@nqmo.com')