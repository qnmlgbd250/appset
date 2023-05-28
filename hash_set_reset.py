# -*- coding: utf-8 -*-

import redis
import json
import schedule
import time
from datetime import datetime, timedelta

# 连接到Redis服务器
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# 定义一个函数用于设置哈希值和重置计数器
def set_hash(key, token, count):
    value = {"token": token, "count": count}
    r.hset("hash_key", key, json.dumps(value))

# 定义一个函数用于获取哈希值并减少计数器
def get_hash_and_decrease_count(key):
    value = r.hget("hash_key", key)
    if value:
        value_dict = json.loads(value)
        if value_dict["count"] > 0:
            value_dict["count"] -= 1
            r.hset("hash_key", key, json.dumps(value_dict))
            return value_dict
    return None

# 定义一个函数用于在每天00:00时重置所有哈希值中的count为50
def reset_counts():
    for key in r.hkeys("hash_key"):
        value = r.hget("hash_key", key)
        if value:
            value_dict = json.loads(value)
            value_dict["count"] = 50
            r.hset("hash_key", key, json.dumps(value_dict))

# 设置哈希值示例：
key = "o165g643@qabq.com"
token = "qqtt"
count = 50

set_hash(key, token, count)

# 获取哈希值并减少计数器示例：
result = get_hash_and_decrease_count(key)
print(result)

# 使用schedule库设置每天00:00执行reset_counts函数
schedule.every().day.at("20:39").do(reset_counts)

# 主循环，检查是否到了执行任务的时间
while True:
    schedule.run_pending()
    time.sleep(1)


