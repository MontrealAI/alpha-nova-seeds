#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures
import re
import runpy
import threading

import requests

_original_request = requests.request
_original_executor = concurrent.futures.ThreadPoolExecutor
_missing_index_tokens: set[str] = set()
_state_lock = threading.Lock()
INSTANCE_RE = re.compile(r"/instances/(\d+)/(holders|transfers)(?:\?|$)")


def synthetic_empty(source_url: str) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response.url = source_url
    response.headers["content-type"] = "application/json"
    response._content = b'{"items":[],"next_page_params":null}'
    response.encoding = "utf-8"
    return response


def request_without_repeating_permanent_blockscout_misses(method, url, **kwargs):
    method_upper = method.upper()
    url_text = str(url)
    match = INSTANCE_RE.search(url_text) if "eth.blockscout.com/api/v2/" in url_text else None
    if method_upper == "GET" and match and match.group(2) == "transfers":
        with _state_lock:
            if match.group(1) in _missing_index_tokens:
                return synthetic_empty(url_text)
    response = _original_request(method, url, **kwargs)
    if method_upper == "GET" and match and response.status_code in (400, 404, 410, 422):
        if match.group(2) == "holders":
            with _state_lock:
                _missing_index_tokens.add(match.group(1))
        return synthetic_empty(response.url)
    return response


class SnapshotExecutor(_original_executor):
    def __init__(self, max_workers=None, *args, **kwargs):
        requested = max_workers or 1
        super().__init__(max_workers=max(requested, 10), *args, **kwargs)


requests.request = request_without_repeating_permanent_blockscout_misses
concurrent.futures.ThreadPoolExecutor = SnapshotExecutor
runpy.run_path(".snapshot/public_snapshot.py", run_name="__main__")
