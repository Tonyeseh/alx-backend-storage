#!/usr/bin/env python3
"""web.py"""
import functools
import redis
import requests
from time import sleep
from typing import Callable

redis_cache = redis.Redis()


def cache_info(method: Callable) -> Callable:
    """caches the methods response and call count"""

    @functools.wraps(method)
    def inner_func(*args, **kwargs):
        """inner function"""
        count_key = "count:{}".format(args[0])
        response_key = "cached:{}".format(args[0])

        redis_cache.incr(count_key)

        if redis_cache.get(response_key) is None:
            redis_cache.setex(response_key, 10, method(*args))

        return redis_cache.get(response_key).decode('utf-8')

    return inner_func


@cache_info
def get_page(url: str) -> str:
    """uses request to obtain the HTML content of
    a particular URL and returns it"""

    return requests.get(url).text
