#!/usr/bin/env python3
"""exercise.py"""

import functools
import redis
from typing import Callable, Optional, Union
import uuid


def count_calls(method: Callable) -> Callable:
    """wrapper that counts number of call on methods in Cache"""

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        """inner function"""
        key = method.__qualname__
        args[0]._redis.incr(key)

        return method(*args)

    return wrapper


class Cache:
    """Cache class"""

    def __init__(self) -> None:
        """Init Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store input data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """get value stored in redis provided the key"""
        value = self._redis.get(key)
        if value and fn:
            value = fn(value)

        return value

    def get_str(value: bytes) -> str:
        """converts bytes to str"""
        return value.decode('utf-8')

    def get_int(value: bytes) -> int:
        """converts bytes to int"""
        return int(value)

if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
