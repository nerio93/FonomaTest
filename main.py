import hashlib
import os

import redis
from fastapi import Body, FastAPI
from typing import List, Dict

import aioredis
import json

app = FastAPI()

redis_cache = redis.Redis(host=os.environ["redisserver"], port=6379, db=0)


@app.get("/")
async def root():
    return {"message": "I'am root :)"}


@app.post('/solution')
async def process_orders(orders: List = Body(embed=False),
                         criterion: str = Body(embed=False)):
    if criterion is None or criterion not in ["completed", "canceled", "pending", "all"]:
        return {"message": "malformed input"}

    result = 0
    js = dict({"orders": orders, "criterion": criterion})
    key = hashlib.md5(json.dumps(js).encode('utf-8')).hexdigest()
    if redis_cache.exists(key):
        return float(redis_cache.get(key))

    for order in orders:
        if float(order["price"]) <= 0 or order["status"] not in ["completed", "canceled", "pending"]:
            return {"message": "malformed input"}
        if criterion == "all" or order["status"] == criterion:
            result = result + order["price"]
    result = round(result, 2)
    redis_cache.set(key, result)
    return result
