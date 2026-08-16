#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import time
import zipfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

import requests

CHAIN_ID = 1
CONTRACT = '0x495f947276749ce646f68ac8c248420045cb7b5e'
CREATOR = '0x054a2e4b3b5ea2c62372e92358fdf7fb74b4f34a'
CREATOR_INT = int(CREATOR, 16)
COUNT = 556
OUT = Path('snapshot-output')
RPCS = ['https://ethereum-rpc.publicnode.com', 'https://eth.drpc.org']
BLOCKSCOUT = 'https://eth.blockscout.com/api/v2'
ADDR_RE = re.compile(r'0x[a-fA-F0-9]{40}')
OWNED_BY_RE = re.compile(r'Owned by(?:<!-- -->)?\s*</span><a[^>]{0,1000}href="/(0x[a-fA-F0-9]{40})"', re.S)
OWNER_JSON_RE = re.compile(r'"owner":\{"address":"(0x[a-fA-F0-9]{40})"')
SELLER_RE = re.compile(r'"seller":\{"@type":"Person","name":"(0x[a-fA-F0-9]{40})"')


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')


def write_csv(path: Path, fields: list[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def request_json(method: str, url: str, *, params=None, body=None, attempts=5, timeout=60, missing_ok=False):
    last = None
    for i in range(attempts):
        try:
            r = requests.request(method, url, params=params, json=body, timeout=timeout,
                                 headers={'user-agent': 'MONTREAL-AI-Becoming-Omega-Snapshot/1.0', 'accept': 'application/json'})
            if missing_ok and r.status_code in (400, 404, 410, 422):
                return {'items': [], 'next_page_params': None}
            if r.status_code in (408, 425, 429) or r.status_code >= 500:
                time.sleep(min(15, .8 * 2 ** i))
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            if i + 1 < attempts:
                time.sleep(min(15, .8 * 2 ** i))
    raise RuntimeError(f'{method} {url} failed: {last}')


def rpc(url: str, method: str, params: list[Any], rid=1):
    p = request_json('POST', url, body={'jsonrpc': '2.0', 'id': rid, 'method': method, 'params': params})
    if p.get('error'):
        raise RuntimeError(f'{url} {method}: {p["error"]}')
    return p.get('result')


def freeze_block():
    heads = []
    for u in RPCS:
        b = rpc(u, 'eth_getBlockByNumber', ['finalized', False])
        heads.append({'rpc_url': u, 'number': int(b['number'], 16), 'hash': b['hash'].lower(), 'timestamp': int(b['timestamp'], 16)})
    number = min(x['number'] for x in heads)
    selected = []
    for u in RPCS:
        b = rpc(u, 'eth_getBlockByNumber', [hex(number), False])
        selected.append({'rpc_url': u, 'number': int(b['number'], 16), 'hash': b['hash'].lower(), 'timestamp': int(b['timestamp'], 16)})
    if len({x['hash'] for x in selected}) != 1 or len({x['timestamp'] for x in selected}) != 1:
        raise RuntimeError(f'RPC block disagreement: {selected}')
    ts = selected[0]['timestamp']
    dt = datetime.fromtimestamp(ts, timezone.utc)
    return {'chain': 'ethereum', 'chain_id': 1, 'block_tag_used': 'finalized', 'block_number': number, 'block_number_hex': hex(number),
            'block_hash': selected[0]['hash'], 'block_timestamp_unix': ts, 'block_timestamp_utc': dt.isoformat().replace('+00:00', 'Z'),
            'block_timestamp_montreal': dt.astimezone(ZoneInfo('America/Montreal')).isoformat(),
            'selection_rule': 'Minimum finalized height reported by two independent public Ethereum RPC endpoints, cross-checked by block hash and timestamp.',
            'providers_at_freeze': heads, 'providers_cross_check': selected, 'frozen_at_utc': now()}


def manifest_items():
    nonces = [n for n in range(4, 563) if n not in {159, 495, 523}]
    assert len(nonces) == COUNT
    nonces[258], nonces[259] = nonces[259], nonces[258]
    items = []
    for canonical, nonce in enumerate(nonces):
        token = (CREATOR_INT << 96) | (nonce << 40) | 1
        dec = str(token)
        hx = '0x' + token.to_bytes(32, 'big').hex()
        raw = 316 if canonical == 317 else canonical
        items.append({'manifest_index': canonical + 1, 'canonical_number': canonical, 'canonical_number_raw': raw,
          'title': f'Crypto AI Art #{canonical:03d}', 'title_raw': f'Crypto AI Art #{raw:03d}', 'chain': 'ethereum', 'chain_id': 1,
          'contract': CONTRACT, 'token_standard': 'erc1155', 'token_id_decimal': dec, 'token_id_hex': hx,
          'encoded_creator': CREATOR, 'creation_nonce': str(nonce), 'encoded_supply': '1',
          'opensea_url': f'https://opensea.io/item/ethereum/{CONTRACT}/{dec}',
          'metadata_url': f'https://api.opensea.io/api/v1/metadata/{CONTRACT}/{hx}',
          'canonical_reconciliation': ('Historical metadata at creation nonce 322 says #316; sequence neighbors #316/#318 and the complete #000-#555 canon deterministically reconcile it to #317.' if canonical == 317 else None)})
    assert len({x['token_id_decimal'] for x in items}) == COUNT
    assert [x['canonical_number'] for x in items] == list(range(COUNT))
    assert items[319]['token_id_decimal'] == '2392630434290240917728431095880785304289144848761899072947382792323770351617'
    return items


def fetch_owner(item):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
               'accept': 'text/html,application/xhtml+xml', 'cache-control': 'no-cache'}
    status = None
    text = ''
    err = None
    for i in range(4):
        try:
            r = requests.get(item['opensea_url'], headers=headers, timeout=45)
            status = r.status_code
            if status in (408, 425, 429) or status >= 500:
                time.sleep(min(8, .8 * 2 ** i))
                continue
            if status in (400, 404, 410, 422):
                break
            r.raise_for_status()
            text = r.text
            break
        except Exception as e:
            err = f'{type(e).__name__}: {e}'
            if i < 3:
                time.sleep(min(8, .8 * 2 ** i))
    owner = None
    source = None
    for p, s in ((OWNED_BY_RE, 'owned_by_link'), (OWNER_JSON_RE, 'item_owner_json'), (SELLER_RE, 'schema_seller')):
        m = p.search(text)
        if m:
            owner = m.group(1).lower()
            source = s
            break
    return {'token_id_decimal': item['token_id_decimal'], 'owner_hint': owner, 'owner_hint_source': source,
            'http_status': status, 'html_bytes': len(text.encode()), 'page_addresses': sorted({a.lower() for a in ADDR_RE.findall(text)}),
            'error': err}


def balance_data(owner: str, token: str):
    return '0x00fdd58e' + owner[2:].rjust(64, '0') + int(token).to_bytes(32, 'big').hex()


def batch_balances(url: str, pairs: list[tuple[str, str]], block_hex: str):
    values = {}
    errors = []
    rid = 1
    for start in range(0, len(pairs), 100):
        chunk = pairs[start:start + 100]
        req = []
        ids = {}
        for token, owner in chunk:
            ids[rid] = (token, owner)
            req.append({'jsonrpc': '2.0', 'id': rid, 'method': 'eth_call', 'params': [{'to': CONTRACT, 'data': balance_data(owner, token)}, block_hex]})
            rid += 1
        try:
            rows = request_json('POST', url, body=req, attempts=5, timeout=90)
            if not isinstance(rows, list):
                raise RuntimeError('batch response not list')
        except Exception as e:
            rows = []
            for q in req:
                try:
                    rows.append({'id': q['id'], 'result': rpc(url, q['method'], q['params'], q['id'])})
                except Exception as x:
                    rows.append({'id': q['id'], 'error': str(x)})
            errors.append({'scope': 'batch_recovered', 'start': start, 'warning': str(e)})
        for row in rows:
            key = ids.get(row.get('id'))
            if not key:
                continue
            if row.get('error'):
                errors.append({'token_id_decimal': key[0], 'owner': key[1], 'error': row['error']})
                continue
            try:
                values[key] = int(row['result'], 16)
            except Exception:
                errors.append({'token_id_decimal': key[0], 'owner': key[1], 'error': f'invalid result {row.get("result")}'})
    return values, errors


def recursive_addresses(obj: Any):
    out = set()
    if isinstance(obj, dict):
        for v in obj.values():
            out |= recursive_addresses(v)
    elif isinstance(obj, list):
        for v in obj:
            out |= recursive_addresses(v)
    elif isinstance(obj, str) and re.fullmatch(r'0x[a-fA-F0-9]{40}', obj):
        out.add(obj.lower())
    return out


def blockscout_candidates(token: str, seeds: set[str]):
    addresses = set(seeds)
    diagnostics = []
    for suffix in ('holders', 'transfers'):
        params = None
        seen = set()
        count = 0
        for _ in range(100):
            p = request_json('GET', f'{BLOCKSCOUT}/tokens/{CONTRACT}/instances/{token}/{suffix}', params=params, attempts=3, missing_ok=True)
            addresses |= recursive_addresses(p)
            count += len(p.get('items') or [])
            nxt = p.get('next_page_params')
            if not nxt:
                break
            params = {k: v for k, v in nxt.items() if v is not None}
            sig = urlencode(sorted((str(k), str(v)) for k, v in params.items()))
            if sig in seen:
                break
            seen.add(sig)
        diagnostics.append({'endpoint': suffix, 'items': count})
    addresses -= {CONTRACT, '0x0000000000000000000000000000000000000000'}
    return addresses, diagnostics


def holdings_from(values):
    return [{'token_id_decimal': t, 'owner': o, 'balance': str(v)} for (t, o), v in values.items() if v > 0]


def totals(holdings):
    d = defaultdict(int)
    for h in holdings:
        d[h['token_id_decimal']] += int(h['balance'])
    return d


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    started = now()
    block = freeze_block()
    dump(OUT / 'snapshot_block.json', block)
    items = manifest_items()
    item_by_token = {x['token_id_decimal']: x for x in items}
    print(f'Frozen finalized block {block["block_number"]} at {block["block_timestamp_utc"]}', flush=True)
    hints = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        fut = [pool.submit(fetch_owner, x) for x in items]
        for i, f in enumerate(as_completed(fut), 1):
            hints.append(f.result())
            if i % 50 == 0 or i == COUNT:
                print(f'Owner hints {i}/{COUNT}', flush=True)
    hint_by_token = {x['token_id_decimal']: x for x in hints}
    current_owners = {x['owner_hint'] for x in hints if x['owner_hint']}
    candidates = {x['token_id_decimal']: {CREATOR} | ({hint_by_token[x['token_id_decimal']]['owner_hint']} if hint_by_token[x['token_id_decimal']]['owner_hint'] else set()) for x in items}
    pairs = sorted((t, a) for t, aa in candidates.items() for a in aa)
    values, errors = batch_balances(RPCS[0], pairs, block['block_number_hex'])
    holdings = holdings_from(values)
    unresolved = [t for t in candidates if totals(holdings)[t] != 1]
    print(f'Initial unresolved {len(unresolved)}', flush=True)
    fallback_diag = []
    if unresolved:
        with ThreadPoolExecutor(max_workers=12) as pool:
            fs = {pool.submit(blockscout_candidates, t, candidates[t]): t for t in unresolved}
            for f in as_completed(fs):
                t = fs[f]
                try:
                    candidates[t], d = f.result()
                    fallback_diag.append({'token_id_decimal': t, 'diagnostics': d, 'candidate_count': len(candidates[t])})
                except Exception as e:
                    fallback_diag.append({'token_id_decimal': t, 'error': str(e), 'candidate_count': len(candidates[t])})
        p = sorted((t, a) for t in unresolved for a in candidates[t])
        v, e = batch_balances(RPCS[0], p, block['block_number_hex'])
        values.update(v)
        errors += e
        holdings = holdings_from(values)
        unresolved = [t for t in candidates if totals(holdings)[t] != 1]
        print(f'After explorer fallback unresolved {len(unresolved)}', flush=True)
    if unresolved:
        all_owner_hints = set(current_owners)
        for t in unresolved:
            candidates[t] |= all_owner_hints | set(hint_by_token[t]['page_addresses'])
            candidates[t] -= {CONTRACT, '0x0000000000000000000000000000000000000000'}
        p = sorted((t, a) for t in unresolved for a in candidates[t])
        v, e = batch_balances(RPCS[0], p, block['block_number_hex'])
        values.update(v)
        errors += e
        holdings = holdings_from(values)
        unresolved = [t for t in candidates if totals(holdings)[t] != 1]
        print(f'After broad fallback unresolved {len(unresolved)}', flush=True)
    positive_pairs = sorted((h['token_id_decimal'], h['owner']) for h in holdings)
    verify, verify_errors = batch_balances(RPCS[1], positive_pairs, block['block_number_hex'])
    mismatches = [{'token_id_decimal': t, 'owner': a, 'provider_a': values.get((t, a)), 'provider_b': verify.get((t, a))} for t, a in positive_pairs if values.get((t, a)) != verify.get((t, a))]
    for h in holdings:
        r = item_by_token[h['token_id_decimal']]
        h.update({'chain_id': 1, 'block_number': block['block_number'], 'block_hash': block['block_hash'], 'contract': CONTRACT, 'canonical_number': r['canonical_number'], 'title': r['title'], 'encoded_supply': '1'})
    holdings.sort(key=lambda x: (x['canonical_number'], x['owner']))
    ttot = totals(holdings)
    token_audit = [{'canonical_number': r['canonical_number'], 'token_id_decimal': r['token_id_decimal'], 'expected_supply': '1', 'holder_row_count': sum(1 for h in holdings if h['token_id_decimal'] == r['token_id_decimal']), 'accounted_balance': str(ttot[r['token_id_decimal']]), 'status': 'ok' if ttot[r['token_id_decimal']] == 1 else 'unresolved'} for r in items]
    wallet = {}
    for h in holdings:
        w = wallet.setdefault(h['owner'], {'wallet': h['owner'], 'distinct_genesis_tokens': 0, 'total_genesis_units': 0, 'canonical_numbers': [], 'category': 'creator' if h['owner'] == CREATOR else 'holder'})
        w['distinct_genesis_tokens'] += 1
        w['total_genesis_units'] += int(h['balance'])
        w['canonical_numbers'].append(h['canonical_number'])
    wallets = []
    for w in wallet.values():
        w['canonical_numbers'] = ','.join(map(str, sorted(w['canonical_numbers'])))
        wallets.append(w)
    wallets.sort(key=lambda x: (-x['total_genesis_units'], x['wallet']))
    canonical = '\n'.join(f"{r['canonical_number']}|{r['contract']}|{r['token_id_decimal']}|1" for r in items) + '\n'
    root = hashlib.sha256(canonical.encode()).hexdigest()
    manifest = {'schema': 'montrealai.becoming.genesis-manifest.v1', 'collection_slug': 'montrealai', 'chain_id': 1, 'contract': CONTRACT, 'creator': CREATOR, 'expected_count': COUNT, 'actual_count': len(items), 'canonical_numbering': '#000 through #555', 'manifest_sha256_canonical_rows': root, 'generated_at_utc': now(), 'items': items}
    critical_errors = [e for e in errors if e.get('scope') != 'batch_recovered'] + verify_errors
    status = 'PASS' if not unresolved and not mismatches and not critical_errors and sum(int(h['balance']) for h in holdings) == COUNT else 'FAIL'
    audit = {'schema': 'montrealai.becoming.snapshot-audit.v1', 'status': status, 'started_at_utc': started, 'completed_at_utc': now(), 'snapshot_block': block,
             'manifest': {'expected_items': COUNT, 'actual_items': len(items), 'unique_token_ids': len({r['token_id_decimal'] for r in items}), 'canonical_numbers_complete': True, 'canonical_rows_sha256': root,
               'historical_metadata_anomaly': {'creation_nonce': 322, 'token_id_decimal': items[317]['token_id_decimal'], 'raw_title': 'Crypto AI Art #316', 'reconciled_title': 'Crypto AI Art #317'}},
             'ownership': {'holding_rows': len(holdings), 'unique_wallets': len(wallets), 'total_accounted_units': sum(int(h['balance']) for h in holdings), 'creator_held_tokens': sum(1 for h in holdings if h['owner'] == CREATOR), 'unresolved_token_ids': unresolved, 'provider_mismatches': mismatches, 'critical_rpc_errors': critical_errors, 'recovered_batch_warnings': [e for e in errors if e.get('scope') == 'batch_recovered']},
             'method': {'enumeration': 'Creator-encoded Shared Storefront nonce set 4..562 excluding 159,495,523, with canonical #258/#259 creation-order swap, verified against legacy OpenSea metadata.', 'candidate_hints': 'Public OpenSea item HTML; no API key.', 'authority': 'ERC-1155 balanceOf(address,uint256) at the frozen finalized block.', 'cross_check': 'Every positive balance repeated through an independent public RPC.'}}
    dump(OUT / 'genesis_manifest_v1.json', manifest)
    write_csv(OUT / 'genesis_manifest_v1.csv', list(items[0].keys()), items)
    dump(OUT / 'snapshot_owner_hint_diagnostics.json', {'rows': sorted(hints, key=lambda x: int(x['token_id_decimal'])), 'targeted_fallback': fallback_diag})
    dump(OUT / 'snapshot_token_holdings.json', {'schema': 'montrealai.becoming.snapshot-token-holdings.v1', 'snapshot_block': block, 'rows': holdings})
    write_csv(OUT / 'snapshot_token_holdings.csv', ['chain_id', 'block_number', 'block_hash', 'contract', 'canonical_number', 'title', 'token_id_decimal', 'owner', 'balance', 'encoded_supply'], holdings)
    dump(OUT / 'snapshot_wallet_summary.json', {'schema': 'montrealai.becoming.snapshot-wallet-summary.v1', 'snapshot_block': block, 'wallets': wallets})
    write_csv(OUT / 'snapshot_wallet_summary.csv', ['wallet', 'distinct_genesis_tokens', 'total_genesis_units', 'category', 'canonical_numbers'], wallets)
    write_csv(OUT / 'snapshot_token_audit.csv', ['canonical_number', 'token_id_decimal', 'expected_supply', 'holder_row_count', 'accounted_balance', 'status'], token_audit)
    dump(OUT / 'snapshot_audit_report.json', audit)
    readme = f'''# MONTREAL.AI — BECOMING Ω: THE FINAL 444\n\n## Genesis 556 finalized-block ownership snapshot\n\n- Legacy contract: `{CONTRACT}`\n- Canonical works: **556**, numbered **#000–#555**\n- Finalized block: **{block['block_number']}**\n- Block hash: `{block['block_hash']}`\n- UTC: **{block['block_timestamp_utc']}**\n- Montréal: **{block['block_timestamp_montreal']}**\n- Positive token-holder rows: **{len(holdings)}**\n- Unique wallets: **{len(wallets)}**\n- Accounted units: **{sum(int(h['balance']) for h in holdings)}**\n- Audit: **{status}**\n\nOwnership is the ERC-1155 `balanceOf` result at the frozen finalized block. OpenSea pages were used only as no-key candidate hints; every positive result was repeated through a second public Ethereum RPC.\n'''
    (OUT / 'README.md').write_text(readme, encoding='utf-8')
    (OUT / 'snapshot.py').write_text(Path(__file__).read_text(), encoding='utf-8')
    targets = sorted(p for p in OUT.iterdir() if p.is_file() and p.name not in {'SHA256SUMS', 'montrealai-becoming-omega-genesis-556-snapshot.zip'})
    (OUT / 'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in targets), encoding='utf-8')
    zpath = OUT / 'montrealai-becoming-omega-genesis-556-snapshot.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(OUT.iterdir()):
            if p.is_file() and p != zpath:
                z.write(p, p.name)
    result = {'status': status, 'block_number': block['block_number'], 'block_hash': block['block_hash'], 'block_timestamp_utc': block['block_timestamp_utc'], 'manifest_items': len(items), 'holding_rows': len(holdings), 'unique_wallets': len(wallets), 'total_units': sum(int(h['balance']) for h in holdings), 'creator_held_tokens': audit['ownership']['creator_held_tokens'], 'unresolved': len(unresolved), 'zip_sha256': sha(zpath)}
    print(json.dumps(result, indent=2), flush=True)
    if status != 'PASS':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
