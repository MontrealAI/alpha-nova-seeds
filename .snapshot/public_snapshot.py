#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import re
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("snapshot_core", HERE / "snapshot.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load snapshot.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

ITEM_RE = re.compile(r"/item/ethereum/(0x[0-9a-fA-F]{40})/(\d+)")
TITLE_RE = re.compile(r"Crypto\s+AI\s+Art\s*#\s*0*(\d{1,3})\b", re.I)
BASE = "https://opensea.io/collection/montrealai"
METADATA_BASE = f"https://api.opensea.io/api/v1/metadata/{core.CONTRACT}"
CREATOR_INT = int(core.CREATOR, 16)
_thread_local = threading.local()


def session() -> requests.Session:
    if not hasattr(_thread_local, "session"):
        s = requests.Session()
        s.headers.update({
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
        })
        _thread_local.session = s
    return _thread_local.session


def get_response(url: str, *, accept: str, attempts: int = 8, missing_ok: bool = False) -> requests.Response | None:
    last = None
    for attempt in range(attempts):
        try:
            r = session().get(url, headers={"accept": accept}, timeout=60)
            if missing_ok and r.status_code in (400, 404, 410, 422):
                return None
            if r.status_code in (408, 425, 429) or r.status_code >= 500:
                wait = min(30.0, 0.8 * (2 ** attempt))
                print(f"retry {r.status_code} {url} in {wait:.1f}s", flush=True)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r
        except Exception as e:
            last = e
            if attempt == attempts - 1:
                break
            wait = min(30.0, 0.8 * (2 ** attempt))
            print(f"retry {type(e).__name__} {url} in {wait:.1f}s", flush=True)
            time.sleep(wait)
    if missing_ok:
        return None
    raise RuntimeError(f"failed to fetch {url}: {last}")


def parse_public_page(html: str, page_url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    found: dict[str, dict[str, Any]] = {}
    for a in soup.find_all("a", href=True):
        href = str(a.get("href"))
        m = ITEM_RE.search(href)
        if not m or m.group(1).lower() != core.CONTRACT:
            continue
        token_id = str(int(m.group(2)))
        combined = " ".join([
            " ".join(a.stripped_strings),
            str(a.get("aria-label") or ""),
            str(a.get("title") or ""),
        ]).strip()
        tm = TITLE_RE.search(combined)
        name = f"Crypto AI Art #{int(tm.group(1)):03d}" if tm else None
        found[token_id] = {
            "identifier": token_id,
            "contract": core.CONTRACT,
            "token_standard": "erc1155",
            "name": name,
            "collection": core.COLLECTION_SLUG,
            "opensea_url": urljoin(page_url, href.split("?")[0]),
            "public_anchor_text": combined[:500],
        }
    return list(found.values())


def token_for_nonce(nonce: int, supply: int = 1) -> tuple[str, str]:
    token_int = (CREATOR_INT << 96) | (nonce << 40) | supply
    return str(token_int), "0x" + token_int.to_bytes(32, "big").hex()


def fetch_metadata_candidate(nonce: int):
    token_id, token_hex = token_for_nonce(nonce)
    url = f"{METADATA_BASE}/{token_hex}"
    response = get_response(url, accept="application/json", missing_ok=True)
    diag: dict[str, Any] = {"nonce": nonce, "token_id_decimal": token_id, "token_id_hex": token_hex, "metadata_url": url}
    if response is None:
        diag["status"] = "not_found_or_failed"
        return nonce, None, diag
    diag["http_status"] = response.status_code
    diag["content_type"] = response.headers.get("content-type")
    diag["body_sha256"] = hashlib.sha256(response.content).hexdigest()
    try:
        payload = response.json()
    except Exception:
        diag["status"] = "non_json"
        diag["body_preview"] = response.text[:300]
        return nonce, None, diag
    diag["payload"] = payload
    if not isinstance(payload, dict):
        diag["status"] = "unexpected_payload"
        return nonce, None, diag
    name = payload.get("name")
    tm = TITLE_RE.search(name) if isinstance(name, str) else None
    if not tm:
        diag["status"] = "not_collection_item"
        return nonce, None, diag
    canonical = int(tm.group(1))
    item = {
        "identifier": token_id,
        "contract": core.CONTRACT,
        "token_standard": "erc1155",
        "name": f"Crypto AI Art #{canonical:03d}",
        "collection": core.COLLECTION_SLUG,
        "opensea_url": f"https://opensea.io/item/ethereum/{core.CONTRACT}/{token_id}",
        "metadata_url": url,
        "image_url": payload.get("image") or payload.get("image_url"),
        "description": payload.get("description"),
        "animation_url": payload.get("animation_url"),
        "external_link": payload.get("external_link"),
    }
    diag["status"] = "collection_item"
    diag["canonical_number"] = canonical
    return nonce, item, diag


def fetch_collection_no_key():
    records: dict[str, dict[str, Any]] = {}
    diagnostics: list[dict[str, Any]] = []
    for page in range(1, 26):
        url = BASE if page == 1 else f"{BASE}?page={page}"
        r = get_response(url, accept="text/html,application/xhtml+xml")
        if r is None:
            break
        items = parse_public_page(r.text, r.url)
        before = len(records)
        for item in items:
            records[item["identifier"]] = item
        diagnostics.append({
            "source": "public_collection_page",
            "page": page,
            "url": r.url,
            "http_status": r.status_code,
            "html_bytes": len(r.content),
            "html_sha256": hashlib.sha256(r.content).hexdigest(),
            "items_found": len(items),
            "new_items": len(records) - before,
            "total_items": len(records),
        })
        print(f"OpenSea public page {page}: {len(items)} links, total {len(records)}", flush=True)
        if page >= 12 and not items:
            break
        time.sleep(0.12)

    existing_nonces = set()
    for token_id in records:
        token_int = int(token_id)
        existing_nonces.add((token_int & ((1 << 96) - 1)) >> 40)

    scan_nonces = [n for n in range(0, 1001) if n not in existing_nonces]
    print(f"Metadata scan: {len(scan_nonces)} candidate nonces; {len(existing_nonces)} already known", flush=True)
    metadata_diagnostics: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_metadata_candidate, nonce): nonce for nonce in scan_nonces}
        completed = 0
        for fut in as_completed(futures):
            nonce, item, diag = fut.result()
            metadata_diagnostics.append(diag)
            if item:
                existing = records.get(item["identifier"])
                if not existing:
                    records[item["identifier"]] = item
                elif not existing.get("name"):
                    records[item["identifier"]] = {**existing, **item}
            completed += 1
            if completed % 50 == 0 or completed == len(scan_nonces):
                found_count = sum(1 for d in metadata_diagnostics if d.get("status") == "collection_item")
                print(f"Metadata scan {completed}/{len(scan_nonces)}; recovered {found_count}; total {len(records)}", flush=True)

    metadata_diagnostics.sort(key=lambda d: d["nonce"])
    diagnostics.append({
        "source": "legacy_metadata_nonce_scan",
        "range": [0, 1000],
        "known_nonces_skipped": len(existing_nonces),
        "candidates_queried": len(scan_nonces),
        "collection_items_recovered": sum(1 for d in metadata_diagnostics if d.get("status") == "collection_item"),
        "diagnostics": metadata_diagnostics,
    })
    print(f"No-key enumeration complete: {len(records)} unique token IDs", flush=True)
    return list(records.values()), diagnostics, "public-pages-plus-legacy-metadata-no-api-key"


