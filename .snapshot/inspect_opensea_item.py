#!/usr/bin/env python3
import json
import re
from pathlib import Path

import requests

URL = "https://opensea.io/item/ethereum/0x495f947276749ce646f68ac8c248420045cb7b5e/2392630434290240917728431095880785304289144848761899072947382792323770351617"
OUT = Path("diag-output")
OUT.mkdir(exist_ok=True)
r = requests.get(URL, headers={"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36","accept":"text/html,application/xhtml+xml"}, timeout=60)
r.raise_for_status()
html = r.text
(OUT / "item-319.html").write_text(html, encoding="utf-8")
addresses = sorted(set(a.lower() for a in re.findall(r"0x[a-fA-F0-9]{40}", html)))
contexts = {}
for address in addresses:
    positions = [m.start() for m in re.finditer(re.escape(address), html, flags=re.I)]
    contexts[address] = [html[max(0,p-300):min(len(html),p+500)] for p in positions[:10]]
result = {"url":r.url,"status":r.status_code,"html_bytes":len(r.content),"addresses":addresses,"contexts":contexts}
(OUT / "addresses.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps({"status":r.status_code,"html_bytes":len(r.content),"address_count":len(addresses),"addresses":addresses}, indent=2))
