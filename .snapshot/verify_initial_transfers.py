#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests

CONTRACT = '0x495f947276749ce646f68ac8c248420045cb7b5e'
SNAPSHOT_BLOCK = 25764033
RPC = 'https://ethereum-rpc.publicnode.com'
OUT = Path('diag-output')
OUT.mkdir(exist_ok=True)
TOKENS = [
('064','2392630434290240917728431095880785304289144848761899072947382510848793640961'),
('146','2392630434290240917728431095880785304289144848761899072947382601008747118593'),
('190','2392630434290240917728431095880785304289144848761899072947382650486770368513'),
('194','2392630434290240917728431095880785304289144848761899072947382654884816879617'),
('201','2392630434290240917728431095880785304289144848761899072947382662581398274049'),
('221','2392630434290240917728431095880785304289144848761899072947382684571630829569'),
('279','2392630434290240917728431095880785304289144848761899072947382748343305240577'),
('351','2392630434290240917728431095880785304289144848761899072947382827508142440449'),
('404','2392630434290240917728431095880785304289144848761899072947382885782258712577'),
('416','2392630434290240917728431095880785304289144848761899072947382898976398245889'),
('423','2392630434290240917728431095880785304289144848761899072947382906672979640321'),
('445','2392630434290240917728431095880785304289144848761899072947382930862235451393'),
('450','2392630434290240917728431095880785304289144848761899072947382936359793590273'),
('467','2392630434290240917728431095880785304289144848761899072947382955051491262465'),
('486','2392630434290240917728431095880785304289144848761899072947382975942212190209'),
('495','2392630434290240917728431095880785304289144848761899072947382986937328467969'),
('496','2392630434290240917728431095880785304289144848761899072947382988036840095745'),
('497','2392630434290240917728431095880785304289144848761899072947382989136351723521'),
('499','2392630434290240917728431095880785304289144848761899072947382991335374979073'),
('501','2392630434290240917728431095880785304289144848761899072947382993534398234625'),
('517','2392630434290240917728431095880785304289144848761899072947383012226095906817'),
('520','2392630434290240917728431095880785304289144848761899072947383015524630790145'),
('531','2392630434290240917728431095880785304289144848761899072947383027619258695681'),
('532','2392630434290240917728431095880785304289144848761899072947383028718770323457'),
]
ADDRESS_RE = re.compile(r'0x[a-fA-F0-9]{40}')
OWNER_JSON_RE = re.compile(r'"owner":\{"address":"(0x[a-fA-F0-9]{40})"')
SELLER_RE = re.compile(r'"seller":\{"@type":"Person","name":"(0x[a-fA-F0-9]{40})"')
OWNED_BY_RE = re.compile(r'Owned by(?:<!-- -->)?\s*</span><a[^>]{0,1500}href="([^"]+)"', re.S)
WALLET_CONTEXT_RE = re.compile(r'(?i)(?:wallet|address)[^\n]{0,300}?(0x[a-fA-F0-9]{40})')

session = requests.Session()
session.headers.update({
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
})


def fetch(url: str):
    last = None
    for attempt in range(6):
        try:
            r = session.get(url, timeout=60, allow_redirects=True)
            if r.status_code in (408,425,429) or r.status_code >= 500:
                time.sleep(min(20, 1.5 * 2**attempt)); continue
            r.raise_for_status()
            return r
        except Exception as exc:
            last = exc
            time.sleep(min(20, 1.5 * 2**attempt))
    raise RuntimeError(f'{url}: {last}')


def rpc(method, params, rid=1):
    r = requests.post(RPC, json={'jsonrpc':'2.0','id':rid,'method':method,'params':params}, timeout=60)
    r.raise_for_status(); p=r.json()
    if p.get('error'): raise RuntimeError(p['error'])
    return p['result']


def balance(owner: str, token: str) -> int:
    data='0x00fdd58e'+owner[2:].lower().rjust(64,'0')+int(token).to_bytes(32,'big').hex()
    return int(rpc('eth_call',[{'to':CONTRACT,'data':data},hex(SNAPSHOT_BLOCK)]),16)


def profile_candidates(href: str):
    if re.fullmatch(r'/0x[a-fA-F0-9]{40}', href):
        return {href[1:].lower()}, None
    url=urljoin('https://opensea.io',href)
    r=fetch(url)
    text=r.text
    candidates={a.lower() for a in ADDRESS_RE.findall(text)}
    candidates |= {a.lower() for a in WALLET_CONTEXT_RE.findall(text)}
    return candidates, {'url':r.url,'status':r.status_code,'bytes':len(r.content),'addresses':sorted(candidates)}


def resolve_one(number: str, token: str):
    base=f'https://opensea.io/item/ethereum/{CONTRACT}/{token}'
    attempts=[base, base+'?locale=en', base+f'?snapshot={SNAPSHOT_BLOCK}']
    captures=[]
    candidates=set()
    profile=None
    owner_field=None
    owner_href=None
    for url in attempts:
        r=fetch(url); text=r.text
        matches=[]
        for pattern,label in ((OWNER_JSON_RE,'owner_json'),(SELLER_RE,'schema_seller')):
            m=pattern.search(text)
            if m:
                addr=m.group(1).lower(); candidates.add(addr); matches.append({'source':label,'address':addr})
                if owner_field is None: owner_field=addr
        m=OWNED_BY_RE.search(text)
        if m:
            owner_href=m.group(1); matches.append({'source':'owned_by_href','href':owner_href})
        captures.append({'url':r.url,'status':r.status_code,'bytes':len(r.content),'owner_matches':matches,'has_owned_by':'Owned by' in text,'all_address_count':len(set(ADDRESS_RE.findall(text)))})
        if owner_field or owner_href:
            break
        time.sleep(1.25)
    if owner_href:
        pc,profile=profile_candidates(owner_href); candidates |= pc
    positives=[]
    for addr in sorted(candidates):
        try:
            b=balance(addr,token)
            if b: positives.append({'address':addr,'balance':b})
        except Exception as exc:
            positives.append({'address':addr,'balance_error':str(exc)})
    result={'canonical_number':int(number),'token_id_decimal':token,'captures':captures,'owner_field':owner_field,'owner_href':owner_href,'profile':profile,'candidate_count':len(candidates),'positive_balances_at_snapshot':positives}
    print(json.dumps({'number':number,'owner':owner_field,'href':owner_href,'candidates':len(candidates),'positive':positives},sort_keys=True),flush=True)
    return result


def main():
    try: fetch('https://opensea.io/collection/montrealai')
    except Exception: pass
    rows=[]
    for i,(number,token) in enumerate(TOKENS,1):
        rows.append(resolve_one(number,token))
        time.sleep(1.5)
        print(f'completed {i}/{len(TOKENS)}',flush=True)
    (OUT/'targeted_owner_resolution.json').write_text(json.dumps({'snapshot_block':SNAPSHOT_BLOCK,'rows':rows},indent=2),encoding='utf-8')
    unresolved=[r['canonical_number'] for r in rows if not any(x.get('balance',0)>0 for x in r['positive_balances_at_snapshot'])]
    (OUT/'targeted_owner_summary.json').write_text(json.dumps({'resolved':len(rows)-len(unresolved),'unresolved':unresolved,'rows':[{'canonical_number':r['canonical_number'],'token_id_decimal':r['token_id_decimal'],'positive_balances_at_snapshot':r['positive_balances_at_snapshot'],'owner_href':r['owner_href']} for r in rows]},indent=2),encoding='utf-8')
    print(json.dumps({'resolved':len(rows)-len(unresolved),'unresolved':unresolved},indent=2),flush=True)

if __name__=='__main__': main()
