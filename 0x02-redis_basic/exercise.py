#!/usr/bin/env python3
"""A Cache class"""
import uuid
import redis
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    tracks the amount of calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        returns the given method
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    tracks details of calls
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        returns all outputs
        """
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        outp = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, outp)
        return outp
    return invoker


def replay(fn: Callable) -> None:
    """
    Shows the call history
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    input_key = '{}:inputs'.format(fxn_name)
    output_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(input_key, 0, -1)
    fxn_outputs = redis_store.lrange(output_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(fxn_name,
              fxn_input.decode("utf-8"),
              fxn_output))

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
