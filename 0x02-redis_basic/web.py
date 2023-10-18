#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.StrictRedis()
'''The module-level Redis instance.
'''

def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        # Increment the access count
        access_count_key = f'count:{url}'
        redis_store.incr(access_count_key)
        
        # Check if the data is cached
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # If not cached, fetch and cache the data
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        
        return result

    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.google.com"
    page = get_page(url)
    print(page)
