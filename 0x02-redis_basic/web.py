#!/usr/bin/env python3
"""Web cache
"""
import requests
import redis
from typing import Callable
from functools import wraps


redis_instance = redis.Redis()


def count_url_calls(method: Callable) -> Callable:
    """Count number of url calls and set expiration

    Args:
        method (Callable): method to count

    Returns:
        Callable: method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = redis_instance.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        redis_instance.incr(count_key)
        redis_instance.set(cached_key, html)
        redis_instance.expire(cached_key, 10)
        return html
    return wrapper


@count_url_calls
def get_page(url: str) -> str:
    """_summary_

    Args:
        url (str): url to request html

    Returns:
        str: html string
    """
    response = requests.get(url).text
    return response
