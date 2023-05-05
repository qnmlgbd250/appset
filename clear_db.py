# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 0:18
# @Author  : huni
# @Email   : zcshiyonghao@163.com
# @File    : clear_db.py
# @Software: PyCharm
import os
import redis

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv(".env")
# 连接Redis数据库
redis_pool = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))

# 获取列表的所有元素，并将其转换为字符串类型
for _ in range(1000):
    redis_pool.rpush('cookieList', '')  # 添加一个空元素