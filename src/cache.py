import redis
from .config import settings
from functools import wraps
from fastapi import HTTPException

redis_client = redis.Redis.from_url(settings.redis_url)

def cache_redirect(expire: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(short_code: str, *args, **kwargs):
            # Try to get from cache
            cached_url = redis_client.get(f"redirect:{short_code}")
            if cached_url:
                return {"url": cached_url.decode()}
            
            # Call original function
            result = func(short_code, *args, **kwargs)
            
            # Cache the result
            if "url" in result:
                redis_client.setex(f"redirect:{short_code}", expire, result["url"])
            
            return result
        return wrapper
    return decorator