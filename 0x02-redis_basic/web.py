#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''

import requests
import time
from functools import lru_cache

@lru_cache(maxsize=None, typed=True)
def get_page(url: str) -> str:
    # Check if the URL was accessed before
    access_count_key = f"count:{url}"
    access_count = int(requests.get(f'http://localhost:8081/access?path={access_count_key}').text) + 1

    # Cache the result with an expiration time of 10 seconds
    result = requests.get(url).text
    requests.get(f'http://localhost:8081/access?path={access_count_key}&value={access_count}', data=dict(content=result))
    return result

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.google.com"
    start_time = time.time()
    page = get_page(url)
    end_time = time.time()
    print(page)
    print(f"Time taken: {end_time - start_time} seconds")
