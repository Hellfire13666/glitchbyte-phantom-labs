#!/usr/bin/env python3
"""ROSE CRAWLER | Public social-profile discovery and respectful metadata collection."""
import argparse
import uuid, csv, datetime as dt, html, json, re, sys, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.robotparser import RobotFileParser

AGENT = 'RoseCrawlerResearch/1.0 (+public-profile-research; respectful robots)' 
PLATFORMS = {
    'GitHub': 'https://github.com/{u}',
    'GitLab': 'https://gitlab.com/{u}',
    'Reddit': 'https://www.reddit.com/user/{u}/',
    'Mastodon.social': 'https://mastodon.social/@{u}',
    'Bluesky': 'https://bsky.app/profile/{u}',
    'Pinterest': 'https://www.pinterest.com/{u}/',
    'Tumblr': 'https://{u}.tumblr.com/',
    'YouTube': 'https://www.youtube.com/@{u}',
    'TikTok': 'https://www.tiktok.com/@{u}',
    'Instagram': 'https://www.instagram.com/{u}/',
    'X': 'https://x.com/{u}',
    'Threads': 'https://www.threads.net/@{u}',
}
COLORS = {'pink':'\033[95m','cyan':'\033[96m','green':'\033[92m','dim':'\033[2m','reset':'\033[0m'}
class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=''; self.description=''; self.links=[]; self.in_title=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.in_title=True
        if tag=='meta' and (a.get('name','').lower()=='description' or a.get('property','').lower()=='og:description'):
            if not self.description: self.description=a.get('content','')
        if tag=='a' and a.get('href') and len(self.links)<40:
            href=a['href']
            if href.startswith('https://') or href.startswith('http://'): self.links.append(href)
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
    def handle_data(self, data):
        if self.in_title: self.title+=data

def robots_allows(url):
    p=urlparse(url); robots=f'{p.scheme}://{p.netloc}/robots.txt'
    try:
        req=Request(robots,headers={'User-Agent':AGENT})
        with urlopen(req,timeout=9) as resp:
            data=resp.read(250_000).decode('utf-8','replace')
        rp=RobotFileParser(); rp.parse(data.splitlines()); return rp.can_fetch(AGENT,url), 'robots.txt checked'
    except HTTPError as e:
        if e.code in (401,403): return False, f'robots.txt blocked ({e.code})'
        if e.code==404: return True, 'no robots.txt (404)'
        return False, f'robots.txt unavailable ({e.code})'
    except (URLError,TimeoutError,ValueError): return False, 'robots.txt could not be verified'

def inspect(name,url,fetch,delay):
    record={'platform':name,'url':url,'status':'not checked','http_status':'','title':'','description':'','public_links':[],'note':'','checked_at':dt.datetime.now(dt.timezone.utc).isoformat()}
    if not fetch:
        record['status']='manual review'; record['note']='URL generated; existence not verified'; return record
    allowed,reason=robots_allows(url)
    if not allowed:
        record['status']='restricted'; record['note']=reason; return record
    time.sleep(delay)
    try:
        req=Request(url,headers={'User-Agent':AGENT,'Accept':'text/html'})
        with urlopen(req,timeout=12) as response:
            final=response.geturl(); content_type=response.headers.get('Content-Type','')
            record['http_status']=response.status
            if urlparse(final).netloc.lower()!=urlparse(url).netloc.lower():
                record['status']='uncertain'; record['note']='Redirected to another host; no content collected'; return record
            if 'text/html' not in content_type.lower():
                record['status']='uncertain'; record['note']='Response is not HTML'; return record
            data=response.read(250_000).decode('utf-8','replace')
        meta=Metadata(); meta.feed(data)
        record['title']=meta.title.strip()[:250]; record['description']=meta.description.strip()[:500]
        record['public_links']=list(dict.fromkeys(meta.links))[:20]
        record['status']='reachable (unverified profile)'
        record['note']='HTTP 200 does not establish account ownership or existence; platform may show login/placeholder page'
    except HTTPError as e:
        record['http_status']=e.code
        record['status']='not found' if e.code==404 else 'restricted' if e.code in (401,403,429) else 'uncertain'
        record['note']=f'HTTP {e.code}'
    except (URLError,TimeoutError,ValueError) as e:
        record['status']='uncertain'; record['note']=str(e)[:160]
    return record

