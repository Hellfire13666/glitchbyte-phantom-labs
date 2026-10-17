#!/usr/bin/env python3
"""Glitchbyte Phantom Labs: Log Constellation, an offline log anomaly explorer."""
import argparse, collections, datetime as dt, hashlib, html, json, pathlib, re, statistics, sys
from urllib.parse import urlsplit

HOME = pathlib.Path.home() / 'GlitchbyteLogConstellation'
ANSI = {'pink':'\033[95m','cyan':'\033[96m','green':'\033[92m','end':'\033[0m'}
LEVEL = re.compile(r'\b(TRACE|DEBUG|INFO|NOTICE|WARN(?:ING)?|ERROR|CRITICAL|FATAL)\b', re.I)
IP = re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])')
DATE = re.compile(r'\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:?\d{2})?')
SECRETS = re.compile(r'(?i)\b(authorization\s*:\s*(?:bearer|basic)\s+|(?:api[_-]?key|access[_-]?token|password|passwd|secret|cookie|session[_-]?id)\s*[=:]\s*)["\']?([^\s,"\';]+)')
EMAIL = re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
URL = re.compile(r'https?://[^\s<>"\']+', re.I)

def scrub(line):
    line = SECRETS.sub(lambda m: m.group(1) + '[REDACTED]', line)
    line = EMAIL.sub('[EMAIL]', line)
    return line

def parse_file(path, limit):
    events=[]
    with path.open('r', encoding='utf-8', errors='replace') as fh:
        for i, raw in enumerate(fh,1):
            if i > limit: break
            line=scrub(raw.strip())[:800]
            if not line: continue
            level=LEVEL.search(line)
            date=DATE.search(line)
            urls=[]
            for u in URL.findall(line):
                try:
                    host=urlsplit(u.rstrip('.,;)')).hostname
                    if host: urls.append(host.lower())
                except ValueError: pass
            events.append({'line':i,'level':(level.group(1).upper().replace('WARNING','WARN') if level else 'OTHER'),
                           'time':date.group(0) if date else '', 'message':line,
                           'ip_count':len(IP.findall(line)), 'hosts':list(dict.fromkeys(urls))})
    return events

