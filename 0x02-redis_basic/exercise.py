#!/usr/bin/env python3
"""exercise.py"""

import redis
import uuid


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