def write_report(records,output,username):
    output.mkdir(parents=True,exist_ok=True)
    stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    base=output/f'rose_{username}_{stamp}_{uuid.uuid4().hex[:12]}'
    (Path(str(base)+'.json')).write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
    with Path(str(base)+'.csv').open('w',newline='',encoding='utf-8') as f:
        cols=['platform','url','status','http_status','title','description','note','checked_at']
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows({k:r.get(k,'') for k in cols} for r in records)
    rows=''.join('<tr>'+''.join(f'<td>{html.escape(str(r.get(k,"")))}</td>' for k in ('platform','url','status','title','description','note'))+'</tr>' for r in records)
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rose Crawler</title><style>body{background:#100c1b;color:#f5eaff;font:16px system-ui;margin:0;padding:30px}h1{color:#ff58af}p{color:#75e9ee}input{padding:12px;width:95%;background:#20172c;color:white;border:1px solid #ff58af;border-radius:8px}table{width:100%;border-collapse:collapse;margin-top:18px}td,th{border-bottom:1px solid #41324d;padding:12px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{color:#75e9ee}tr:hover{background:#251a35}</style><h1>🌹 ROSE CRAWLER // PHANTOM LABS</h1><p>Public-profile research. Reachable does not mean confirmed.</p><input id="q" placeholder="Filter platforms, titles, statuses..." oninput="document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.innerText.toLowerCase().includes(this.value.toLowerCase()))"><table><thead><tr><th>Platform</th><th>URL</th><th>Status</th><th>Title</th><th>Description</th><th>Notes</th></tr></thead><tbody>'''+rows+'</tbody></table></html>'
    Path(str(base)+'.html').write_text(page,encoding='utf-8')
    return base

def main():
    ap=argparse.ArgumentParser(description='Rose Crawler: respectful public social profile research')
    ap.add_argument('username',nargs='?',help='public username to research')
    ap.add_argument('--fetch',action='store_true',help='check public pages; respects robots.txt and rate limits')
    ap.add_argument('--delay',type=float,default=2.5,help='seconds between page requests (minimum 2)')
    ap.add_argument('--output',default=str(Path.home()/'RoseCrawlerReports'))
    ap.add_argument('--platforms',help='comma-separated platform names, or use --list')
    ap.add_argument('--list',action='store_true',help='list supported platforms')
    args=ap.parse_args()
    if args.list:
        print('\n'.join(PLATFORMS)); return
    if not args.username: ap.error('provide a username, e.g. python3 rose_crawler.py exampleuser')
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,40}',args.username): ap.error('username must be 1-40 characters: letters, digits, underscore, dot, hyphen')
    if args.delay<2: ap.error('--delay must be at least 2 seconds')
    names=list(PLATFORMS)
    if args.platforms:
        requested=[s.strip().lower() for s in args.platforms.split(',')]
        names=[n for n in names if n.lower() in requested]
        if not names: ap.error('no matching platforms; see --list')
    print(COLORS['pink']+r'''
       .-.-.      ROSE CRAWLER
      (  |  )     GLITCHBYTE PHANTOM LABS
       \ | /      PUBLIC SIGNAL RESEARCH
        \|/       [*] RESPECT ROBOTS  [*] NO LOGINS
         |        [*] SAVE THE EVIDENCE
        / \
    '''+COLORS['reset'])
    records=[]
    for name in names:
        url=PLATFORMS[name].format(u=quote(args.username,safe=''))
        print(f"{COLORS['cyan']}[SCAN]{COLORS['reset']} {name:17} {url}")
        r=inspect(name,url,args.fetch,args.delay); records.append(r)
        print(f"   {COLORS['green']}↳ {r['status']}{COLORS['reset']}")
    base=write_report(records,Path(args.output),args.username)
    print(f'\n🌹 Saved: {base}.html / .json / .csv')
    if not args.fetch: print('Tip: add --fetch to request allowed public pages. Without it, results are candidate URLs only.')

if __name__=='__main__': main()
