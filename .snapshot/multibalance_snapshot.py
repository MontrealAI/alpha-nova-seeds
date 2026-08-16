#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

SCRIPT = Path('.snapshot/quick_snapshot.py')
spec = importlib.util.spec_from_file_location('quick_snapshot_core', SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load quick_snapshot.py')
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)

_original_batch = q.batch_balances
_original_freeze = q.freeze_block
_original_fetch_owner = q.fetch_owner
_creator_held: set[str] = set()
SELECTOR = '4e1273f4'


def encode_balance_of_batch(owner: str, tokens: list[str]) -> str:
    n = len(tokens)
    accounts_offset = 64
    ids_offset = 96 + 32 * n
    words = [accounts_offset, ids_offset, n]
    words.extend(int(owner, 16) for _ in tokens)
    words.append(n)
    words.extend(int(token) for token in tokens)
    return '0x' + SELECTOR + ''.join(int(word).to_bytes(32, 'big').hex() for word in words)


def decode_uint_array(result: str, expected: int) -> list[int]:
    raw = bytes.fromhex(result[2:])
    offset = int.from_bytes(raw[:32], 'big')
    length = int.from_bytes(raw[offset:offset + 32], 'big')
    if length != expected:
        raise RuntimeError(f'balanceOfBatch length {length} != {expected}')
    start = offset + 32
    return [int.from_bytes(raw[start + 32 * i:start + 32 * (i + 1)], 'big') for i in range(length)]


def grouped_balances(url: str, pairs: list[tuple[str, str]], block_hex: str):
    groups: dict[str, list[str]] = defaultdict(list)
    for token, owner in pairs:
        if token not in groups[owner]:
            groups[owner].append(token)
    tasks = []
    for owner, tokens in groups.items():
        for i in range(0, len(tokens), 200):
            tasks.append((owner, tokens[i:i + 200]))
    values = {}
    errors = []

    def query(owner, tokens):
        data = encode_balance_of_batch(owner, tokens)
        result = q.rpc(url, 'eth_call', [{'to': q.CONTRACT, 'data': data}, block_hex])
        return owner, tokens, decode_uint_array(result, len(tokens))

    failed = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(query, owner, tokens): (owner, tokens) for owner, tokens in tasks}
        for future in as_completed(futures):
            owner, tokens = futures[future]
            try:
                _, _, balances = future.result()
                for token, value in zip(tokens, balances):
                    values[(token, owner)] = value
            except Exception as exc:
                failed.extend((token, owner) for token in tokens)
                errors.append({'scope': 'balanceOfBatch_fallback', 'owner': owner, 'token_count': len(tokens), 'warning': str(exc)})
    if failed:
        fallback_values, fallback_errors = _original_batch(url, failed, block_hex)
        values.update(fallback_values)
        errors.extend(fallback_errors)
    return values, errors


def freeze_and_prefetch_creator_balances():
    block = _original_freeze()
    items = q.manifest_items()
    pairs = [(item['token_id_decimal'], q.CREATOR) for item in items]
    values, errors = grouped_balances(q.RPCS[0], pairs, block['block_number_hex'])
    _creator_held.update(token for token, owner in pairs if values.get((token, owner)) == 1)
    print(f'Creator balanceOfBatch pre-pass: {len(_creator_held)}/{len(items)} resolved; {len(errors)} fallback diagnostics', flush=True)
    return block


def indexed_owner_hint(item):
    token = item['token_id_decimal']
    if token in _creator_held:
        return {'token_id_decimal': token, 'owner_hint': q.CREATOR, 'owner_hint_source': 'creator_balance_at_snapshot_block',
                'http_status': None, 'html_bytes': 0, 'page_addresses': [q.CREATOR], 'error': None}
    url = f'{q.BLOCKSCOUT}/tokens/{q.CONTRACT}/instances/{token}/holders'
    try:
        r = requests.get(url, headers={'accept': 'application/json', 'user-agent': 'MONTREAL-AI-Becoming-Omega-Snapshot/1.0'}, timeout=12)
        if r.status_code == 200:
            payload = r.json()
            addresses = q.recursive_addresses(payload) - {q.CONTRACT, q.CREATOR, '0x0000000000000000000000000000000000000000'}
            if addresses:
                owner = sorted(addresses)[0]
                return {'token_id_decimal': token, 'owner_hint': owner, 'owner_hint_source': 'blockscout_current_holder',
                        'http_status': r.status_code, 'html_bytes': len(r.content), 'page_addresses': sorted(addresses), 'error': None}
    except Exception:
        pass
    return _original_fetch_owner(item)


q.batch_balances = grouped_balances
q.freeze_block = freeze_and_prefetch_creator_balances
q.fetch_owner = indexed_owner_hint
q.main()
