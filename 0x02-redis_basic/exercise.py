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
        self = args[0]
        self._redis.incr(key)

        return method(*args)

    return wrapper


def call_history(method: Callable) -> Callable:
    """store the hostory of inputs and outputs for a particular function"""

    @functools.wraps(method)
    def inner_func(*args, **kwargs):
        """inner function"""
        self = args[0]
        result = method(*args)
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args[1:]))
        self._redis.rpush(output_key, result)
        return result

    return inner_func

def replay(method: Callable) -> None:
    """dispay the history of calls of a particular function"""
    r = redis.Redis()

    input_key = method.__qualname__ + ":inputs"
    ouput_key = method.__qualname__ + ":outputs"

    input_lst = r.lrange(input_key, 0, -1)
    output_lst = r.lrange(ouput_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(output_lst)))
    for inp, outp in zip(input_lst, output_lst):
        print("{}(*{}) -> {}".format(method.__qualname__, inp.decode('utf-8'), outp.decode('utf-8')))



class Cache:
    """Cache class"""

    def __init__(self) -> None:
        """Init Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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

    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
