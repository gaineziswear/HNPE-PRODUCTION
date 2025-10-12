import aioredis
import os

REDIS_URL = os.getenv('REDIS_URL') or "redis://redis:6379/0"
redis = None

async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url(REDIS_URL)
    return redis
