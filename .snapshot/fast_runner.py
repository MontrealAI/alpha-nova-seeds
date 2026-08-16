#!/usr/bin/env python3
from __future__ import annotations

import runpy

import requests

_original_request = requests.request


def request_without_repeating_permanent_blockscout_misses(method, url, **kwargs):
    response = _original_request(method, url, **kwargs)
    if method.upper() == "GET" and "eth.blockscout.com/api/v2/" in str(url) and response.status_code in (400, 404, 410, 422):
        synthetic = requests.Response()
        synthetic.status_code = 200
        synthetic.url = response.url
        synthetic.headers["content-type"] = "application/json"
        synthetic._content = b'{"items":[],"next_page_params":null}'
        synthetic.encoding = "utf-8"
        return synthetic
    return response


requests.request = request_without_repeating_permanent_blockscout_misses
runpy.run_path(".snapshot/public_snapshot.py", run_name="__main__")
