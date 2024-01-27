#!/usr/bin/env python3
"""exercise.py"""

import functools
import redis
from typing import Callable, Union
import uuid

def count_calls(method: Callable) -> Callable:
    """wrapper that counts number of call on methods in Cache"""

    @functools.wraps(method)
    def wrapper():
        """inner function"""


    return wrapper


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        """Init Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str | bytes | int | float) -> str:
        """store input data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
