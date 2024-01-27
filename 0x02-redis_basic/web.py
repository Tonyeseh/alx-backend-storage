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
        count_key = "count: {}".format(args[0])
        response_key = "reponse: {}".format(args[0])

        redis_cache.incr(count_key)

        if redis_cache.get(response_key) is None:
            print("printing non cached value")
            redis_cache.set(response_key, method(*args), 10)
        print("printing cached value")

        return redis_cache.get(response_key)

    return inner_func


@cache_info
def get_page(url: str) -> str:
    """uses request to obtain the HTML content of a particular URL and returns it"""

    return requests.get(url).text


if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))

    sleep(1)
    print(get_page('http://slowwly.robertomurray.co.uk'))

    sleep(10)

    print(get_page('http://slowwly.robertomurray.co.uk'))
