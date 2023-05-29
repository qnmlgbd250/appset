# -*- coding: utf-8 -*-
import os
import redis
import json

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
# 连接Redis数据库
host = os.getenv('REDIS_HOST')
port = int(os.getenv('REDIS_PORT'))
db = int(os.getenv('REDIS_DB'))
password = os.getenv('REDIS_PASS')
print(host, port, db, password)
redis_pool = redis.Redis(host=host, port=port, db=db, password=password)
def reset_counts():
    for key in redis_pool.hkeys("hash_db"):
        value = redis_pool.hget("hash_db", key)
        if value:
            value_dict = json.loads(value)
            value_dict["count"] = 50
            redis_pool.hset("hash_db", key, json.dumps(value_dict))

if __name__ == '__main__':
    reset_counts()