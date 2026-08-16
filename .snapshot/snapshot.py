#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import threading
import time
import zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

import requests

COLLECTION_SLUG = "montrealai"
CHAIN = "ethereum"
CHAIN_ID = 1
CONTRACT = "0x495f947276749ce646f68ac8c248420045cb7b5e"
CREATOR = "0x054a2e4b3b5ea2c62372e92358fdf7fb74b4f34a"
EXPECTED_COUNT = 556
OUTPUT = Path("snapshot-output")
OPEN_SEA_API = "https://api.opensea.io/api/v2"
BLOCKSCOUT_API = "https://eth.blockscout.com/api/v2"
RPC_URLS = [
    "https://ethereum-rpc.publicnode.com",
    "https://eth.drpc.org",
]
ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")
NUMBER_RE = re.compile(r"#\s*0*(\d{1,4})\b")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def json_dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def csv_write(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def request_json(method: str, url: str, *, headers: dict[str, str] | None = None,
                 params: dict[str, Any] | None = None, json_body: Any = None,
                 timeout: int = 45, attempts: int = 8) -> Any:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            r = requests.request(method, url, headers=headers, params=params, json=json_body, timeout=timeout)
            if r.status_code in (408, 425, 429) or r.status_code >= 500:
                wait = min(30.0, 1.25 * (2 ** attempt))
                print(f"retry {r.status_code} {url} in {wait:.1f}s", flush=True)
                time.sleep(wait)
                continue
            r.raise_for_status()
            if not r.text.strip():
                return {}
            return r.json()
        except Exception as e:
            last = e
            if attempt == attempts - 1:
                break
            wait = min(30.0, 1.25 * (2 ** attempt))
            print(f"retry exception {type(e).__name__} {url} in {wait:.1f}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"request failed after {attempts} attempts: {method} {url}: {last}")


def find_api_key(obj: Any) -> str | None:
    if isinstance(obj, dict):
        for k in ("api_key", "apikey", "key", "token"):
            v = obj.get(k)
            if isinstance(v, str) and len(v) >= 12:
                return v
        for v in obj.values():
            found = find_api_key(v)
            if found:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_api_key(v)
            if found:
                return found
    return None


def get_opensea_key() -> str:
    supplied = os.getenv("OPENSEA_API_KEY", "").strip()
    if supplied:
        return supplied
    payload = request_json("POST", f"{OPEN_SEA_API}/auth/keys")
    key = find_api_key(payload)
    if not key:
        raise RuntimeError(f"OpenSea instant key endpoint returned no recognizable key: {payload}")
    return key


def extract_address(value: Any) -> str | None:
    if isinstance(value, str) and ADDRESS_RE.fullmatch(value):
        return value.lower()
    return None


def recursive_addresses(obj: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(obj, dict):
        for v in obj.values():
            found |= recursive_addresses(v)
    elif isinstance(obj, list):
        for v in obj:
            found |= recursive_addresses(v)
    else:
        a = extract_address(obj)
        if a:
            found.add(a)
    return found


def normalize_contract(v: Any) -> str | None:
    if isinstance(v, str):
        return v.lower()
    if isinstance(v, dict):
        for k in ("address", "contract_address", "contract"):
            a = extract_address(v.get(k))
            if a:
                return a
    return None


def parse_identifier(nft: dict[str, Any]) -> str | None:
    for k in ("identifier", "token_id", "tokenId", "id"):
        v = nft.get(k)
        if isinstance(v, int):
            return str(v)
        if isinstance(v, str) and v.isdigit():
            return str(int(v))
    return None


def parse_canonical_number(name: str | None) -> int | None:
    if not name:
        return None
    m = NUMBER_RE.search(name)
    return int(m.group(1)) if m else None


def fetch_opensea_collection() -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    key = get_opensea_key()
    headers = {"x-api-key": key, "accept": "application/json", "user-agent": "MONTREAL-AI-Becoming-Omega-Snapshot/1.0"}
    raw_pages: list[dict[str, Any]] = []
    nfts: list[dict[str, Any]] = []
    cursor: str | None = None
    seen_cursors: set[str] = set()
    for page in range(1, 50):
        params: dict[str, Any] = {"limit": 200}
        if cursor:
            params["next"] = cursor
        payload = request_json("GET", f"{OPEN_SEA_API}/collection/{COLLECTION_SLUG}/nfts", headers=headers, params=params)
        if not isinstance(payload, dict):
            raise RuntimeError(f"unexpected OpenSea payload type: {type(payload)}")
        raw_pages.append(payload)
        items = payload.get("nfts") or payload.get("items") or []
        if not isinstance(items, list):
            raise RuntimeError(f"unexpected OpenSea nfts field: {type(items)}")
        nfts.extend(x for x in items if isinstance(x, dict))
        cursor_value = payload.get("next") or payload.get("next_cursor")
        cursor = str(cursor_value) if cursor_value else None
        print(f"OpenSea page {page}: {len(items)} items; total {len(nfts)}", flush=True)
        if not cursor:
            break
        if cursor in seen_cursors:
            raise RuntimeError("OpenSea pagination cursor repeated")
        seen_cursors.add(cursor)
    else:
        raise RuntimeError("OpenSea pagination exceeded safety limit")
    return nfts, raw_pages, key


def build_manifest(nfts: list[dict[str, Any]]):
    records: dict[tuple[str, str], dict[str, Any]] = {}
    source_addresses: dict[str, set[str]] = defaultdict(set)
    issues: list[str] = []
    for nft in nfts:
        identifier = parse_identifier(nft)
        contract = normalize_contract(nft.get("contract")) or normalize_contract(nft.get("contract_address"))
        if not identifier:
            issues.append(f"NFT missing identifier: {nft}")
            continue
        if not contract:
            contract = CONTRACT
        if contract != CONTRACT:
            continue
        name = nft.get("name") if isinstance(nft.get("name"), str) else None
        canonical = parse_canonical_number(name)
        token_int = int(identifier)
        token_hex = "0x" + token_int.to_bytes(32, "big").hex()
        encoded_creator = "0x" + token_hex[2:42]
        lower96 = token_int & ((1 << 96) - 1)
        creation_nonce = lower96 >> 40
        encoded_supply = lower96 & ((1 << 40) - 1)
        rec = {
            "canonical_number": canonical,
            "title": name,
            "chain": CHAIN,
            "chain_id": CHAIN_ID,
            "contract": contract,
            "token_standard": (nft.get("token_standard") or "erc1155").lower(),
            "token_id_decimal": identifier,
            "token_id_hex": token_hex,
            "encoded_creator": encoded_creator.lower(),
            "creation_nonce": str(creation_nonce),
            "encoded_supply": str(encoded_supply),
            "opensea_url": nft.get("opensea_url") or f"https://opensea.io/item/ethereum/{contract}/{identifier}",
            "metadata_url": nft.get("metadata_url"),
            "image_url": nft.get("image_url") or nft.get("display_image_url"),
            "collection": nft.get("collection") or COLLECTION_SLUG,
        }
        key = (contract, identifier)
        if key in records and records[key] != rec:
            issues.append(f"duplicate token with conflicting normalized data: {identifier}")
        records[key] = rec
        source_addresses[identifier] |= recursive_addresses(nft)
    manifest = list(records.values())
    manifest.sort(key=lambda r: (r["canonical_number"] is None, r["canonical_number"] or 10**9, int(r["token_id_decimal"])))
    number_counts = Counter(r["canonical_number"] for r in manifest if r["canonical_number"] is not None)
    actual_numbers = {int(n) for n in number_counts}
    audit = {
        "normalization_issues": issues,
        "duplicate_canonical_numbers": sorted(str(n) for n, c in number_counts.items() if c > 1),
        "missing_canonical_numbers": sorted(str(n) for n in set(range(1, EXPECTED_COUNT + 1)) - actual_numbers),
        "out_of_range_canonical_numbers": sorted(str(n) for n in actual_numbers - set(range(1, EXPECTED_COUNT + 1))),
    }
    return manifest, {k: sorted(v) for k, v in source_addresses.items()}, audit


def rpc_call(url: str, method: str, params: list[Any], request_id: int = 1) -> Any:
    payload = request_json("POST", url, json_body={"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
    if not isinstance(payload, dict):
        raise RuntimeError(f"bad JSON-RPC payload from {url}: {payload}")
    if payload.get("error"):
        raise RuntimeError(f"JSON-RPC error from {url}: {payload['error']}")
    return payload.get("result")


def freeze_block() -> dict[str, Any]:
    provider_heads = []
    for url in RPC_URLS:
        block = rpc_call(url, "eth_getBlockByNumber", ["finalized", False])
        if not isinstance(block, dict) or not block.get("number") or not block.get("hash"):
            raise RuntimeError(f"provider does not return finalized block: {url}: {block}")
        provider_heads.append({"rpc_url": url, "number": int(block["number"], 16), "hash": block["hash"].lower(), "timestamp": int(block["timestamp"], 16)})
    selected_number = min(x["number"] for x in provider_heads)
    selected_hex = hex(selected_number)
    selected = []
    for url in RPC_URLS:
        block = rpc_call(url, "eth_getBlockByNumber", [selected_hex, False])
        if not isinstance(block, dict):
            raise RuntimeError(f"provider missing selected block {selected_number}: {url}")
        selected.append({"rpc_url": url, "number": int(block["number"], 16), "hash": block["hash"].lower(), "timestamp": int(block["timestamp"], 16)})
    if len({x["hash"] for x in selected}) != 1 or len({x["timestamp"] for x in selected}) != 1:
        raise RuntimeError(f"RPC providers disagree on selected block: {selected}")
    ts = selected[0]["timestamp"]
    dt_utc = datetime.fromtimestamp(ts, timezone.utc)
    dt_mtl = dt_utc.astimezone(ZoneInfo("America/Montreal"))
    return {
        "chain": CHAIN,
        "chain_id": CHAIN_ID,
        "block_tag_used": "finalized",
        "block_number": selected_number,
        "block_number_hex": selected_hex,
        "block_hash": selected[0]["hash"],
        "block_timestamp_unix": ts,
        "block_timestamp_utc": dt_utc.isoformat().replace("+00:00", "Z"),
        "block_timestamp_montreal": dt_mtl.isoformat(),
        "selection_rule": "Minimum finalized height reported by two independent public Ethereum RPC endpoints, cross-checked by block hash and timestamp.",
        "providers_at_freeze": provider_heads,
        "providers_cross_check": selected,
        "frozen_at_utc": utc_now(),
    }


def blockscout_pages(path: str, max_pages: int = 200):
    url = f"{BLOCKSCOUT_API}{path}"
    params = None
    all_items = []
    errors = []
    seen = set()
    for _ in range(max_pages):
        try:
            payload = request_json("GET", url, params=params, attempts=7)
        except Exception as e:
            errors.append(str(e))
            break
        if isinstance(payload, dict):
            items = payload.get("items") or []
            if isinstance(items, list):
                all_items.extend(items)
            nxt = payload.get("next_page_params")
            if not nxt:
                break
            if not isinstance(nxt, dict):
                errors.append(f"unexpected next_page_params: {nxt}")
                break
            params = {k: v for k, v in nxt.items() if v is not None}
            signature = urlencode(sorted((str(k), str(v)) for k, v in params.items()))
            if signature in seen:
                errors.append("repeated Blockscout pagination cursor")
                break
            seen.add(signature)
        elif isinstance(payload, list):
            all_items.extend(payload)
            break
        else:
            errors.append(f"unexpected Blockscout payload type: {type(payload)}")
            break
    else:
        errors.append("Blockscout pagination exceeded safety limit")
    return all_items, errors


def candidate_worker(rec: dict[str, Any], seed: list[str]) -> dict[str, Any]:
    token_id = rec["token_id_decimal"]
    base = f"/tokens/{CONTRACT}/instances/{token_id}"
    holders, holder_errors = blockscout_pages(base + "/holders", max_pages=20)
    transfers, transfer_errors = blockscout_pages(base + "/transfers", max_pages=200)
    addresses = {CREATOR}
    addresses.update(a.lower() for a in seed if ADDRESS_RE.fullmatch(a))
    addresses |= recursive_addresses(holders)
    addresses |= recursive_addresses(transfers)
    addresses.discard(CONTRACT)
    addresses.discard("0x0000000000000000000000000000000000000000")
    return {
        "token_id_decimal": token_id,
        "candidate_addresses": sorted(addresses),
        "holder_item_count": len(holders),
        "transfer_item_count": len(transfers),
        "errors": holder_errors + transfer_errors,
    }


def gather_candidates(manifest, source_addresses):
    candidates = {}
    diagnostics = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(candidate_worker, rec, source_addresses.get(rec["token_id_decimal"], [])): rec for rec in manifest}
        completed = 0
        for fut in as_completed(futures):
            rec = futures[fut]
            result = fut.result()
            candidates[rec["token_id_decimal"]] = result["candidate_addresses"]
            diagnostics.append(result)
            completed += 1
            if completed % 25 == 0 or completed == len(manifest):
                print(f"Blockscout candidate discovery: {completed}/{len(manifest)}", flush=True)
    diagnostics.sort(key=lambda x: int(x["token_id_decimal"]))
    return candidates, diagnostics


def balance_call_data(owner: str, token_id: str) -> str:
    return "0x00fdd58e" + owner[2:].lower().rjust(64, "0") + int(token_id).to_bytes(32, "big").hex()


def rpc_batch(url: str, calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    last = None
    for attempt in range(8):
        try:
            r = requests.post(url, json=calls, timeout=90)
            if r.status_code in (408, 425, 429) or r.status_code >= 500:
                time.sleep(min(30.0, 1.2 * (2 ** attempt)))
                continue
            r.raise_for_status()
            payload = r.json()
            if not isinstance(payload, list):
                raise RuntimeError(f"batch response is not a list: {payload}")
            return payload
        except Exception as e:
            last = e
            if attempt == 7:
                break
            time.sleep(min(30.0, 1.2 * (2 ** attempt)))
    raise RuntimeError(f"RPC batch failed: {url}: {last}")


def query_balances(candidates, block):
    tasks = [(token_id, address) for token_id, addresses in candidates.items() for address in addresses]
    print(f"Historical balance checks to run: {len(tasks)}", flush=True)
    responses_by_key = {}
    errors = []
    next_id = 1
    chunk_size = 100
    for start in range(0, len(tasks), chunk_size):
        chunk = tasks[start:start + chunk_size]
        request_rows = []
        id_to_key = {}
        for token_id, owner in chunk:
            rid = next_id
            next_id += 1
            id_to_key[rid] = (token_id, owner)
            request_rows.append({"jsonrpc": "2.0", "id": rid, "method": "eth_call", "params": [{"to": CONTRACT, "data": balance_call_data(owner, token_id)}, block["block_number_hex"]]})
        try:
            response_rows = rpc_batch(RPC_URLS[0], request_rows)
        except Exception as batch_error:
            response_rows = []
            for req in request_rows:
                try:
                    result = rpc_call(RPC_URLS[0], req["method"], req["params"], req["id"])
                    response_rows.append({"jsonrpc": "2.0", "id": req["id"], "result": result})
                except Exception as e:
                    response_rows.append({"jsonrpc": "2.0", "id": req["id"], "error": str(e)})
            errors.append({"scope": "batch", "start": start, "error": str(batch_error)})
        for row in response_rows:
            rid = row.get("id")
            key = id_to_key.get(rid)
            if not key:
                continue
            if row.get("error"):
                errors.append({"token_id_decimal": key[0], "owner": key[1], "error": row["error"]})
                continue
            result = row.get("result")
            try:
                value = int(result, 16) if isinstance(result, str) else int(result)
            except Exception:
                errors.append({"token_id_decimal": key[0], "owner": key[1], "error": f"invalid result {result}"})
                continue
            responses_by_key[key] = value
        if (start // chunk_size + 1) % 10 == 0 or start + chunk_size >= len(tasks):
            print(f"Historical balances: {min(start + chunk_size, len(tasks))}/{len(tasks)}", flush=True)
    holdings = []
    for (token_id, owner), balance in sorted(responses_by_key.items(), key=lambda kv: (int(kv[0][0]), kv[0][1])):
        if balance > 0:
            holdings.append({"chain_id": CHAIN_ID, "block_number": block["block_number"], "block_hash": block["block_hash"], "contract": CONTRACT, "token_id_decimal": token_id, "owner": owner, "balance": str(balance)})
    return holdings, errors


def manifest_root(manifest) -> str:
    canonical = "\n".join(f"{r['canonical_number']}|{r['contract']}|{r['token_id_decimal']}|{r['encoded_supply']}" for r in manifest) + "\n"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    print(f"Snapshot started at {started_at}", flush=True)
    block = freeze_block()
    print(f"Frozen finalized block {block['block_number']} {block['block_hash']} at {block['block_timestamp_utc']}", flush=True)
    json_dump(OUTPUT / "snapshot_block.json", block)
    nfts, raw_pages, _key = fetch_opensea_collection()
    json_dump(OUTPUT / "raw_opensea_collection_pages.json", raw_pages)
    manifest, source_addresses, manifest_audit = build_manifest(nfts)
    for i, rec in enumerate(manifest, start=1):
        rec["manifest_index"] = i
    json_dump(OUTPUT / "genesis_manifest_v1.json", {"schema": "montrealai.becoming.genesis-manifest.v1", "collection_slug": COLLECTION_SLUG, "chain_id": CHAIN_ID, "contract": CONTRACT, "creator": CREATOR, "expected_count": EXPECTED_COUNT, "actual_count": len(manifest), "manifest_sha256_canonical_rows": manifest_root(manifest), "generated_at_utc": utc_now(), "items": manifest})
    manifest_fields = ["manifest_index", "canonical_number", "title", "chain", "chain_id", "contract", "token_standard", "token_id_decimal", "token_id_hex", "encoded_creator", "creation_nonce", "encoded_supply", "opensea_url", "metadata_url", "image_url", "collection"]
    csv_write(OUTPUT / "genesis_manifest_v1.csv", manifest_fields, manifest)
    json_dump(OUTPUT / "manifest_normalization_audit.json", manifest_audit)
    fatal_manifest = []
    if len(manifest) != EXPECTED_COUNT:
        fatal_manifest.append(f"manifest count {len(manifest)} != {EXPECTED_COUNT}")
    if manifest_audit["duplicate_canonical_numbers"]:
        fatal_manifest.append(f"duplicate canonical numbers: {manifest_audit['duplicate_canonical_numbers']}")
    if manifest_audit["missing_canonical_numbers"]:
        fatal_manifest.append(f"missing canonical numbers: {manifest_audit['missing_canonical_numbers']}")
    if manifest_audit["out_of_range_canonical_numbers"]:
        fatal_manifest.append(f"out-of-range canonical numbers: {manifest_audit['out_of_range_canonical_numbers']}")
    wrong_creator = [r["canonical_number"] for r in manifest if r["encoded_creator"] != CREATOR]
    if wrong_creator:
        fatal_manifest.append(f"token IDs with unexpected encoded creator: {wrong_creator}")
    if fatal_manifest:
        raise RuntimeError("; ".join(fatal_manifest))
    print("Manifest audit passed: 556 unique canonical IDs", flush=True)
    candidates, candidate_diagnostics = gather_candidates(manifest, source_addresses)
    json_dump(OUTPUT / "candidate_discovery_diagnostics.json", candidate_diagnostics)
    holdings, balance_errors = query_balances(candidates, block)
    by_token = defaultdict(list)
    for h in holdings:
        by_token[h["token_id_decimal"]].append(h)
    canonical_by_token = {r["token_id_decimal"]: r for r in manifest}
    for h in holdings:
        rec = canonical_by_token[h["token_id_decimal"]]
        h["canonical_number"] = rec["canonical_number"]
        h["title"] = rec["title"]
        h["encoded_supply"] = rec["encoded_supply"]
    holdings.sort(key=lambda h: (h["canonical_number"], h["owner"]))
    token_audit_rows = []
    unresolved = []
    supply_mismatches = []
    for rec in manifest:
        token_id = rec["token_id_decimal"]
        holder_rows = by_token.get(token_id, [])
        total = sum(int(x["balance"]) for x in holder_rows)
        expected = int(rec["encoded_supply"])
        status = "ok" if total == expected else "supply_mismatch"
        if not holder_rows:
            unresolved.append(rec["canonical_number"])
            status = "unresolved"
        if total != expected:
            supply_mismatches.append({"canonical_number": rec["canonical_number"], "token_id_decimal": token_id, "expected_supply": expected, "accounted_balance": total})
        token_audit_rows.append({"canonical_number": rec["canonical_number"], "token_id_decimal": token_id, "expected_supply": str(expected), "holder_row_count": len(holder_rows), "accounted_balance": str(total), "candidate_count": len(candidates.get(token_id, [])), "status": status})
    holding_fields = ["chain_id", "block_number", "block_hash", "contract", "canonical_number", "title", "token_id_decimal", "owner", "balance", "encoded_supply"]
    csv_write(OUTPUT / "snapshot_token_holdings.csv", holding_fields, holdings)
    json_dump(OUTPUT / "snapshot_token_holdings.json", {"schema": "montrealai.becoming.snapshot-token-holdings.v1", "snapshot_block": block, "rows": holdings})
    wallet_totals = {}
    for h in holdings:
        w = wallet_totals.setdefault(h["owner"], {"wallet": h["owner"], "distinct_genesis_tokens": 0, "total_genesis_units": 0, "canonical_numbers": []})
        w["distinct_genesis_tokens"] += 1
        w["total_genesis_units"] += int(h["balance"])
        w["canonical_numbers"].append(h["canonical_number"])
    wallet_rows = []
    for w in wallet_totals.values():
        nums = sorted(w.pop("canonical_numbers"))
        w["canonical_numbers"] = ",".join(str(n) for n in nums)
        w["category"] = "creator" if w["wallet"] == CREATOR else "holder"
        wallet_rows.append(w)
    wallet_rows.sort(key=lambda w: (-w["total_genesis_units"], w["wallet"]))
    wallet_fields = ["wallet", "distinct_genesis_tokens", "total_genesis_units", "category", "canonical_numbers"]
    csv_write(OUTPUT / "snapshot_wallet_summary.csv", wallet_fields, wallet_rows)
    json_dump(OUTPUT / "snapshot_wallet_summary.json", {"schema": "montrealai.becoming.snapshot-wallet-summary.v1", "snapshot_block": block, "wallets": wallet_rows})
    csv_write(OUTPUT / "snapshot_token_audit.csv", ["canonical_number", "token_id_decimal", "expected_supply", "holder_row_count", "accounted_balance", "candidate_count", "status"], token_audit_rows)
    api_errors = [d for d in candidate_diagnostics if d["errors"]]
    audit = {
        "schema": "montrealai.becoming.snapshot-audit.v1",
        "started_at_utc": started_at,
        "completed_at_utc": utc_now(),
        "snapshot_block": block,
        "manifest": {"expected_items": EXPECTED_COUNT, "actual_items": len(manifest), "unique_token_ids": len({r['token_id_decimal'] for r in manifest}), "canonical_numbers_complete": not manifest_audit["missing_canonical_numbers"] and not manifest_audit["duplicate_canonical_numbers"], "canonical_rows_sha256": manifest_root(manifest)},
        "ownership": {"holding_rows": len(holdings), "unique_wallets": len(wallet_rows), "total_accounted_units": sum(int(h["balance"]) for h in holdings), "creator_held_tokens": sum(1 for h in holdings if h["owner"] == CREATOR), "unresolved_canonical_numbers": unresolved, "supply_mismatches": supply_mismatches, "historical_balance_call_errors": balance_errors, "blockscout_token_diagnostics_with_errors": api_errors},
        "status": "PASS" if not unresolved and not supply_mismatches and not balance_errors else "FAIL",
    }
    json_dump(OUTPUT / "snapshot_audit_report.json", audit)
    readme = f"""# MONTREAL.AI — BECOMING Ω: THE FINAL 444\n\n## Genesis 556 ownership snapshot\n\nThis package contains the exact 556 token IDs in the legacy MONTREAL.AI OpenSea collection and their ERC-1155 balances at one finalized Ethereum block.\n\n- Contract: `{CONTRACT}`\n- Collection slug: `{COLLECTION_SLUG}`\n- Finalized block: `{block['block_number']}`\n- Block hash: `{block['block_hash']}`\n- Block time (UTC): `{block['block_timestamp_utc']}`\n- Block time (Montréal): `{block['block_timestamp_montreal']}`\n- Manifest items: `{len(manifest)}`\n- Positive token-holder rows: `{len(holdings)}`\n- Unique holder wallets: `{len(wallet_rows)}`\n- Accounted ERC-1155 units: `{sum(int(h['balance']) for h in holdings)}`\n- Audit result: `{audit['status']}`\n\n## Authority and method\n\nOpenSea's collection API was used only to enumerate the collection's exact token IDs and metadata. Ownership was computed by calling the legacy ERC-1155 contract's `balanceOf(address,uint256)` at the frozen block. Candidate addresses came from the creator encoded in the IDs, OpenSea records, and Blockscout holder/transfer indexes. The contract call at the selected block is the ownership authority.\n\n## Principal files\n\n- `genesis_manifest_v1.json` / `.csv`: exact canonical 556-token manifest.\n- `snapshot_block.json`: finalized block selection and two-provider cross-check.\n- `snapshot_token_holdings.json` / `.csv`: token-level balances at that block.\n- `snapshot_wallet_summary.json` / `.csv`: wallet-level aggregation.\n- `snapshot_token_audit.csv`: one-row-per-token supply reconciliation.\n- `snapshot_audit_report.json`: completeness and integrity checks.\n- `SHA256SUMS`: package file hashes.\n\n## Verification\n\nFor any row, call `balanceOf(owner, tokenId)` on `{CONTRACT}` at block `{block['block_number']}`. No private key, signature, transaction, gas, OpenSea account, or paid API key is required to verify ownership.\n"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")
    (OUTPUT / "snapshot.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")
    hash_targets = sorted(p for p in OUTPUT.iterdir() if p.is_file() and p.name not in {"SHA256SUMS", "montrealai-becoming-omega-genesis-556-snapshot.zip"})
    (OUTPUT / "SHA256SUMS").write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in hash_targets), encoding="utf-8")
    zip_path = OUTPUT / "montrealai-becoming-omega-genesis-556-snapshot.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(OUTPUT.iterdir()):
            if p.is_file() and p != zip_path:
                z.write(p, arcname=p.name)
    print(json.dumps({"status": audit["status"], "block_number": block["block_number"], "block_hash": block["block_hash"], "block_timestamp_utc": block["block_timestamp_utc"], "manifest_items": len(manifest), "holding_rows": len(holdings), "unique_wallets": len(wallet_rows), "total_units": sum(int(h["balance"]) for h in holdings), "creator_held_tokens": audit["ownership"]["creator_held_tokens"], "unresolved": unresolved, "supply_mismatches": supply_mismatches, "zip_sha256": sha256_file(zip_path)}, indent=2), flush=True)
    if audit["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