_original_build_manifest = core.build_manifest
MISTITLED_TOKEN_ID = token_for_nonce(322)[0]


def build_manifest_reconciled(nfts):
    manifest, source_addresses, audit = _original_build_manifest(nfts)
    anomalies = []
    for rec in manifest:
        rec["canonical_number_raw"] = rec["canonical_number"]
        rec["title_raw"] = rec["title"]
        if rec["token_id_decimal"] == MISTITLED_TOKEN_ID:
            anomalies.append({
                "token_id_decimal": rec["token_id_decimal"],
                "token_id_hex": rec["token_id_hex"],
                "creation_nonce": rec["creation_nonce"],
                "raw_title": rec["title"],
                "raw_canonical_number": rec["canonical_number"],
                "reconciled_title": "Crypto AI Art #317",
                "reconciled_canonical_number": 317,
                "reason": "The canonical collection sequence is #000 through #555. Creation nonce 321 is #316 and nonce 323 is #318; therefore nonce 322 is the sole historical metadata typo and deterministically reconciles to #317.",
            })
            rec["canonical_number"] = 317
            rec["title"] = "Crypto AI Art #317"
            rec["canonical_reconciliation"] = anomalies[-1]["reason"]
    manifest.sort(key=lambda r: (r["canonical_number"] is None, r["canonical_number"] if r["canonical_number"] is not None else 10**9, int(r["token_id_decimal"])))
    counts = Counter(r["canonical_number"] for r in manifest if r["canonical_number"] is not None)
    expected = set(range(0, core.EXPECTED_COUNT))
    actual = set(int(n) for n in counts)
    audit = {
        **audit,
        "canonical_numbering": "Crypto AI Art #000 through #555",
        "canonical_number_min": 0,
        "canonical_number_max": 555,
        "metadata_anomalies_reconciled": anomalies,
        "duplicate_canonical_numbers": sorted(str(n) for n, c in counts.items() if c > 1),
        "missing_canonical_numbers": sorted(str(n) for n in expected - actual),
        "out_of_range_canonical_numbers": sorted(str(n) for n in actual - expected),
    }
    return manifest, source_addresses, audit


core.fetch_opensea_collection = fetch_collection_no_key
core.build_manifest = build_manifest_reconciled
core.main()
