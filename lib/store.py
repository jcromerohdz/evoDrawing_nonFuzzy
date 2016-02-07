import os
import redis

REDISTOGO_URL ='redis://redistogo:ef633f5cb7aa5f7e0330a3447970a78c@chubb.redistogo.com:9739/'
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)