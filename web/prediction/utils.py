from django.http import HttpResponse
import redis
import os

def redis_connection() :
    try :
        r = redis.StrictRedis.from_url(
            url=os.environ.get("REDIS_URL"),
            decode_responses=True
        )
        return r
    
    except ConnectionError:
        return HttpResponse("Redis server is currently unavailable. Please try again later.")
