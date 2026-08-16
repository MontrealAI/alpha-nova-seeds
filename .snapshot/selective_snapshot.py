#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

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
    print(f'Creator balance pre-pass: {len(_creator_held)}/{len(items)} tokens resolved; {len(errors)} non-fatal pre-pass diagnostics', flush=True)
    return block


def fetch_only_when_creator_does_not_hold(item):
    token = item['token_id_decimal']
    if token in _creator_held:
        return {'token_id_decimal': token, 'owner_hint': q.CREATOR, 'owner_hint_source': 'creator_balance_at_snapshot_block',
                'http_status': None, 'html_bytes': 0, 'page_addresses': [q.CREATOR], 'error': None}
    return _original_fetch_owner(item)


q.freeze_block = freeze_and_prefetch_creator_balances
q.fetch_owner = fetch_only_when_creator_does_not_hold
q.main()
