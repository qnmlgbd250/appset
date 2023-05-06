# -*- coding: utf-8 -*-
import os
import redis
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv(".env")
# 连接Redis数据库
redis_pool = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')), password=os.getenv('REDIS_PASS'))

mylist = redis_pool.lrange('cookieList', 0, -1)
result = [{i:val.decode('utf-8')} for i, val in enumerate(mylist) if val.endswith(b'.com')]
print(result)