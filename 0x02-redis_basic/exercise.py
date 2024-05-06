#!/usr/bin/env python3
"""A Cache class"""
import uuid
import redis
from typing import Union, Callable, Optional, Any
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Count number of method calls

    Args:
        method (Callable): _description_

    Returns:
        Callable: method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap the decorated function and return the wrapper."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrap the decorated function and return the wrapper."""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


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
