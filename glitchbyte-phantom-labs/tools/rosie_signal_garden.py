#!/usr/bin/env python3
"""RosieGlitchbyte Phantom Labs: Signal Garden, offline research organizer."""
import argparse
import csv
import hashlib
import html
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

PINK='\033[95m'; CYAN='\033[96m'; GREEN='\033[92m'; RED='\033[91m'; RESET='\033[0m'
URL_RE = re.compile(r'https?://[^\s<>"\'`]+', re.I)
DATE_RE = re.compile(r'\b(?:20\d{2}-\d{2}-\d{2})(?:[T ][0-2]\d:[0-5]\d(?::[0-5]\d)?)?\b')

def banner():
    print(PINK + r'''    .-._.-.   ROSIEGLITCHBYTE   .-._.-.
   (  / \  )  SIGNAL GARDEN     (  / \  )
    `-\_/-'   PHANTOM LABS #001 `-\_/-'
      /|\      *  .  *  .        /|\
     /_|_\   LINK // TRACE // BLOOM /_|_/''' + RESET)
    print(CYAN+'    [ OFFLINE INTEL • NO API • YOUR OWN FILES ]'+RESET+'\n')

def safe_domain(url):
    try:
        p=urlsplit(url)
        if p.scheme not in ('http','https') or not p.hostname: return None
        return p.hostname.lower().rstrip('.')
    except ValueError: return None

def scan_file(path):
    raw=path.read_bytes()
    text=raw.decode('utf-8',errors='replace')
    urls=[]
    for match in URL_RE.finditer(text):
        url=match.group().rstrip('.,;:!?)]}')
        domain=safe_domain(url)
        if domain: urls.append({'url':url,'domain':domain,'source':path.name})
    timeline=[]
    for line_no,line in enumerate(text.splitlines(),1):
        dates=DATE_RE.findall(line)
        for date in dates:
            timeline.append({'date':date,'source':path.name,'line':line_no,'note':line.strip()[:500]})
    return {'name':path.name,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'urls':urls,'timeline':timeline,'text':text}

def gather(folder):
    files=sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in ('.txt','.md','.csv','.json','.log'))
    return [scan_file(p) for p in files if p.stat().st_size<=5_000_000]

def report(data, keyword):
    urls=[u for f in data for u in f['urls']]
    domains=Counter(u['domain'] for u in urls)
    repeats=Counter(u['url'] for u in urls)
    timeline=sorted((t for f in data for t in f['timeline']),key=lambda x:x['date'])
    hits=[]
    if keyword:
        for f in data:
            for n,line in enumerate(f['text'].splitlines(),1):
                if keyword.casefold() in line.casefold():
                    hits.append({'source':f['name'],'line':n,'text':line.strip()[:500]})
    return {'project':'ROSIEGLITCHBYTE SIGNAL GARDEN','generated_utc':datetime.now(timezone.utc).isoformat(),
            'files':[{'name':f['name'],'size_bytes':f['size'],'sha256':f['sha256']} for f in data],
            'links':urls,'domains':dict(domains.most_common()),
            'duplicates':[{'url':u,'count':n} for u,n in repeats.most_common() if n>1],
            'timeline':timeline,'keyword':keyword,'keyword_hits':hits}

