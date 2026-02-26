import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.from_url(os.getenv("REDIS_URL"))

def get_cached_url(short_code: str):
    return redis_client.get(short_code)

def set_cached_url(short_code: str, original_url: str):
    redis_client.set(short_code, original_url, ex=3600)  # expires in 1 hour