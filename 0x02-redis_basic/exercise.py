#!/usr/bin/env python3
"""A Cache class"""
import uuid
import redis
from typing import Union, Callable, Optional, Any


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