def save_report(r,out):
    out.mkdir(parents=True,exist_ok=True)
    (out/'signal_garden.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8')
    with (out/'signal_links.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['url','domain','source']);w.writeheader();w.writerows(r['links'])
    with (out/'signal_timeline.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['date','source','line','note']);w.writeheader();w.writerows(r['timeline'])
    h=lambda s:html.escape(str(s),quote=True)
    domain_rows=''.join(f'<tr><td>{h(d)}</td><td>{n}</td></tr>' for d,n in r['domains'].items())
    link_rows=''.join(f'<tr><td>{h(x["url"])}</td><td>{h(x["domain"])}</td><td>{h(x["source"])}</td></tr>' for x in r['links'])
    time_rows=''.join(f'<tr><td>{h(x["date"])}</td><td>{h(x["source"])}</td><td>{h(x["note"])}</td></tr>' for x in r['timeline'])
    hit_rows=''.join(f'<tr><td>{h(x["source"])}</td><td>{x["line"]}</td><td>{h(x["text"])}</td></tr>' for x in r['keyword_hits'])
    file_rows=''.join(f'<tr><td>{h(x["name"])}</td><td>{x["size_bytes"]}</td><td><code>{h(x["sha256"])}</code></td></tr>' for x in r['files'])
    page=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RosieGlitchbyte | Signal Garden</title>
<style>body{{background:#0c0a17;color:#e8e8f4;font:16px system-ui;margin:0;padding:24px}}main{{max-width:1100px;margin:auto}}h1{{color:#ff4fb7;text-shadow:0 0 18px #9c2bc9}}h2{{color:#54eaff}}.tag{{color:#9bffa5}}section{{background:#161327;border:1px solid #53366d;border-radius:15px;padding:18px;margin:18px 0;overflow:auto}}table{{border-collapse:collapse;width:100%}}td,th{{text-align:left;padding:10px;border-bottom:1px solid #3b2a50;overflow-wrap:anywhere}}th{{color:#ff85d1}}input{{padding:12px;border:1px solid #ae50ff;background:#0a0915;color:white;width:min(96%,500px);border-radius:8px}}code{{font-size:12px}}.small{{color:#a5a4b8}}</style>
<main><h1>♡ ROSIEGLITCHBYTE // SIGNAL GARDEN</h1><p class="tag">PHANTOM LABS #001 • OFFLINE RESEARCH ARCHIVE</p><p>{len(r['files'])} files • {len(r['links'])} links • {len(r['domains'])} domains • {len(r['timeline'])} dated entries</p><input id="search" placeholder="Filter all tables by text..." aria-label="Filter tables"><section><h2>Domain Map</h2><table><thead><tr><th>Domain</th><th>Links</th></tr></thead><tbody>{domain_rows}</tbody></table></section>
<section><h2>Harvested Links</h2><table><thead><tr><th>URL</th><th>Domain</th><th>Source</th></tr></thead><tbody>{link_rows}</tbody></table></section><section><h2>Timeline</h2><table><thead><tr><th>Date</th><th>Source</th><th>Note</th></tr></thead><tbody>{time_rows}</tbody></table></section>
<section><h2>Keyword Hits: {h(r['keyword'] or '(none)')}</h2><table><tbody>{hit_rows}</tbody></table></section><section><h2>File Fingerprints</h2><table><thead><tr><th>File</th><th>Bytes</th><th>SHA-256</th></tr></thead><tbody>{file_rows}</tbody></table></section><p class="small">Local-file analysis only. Links are not fetched or verified. Matching domains do not establish common ownership.</p></main><script>document.getElementById('search').addEventListener('input',e=>{{let q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(row=>row.hidden=!row.textContent.toLowerCase().includes(q))}})</script></html>'''
    (out/'signal_garden.html').write_text(page,encoding='utf-8')

def main():
    parser=argparse.ArgumentParser(description='RosieGlitchbyte offline link and research analyzer')
    parser.add_argument('--folder',default=str(Path.home()/'RosieSignalGarden'/'input'))
    parser.add_argument('--output',default=str(Path.home()/'RosieSignalGarden'/'reports'))
    parser.add_argument('--keyword',default='')
    parser.add_argument('--demo',action='store_true',help='Create a harmless example research note')
    args=parser.parse_args();banner()
    folder=Path(args.folder).expanduser();out=Path(args.output).expanduser()
    folder.mkdir(parents=True,exist_ok=True)
    if args.demo:
        (folder/'demo_notes.txt').write_text('2026-10-10 Public research: https://example.org/news\n2026-10-11 Compare https://www.python.org/ and https://example.org/news\nKeyword: phantom\n',encoding='utf-8')
        print(GREEN+'[GARDEN] Created example notes.'+RESET)
    data=gather(folder)
    if not data:
        print(RED+f'[EMPTY] Put .txt, .md, .csv, .json, or .log files into {folder}'+RESET)
        print('Or try: python3 rosie_signal_garden.py --demo')
        return 0
    r=report(data,args.keyword);save_report(r,out)
    print(CYAN+f'[HARVEST] {len(data)} files | {len(r["links"])} links | {len(r["domains"])} domains'+RESET)
    print(PINK+f'[TIMELINE] {len(r["timeline"])} dated notes | [KEYWORD] {len(r["keyword_hits"])} matches'+RESET)
    print(GREEN+f'[SAVED] {out / "signal_garden.html"}'+RESET)
    print('Open the HTML report in Firefox or another browser.')
    return 0

if __name__=='__main__':
    sys.exit(main())
