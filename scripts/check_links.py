#!/usr/bin/env python3
"""Optional public-URL probe. Explicit network access; never treats 403/429 as dead."""
from __future__ import annotations
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]

def classify(code: int) -> str:
    if 200 <= code < 400:
        return 'reachable'
    if code in (401,403,429):
        return 'blocked_or_rate_limited'
    if code in (404,410):
        return 'not_found_reported'
    return 'http_error'


def probe(url: str, timeout: float) -> dict:
    for attempt in range(2):
        method='HEAD'
        try:
            req=Request(url,method=method,headers={'User-Agent':'awesome-gpt6-embodied-linkcheck/0.1'})
            try:
                response=urlopen(req,timeout=timeout)
            except HTTPError as exc:
                if exc.code != 405:
                    raise
                # Read at most a tiny range when a server does not implement HEAD.
                response=urlopen(Request(url,headers={'Range':'bytes=0-0','User-Agent':'awesome-gpt6-embodied-linkcheck/0.1'}),timeout=timeout)
            with response:
                return {'url':url,'status':classify(response.status),'http_status':response.status,'final_url':response.url}
        except HTTPError as exc:
            if exc.code >= 500 and attempt == 0:
                time.sleep(0.5)
                continue
            return {'url':url,'status':classify(exc.code),'http_status':exc.code}
        except (URLError,TimeoutError,OSError) as exc:
            if attempt==0:
                time.sleep(0.5)
                continue
            return {'url':url,'status':'network_unverified','error':str(exc)[:250]}
    return {'url':url,'status':'network_unverified'}


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',action='store_true',help='Explicitly permit public network requests')
    p.add_argument('--timeout',type=float,default=10)
    p.add_argument('--workers',type=int,default=2)
    p.add_argument('--limit',type=int,default=0,help='0 means all unique source URLs')
    p.add_argument('--output',type=Path,default=Path('link-report.json'))
    a=p.parse_args()
    if not a.run:
        p.error('Network checking is opt-in. Pass --run to request public source URLs.')
    if not 0<a.timeout<=60 or not 1<=a.workers<=4 or a.limit<0:
        p.error('Use timeout (0,60], workers 1..4 and limit >=0.')
    sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
    urls=list(dict.fromkeys(s['url'] for s in sources))
    if a.limit:
        urls=urls[:a.limit]
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        results=list(pool.map(lambda url:probe(url,a.timeout),urls))
    payload={'note':'Reachability does not verify content, authority or reproduction. Errors may reflect blocking.','results':results}
    a.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(results)} probe results to {a.output}; review them manually.')
    return 0

if __name__=='__main__':
    sys.exit(main())
