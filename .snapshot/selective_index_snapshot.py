#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import requests

SCRIPT = Path('.snapshot/quick_snapshot.py')
spec = importlib.util.spec_from_file_location('quick_snapshot_core', SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load quick_snapshot.py')
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)

_original_freeze = q.freeze_block
_original_fetch_owner = q.fetch_owner
_creator_held: set[str] = set()


def freeze_and_prefetch_creator_balances():
    block = _original_freeze()
    items = q.manifest_items()
    pairs = [(item['token_id_decimal'], q.CREATOR) for item in items]
    values, errors = q.batch_balances(q.RPCS[0], pairs, block['block_number_hex'])
    _creator_held.update(token for token, owner in pairs if values.get((token, owner)) == 1)
    print(f'Creator balance pre-pass: {len(_creator_held)}/{len(items)} resolved; {len(errors)} pre-pass diagnostics', flush=True)
    return block


def indexed_owner_hint(item):
    token = item['token_id_decimal']
    if token in _creator_held:
        return {'token_id_decimal': token, 'owner_hint': q.CREATOR, 'owner_hint_source': 'creator_balance_at_snapshot_block',
                'http_status': None, 'html_bytes': 0, 'page_addresses': [q.CREATOR], 'error': None}
    url = f'{q.BLOCKSCOUT}/tokens/{q.CONTRACT}/instances/{token}/holders'
    try:
        r = requests.get(url, headers={'accept': 'application/json', 'user-agent': 'MONTREAL-AI-Becoming-Omega-Snapshot/1.0'}, timeout=25)
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


q.freeze_block = freeze_and_prefetch_creator_balances
q.fetch_owner = indexed_owner_hint
q.main()