def render(report):
    data=json.dumps(report,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GLITCHBYTE // LOG CONSTELLATION</title><style>
:root{color-scheme:dark;font-family:ui-monospace,Consolas,monospace;background:#090a16;color:#e9e8ff}
body{max-width:1150px;margin:30px auto;padding:0 18px}h1{color:#ff63be;text-shadow:0 0 16px #ff4aaf70;letter-spacing:.07em}
small,.muted{color:#a7a6c7}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:22px 0}
.card{background:#15162b;border:1px solid #383153;border-radius:12px;padding:16px}.number{font-size:1.7rem;color:#66e8f7}
input,select{background:#171a32;color:white;border:1px solid #66618b;padding:10px;border-radius:8px;margin:8px 8px 8px 0}
.entry{border-left:3px solid #5ee6e8;padding:10px 12px;margin:9px 0;background:#131629;border-radius:5px;overflow-wrap:anywhere}
.ERROR,.CRITICAL,.FATAL{border-color:#ff638b}.WARN{border-color:#ffd36c}.time{color:#80d7ec}.tag{font-size:.75rem;color:#c2a2fa}
.bar{height:12px;background:#2b2a4b;border-radius:12px;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,#ff64b9,#58ebf3)}
</style><h1>✿ GLITCHBYTE // LOG CONSTELLATION</h1><p class="muted">PHANTOM LABS • Offline anomaly explorer • Sensitive values redacted</p>
<div class="stats" id="stats"></div><section class="card"><h2>Signal distribution</h2><div id="levels"></div></section>
<h2>Event telescope</h2><input id="search" placeholder="Search log messages" aria-label="Search log messages"><select id="level"><option value="">All levels</option></select>
<div id="entries"></div><script id="payload" type="application/json">''' + data + '''</script><script>
const d=JSON.parse(document.getElementById('payload').textContent);const $=id=>document.getElementById(id);
function el(tag,cls,text){let n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=String(text);return n}
[['Events',d.total],['Errors / critical',d.error_count],['Warnings',d.warning_count],['IP mentions',d.ip_mentions],['Unique URL hosts',d.unique_hosts]].forEach(([k,v])=>{let c=el('div','card');c.append(el('div','muted',k),el('div','number',v));$('stats').append(c)});
let max=Math.max(1,...Object.values(d.levels));Object.entries(d.levels).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>{
let wrap=el('div','');wrap.append(el('p','',k+'  '+v));let bar=el('div','bar'),fill=el('div','fill');fill.style.width=(100*v/max)+'%';bar.append(fill);wrap.append(bar);$('levels').append(wrap);
$('level').append(new Option(k,k));});
function show(){let q=$('search').value.toLowerCase(),level=$('level').value;let box=$('entries');box.replaceChildren();let found=0;
for(let e of d.events){if(level&&e.level!==level)continue;if(q&&!e.message.toLowerCase().includes(q))continue;
let item=el('div','entry '+e.level);item.append(el('div','tag',e.level+' • line '+e.line+(e.time?' • '+e.time:'')),el('div','',e.message));box.append(item);found++;if(found>=500){box.append(el('p','muted','Showing first 500 matches. Narrow your search.'));break;}}
if(!found)box.append(el('p','muted','No matching events.'));}
$('search').addEventListener('input',show);$('level').addEventListener('change',show);show();
</script></html>'''

def demo(folder):
    folder.mkdir(parents=True,exist_ok=True)
    path=folder/'demo.log'
    base=dt.datetime(2026,10,16,10,0)
    with path.open('w',encoding='utf-8') as f:
        for i in range(120):
            level='ERROR' if i%19==0 else ('WARN' if i%11==0 else 'INFO')
            msg=('connection timeout to https://status.example.org/health' if level=='ERROR' else
                 'queue depth above threshold' if level=='WARN' else 'worker heartbeat healthy')
            if i==41: msg+=' api_key=EXAMPLE_DEMO_TOKEN'
            f.write(f'{(base+dt.timedelta(seconds=i*25)).isoformat()} {level} {msg}\n')
    return path

def main():
    p=argparse.ArgumentParser(description='Offline log analysis with redacted HTML and JSON reports')
    p.add_argument('files',nargs='*',type=pathlib.Path,help='Local log/text files to inspect')
    p.add_argument('--demo',action='store_true',help='Generate and analyze a safe sample log')
    p.add_argument('--out',type=pathlib.Path,default=HOME/'reports',help='Report folder')
    p.add_argument('--max-lines',type=int,default=100000,help='Maximum lines per file (default 100000)')
    args=p.parse_args()
    if args.max_lines<1 or args.max_lines>1000000: p.error('--max-lines must be 1..1000000')
    if args.demo: args.files.append(demo(HOME/'samples'))
    if not args.files: p.error('Provide log file(s) or use --demo')
    all_events=[];sources=[]
    for path in args.files:
        if not path.is_file(): print(f'Skipping missing file: {path}',file=sys.stderr);continue
        events=parse_file(path,args.max_lines)
        for e in events:e['source']=path.name
        all_events.extend(events)
        sources.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'events':len(events)})
    if not sources: return 2
    counts=collections.Counter(e['level'] for e in all_events)
    hosts={h for e in all_events for h in e['hosts']}
    report={'project':'GLITCHBYTE LOG CONSTELLATION','generated_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'sources':sources,'total':len(all_events),'levels':dict(counts),
            'error_count':sum(counts[k] for k in ('ERROR','CRITICAL','FATAL')),
            'warning_count':counts['WARN'],'ip_mentions':sum(e['ip_count'] for e in all_events),
            'unique_hosts':len(hosts),'hosts':sorted(hosts),'events':all_events}
    args.out.mkdir(parents=True,exist_ok=True)
    jsonpath=args.out/'constellation.json';htmlpath=args.out/'constellation.html'
    jsonpath.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    htmlpath.write_text(render(report),encoding='utf-8')
    print('\033[95m✿ GLITCHBYTE // LOG CONSTELLATION\033[0m')
    print(f'Analyzed {len(sources)} files / {len(all_events)} events | errors: {report["error_count"]} | warnings: {report["warning_count"]}')
    print(f'HTML: {htmlpath}\nJSON: {jsonpath}')
    return 0

if __name__=='__main__':raise SystemExit(main())
