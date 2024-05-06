#!/usr/bin/env python3
"""A Cache class"""
import uuid
import redis
from typing import Union


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
