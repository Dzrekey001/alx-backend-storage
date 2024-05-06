#!/usr/bin/env python3
"""A Cache class"""
import uuid
import redis
from typing import Union, Callable, Optional, Any
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
        Count How many times a method was called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            Wrapper function.
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and
    outputs for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):  # sourcery skip: avoid-builtin-shadow
        """ Wrapper for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    # sourcery skip: use-fstring-for-concatenation, use-fstring-for-formatting
    """
    3. Storing lists
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))

class Cache:
    """Cache class"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string. The method
        should generate a random key (e.g. using uuid), store the
        input data in Redis using the random key and return the key.
        """
        rad_key: str = str(uuid.uuid4())
        self._redis.set(rad_key, data)

        return rad_key

    def get(self, key: str, fn: Optional[Callable[..., Any]] = None
            ) -> Union[str, bytes, int, float]:
        """gets value from redis database"""
        data = self._redis.get(key)

        if fn is not None:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> Union[str, None]:
        """converte data to str"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key) -> Union[int, None]:
        """convert data to int"""
        return self.get(key, lambda x: int(x))
