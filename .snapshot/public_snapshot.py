#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import re
import time
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


def fetch_html(url: str, attempts: int = 8) -> requests.Response:
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
    }
    last = None
    for attempt in range(attempts):
        try:
            r = requests.get(url, headers=headers, timeout=60)
            if r.status_code in (408, 425, 429) or r.status_code >= 500:
                wait = min(30.0, 1.5 * (2 ** attempt))
                print(f"OpenSea public page retry {r.status_code} {url} in {wait:.1f}s", flush=True)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r
        except Exception as e:
            last = e
            if attempt == attempts - 1:
                break
            wait = min(30.0, 1.5 * (2 ** attempt))
            print(f"OpenSea public page exception {type(e).__name__} {url} in {wait:.1f}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"failed to fetch public OpenSea page {url}: {last}")


def parse_page(html: str, page_url: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    found: dict[str, dict[str, Any]] = {}
    for a in soup.find_all("a", href=True):
        href = str(a.get("href"))
        m = ITEM_RE.search(href)
        if not m or m.group(1).lower() != core.CONTRACT:
            continue
        token_id = str(int(m.group(2)))
        text_candidates = [
            " ".join(a.stripped_strings),
            str(a.get("aria-label") or ""),
            str(a.get("title") or ""),
            str(a.get("data-testid") or ""),
        ]
        combined = " ".join(x for x in text_candidates if x).strip()
        title_match = TITLE_RE.search(combined)
        name = f"Crypto AI Art #{int(title_match.group(1)):03d}" if title_match else None
        found[token_id] = {
            "identifier": token_id,
            "contract": core.CONTRACT,
            "token_standard": "erc1155",
            "name": name,
            "collection": core.COLLECTION_SLUG,
            "opensea_url": urljoin(page_url, href.split("?")[0]),
            "public_anchor_text": combined[:500],
        }
    if found:
        return list(found.values())
    for m in ITEM_RE.finditer(html.replace("\\/", "/")):
        if m.group(1).lower() != core.CONTRACT:
            continue
        token_id = str(int(m.group(2)))
        left = max(0, m.start() - 1000)
        right = min(len(html), m.end() + 1000)
        nearby = html[left:right].replace("\\u0023", "#").replace("\\/", "/")
        title_matches = list(TITLE_RE.finditer(nearby))
        name = None
        if title_matches:
            closest = min(title_matches, key=lambda x: abs((left + x.start()) - m.start()))
            name = f"Crypto AI Art #{int(closest.group(1)):03d}"
        found[token_id] = {
            "identifier": token_id,
            "contract": core.CONTRACT,
            "token_standard": "erc1155",
            "name": name,
            "collection": core.COLLECTION_SLUG,
            "opensea_url": f"https://opensea.io/item/ethereum/{core.CONTRACT}/{token_id}",
            "public_anchor_text": "",
        }
    return list(found.values())


def fetch_public_collection():
    records: dict[str, dict[str, Any]] = {}
    raw_pages: list[dict[str, Any]] = []
    page_without_links = 0
    for sweep in range(1, 4):
        sweep_new = 0
        for page in range(1, 26):
            url = BASE if page == 1 else f"{BASE}?page={page}"
            response = fetch_html(url)
            items = parse_page(response.text, response.url)
            before = len(records)
            for item in items:
                existing = records.get(item["identifier"])
                if existing and not existing.get("name") and item.get("name"):
                    records[item["identifier"]] = item
                elif not existing:
                    records[item["identifier"]] = item
            added = len(records) - before
            sweep_new += added
            raw_pages.append({
                "sweep": sweep,
                "page": page,
                "url": response.url,
                "status": response.status_code,
                "html_bytes": len(response.content),
                "html_sha256": hashlib.sha256(response.content).hexdigest(),
                "unique_items_on_page": len(items),
                "new_items_added": added,
                "total_unique_items": len(records),
                "items": items,
            })
            print(f"OpenSea public sweep {sweep} page {page}: {len(items)} links, +{added}, total {len(records)}", flush=True)
            if len(items) == 0:
                page_without_links += 1
            else:
                page_without_links = 0
            if page >= 18 and page_without_links >= 2:
                break
            if len(records) == core.EXPECTED_COUNT and page >= 18:
                break
            time.sleep(0.15)
        missing_names = sum(1 for x in records.values() if not x.get("name"))
        print(f"OpenSea public sweep {sweep} complete: {len(records)} IDs, {missing_names} missing names, {sweep_new} new", flush=True)
        if len(records) == core.EXPECTED_COUNT and missing_names == 0:
            break
        time.sleep(1.0)
    missing = [x for x in records.values() if not x.get("name")]
    for index, item in enumerate(missing, start=1):
        r = fetch_html(item["opensea_url"])
        soup = BeautifulSoup(r.text, "html.parser")
        candidates = []
        if soup.title and soup.title.string:
            candidates.append(soup.title.string)
        for key, value in (("property", "og:title"), ("name", "twitter:title")):
            tag = soup.find("meta", attrs={key: value})
            if tag and tag.get("content"):
                candidates.append(str(tag.get("content")))
        m = TITLE_RE.search(" ".join(candidates))
        if m:
            item["name"] = f"Crypto AI Art #{int(m.group(1)):03d}"
        print(f"OpenSea item-title recovery {index}/{len(missing)}: {item['identifier']} -> {item.get('name')}", flush=True)
        time.sleep(0.1)
    return list(records.values()), raw_pages, "public-web-no-api-key"


core.fetch_opensea_collection = fetch_public_collection
core.main()
