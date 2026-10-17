#!/usr/bin/env python3
"""RosieGlitchbyte HackGirl: no-API public X research workstation.
Python 3 standard library only. No login, session cookies, or bypasses.
"""
import argparse, csv, collections, datetime as dt, html, json, pathlib, re, sys, time
import urllib.parse, urllib.request, urllib.error
from html.parser import HTMLParser

HOME = pathlib.Path.home() / 'RosieGlitchbyte_Intel'
COLORS = ['\033[95m','\033[96m','\033[91m','\033[94m','\033[92m','\033[93m']
RESET='\033[0m'
UA='RosieGlitchbytePublicResearch/1.0 (public page metadata; no authentication)'
HEADERS={'User-Agent':UA, 'Accept':'text/html,application/xhtml+xml'}
POST_FIELDS=['date','username','text','url','likes','reposts','replies','quotes']

def color(s, n=0): return COLORS[n%len(COLORS)]+str(s)+RESET if sys.stdout.isatty() else str(s)
def banner():
    print('\n'+color('╔══════════════════════════════════════════════════════════╗',0))
    print(color('║  ♡ ROSIEGLITCHBYTE // HACKGIRL INTEL TERMINAL ♡         ║',1))
    print(color('║  X PUBLIC SIGNALS • NEON RECON • ZERO API KEYS          ║',2))
    print(color('╚══════════════════════════════════════════════════════════╝',3))
    print(color('[ETHICS] Public information only. No credentials or bypasses.\n',4))

def stamp(): return dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S')
def save_json(name, data):
    HOME.mkdir(parents=True,exist_ok=True)
    path=HOME/(name+'_'+stamp()+'.json')
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
    print(color('[SAVED] '+str(path),4)); return path

def handle(value):
    s=value.strip().lstrip('@')
    if not re.fullmatch(r'[A-Za-z0-9_]{1,15}',s): raise ValueError('X username must be 1-15 letters, digits, or underscores')
    return s

def fetch(url):
    req=urllib.request.Request(url,headers=HEADERS)
    try:
        with urllib.request.urlopen(req,timeout=12) as r:
            content=r.read(400_000).decode('utf-8','replace')
            return {'status':r.status,'final_url':r.geturl(),'html':content,'error':None}
    except urllib.error.HTTPError as e: return {'status':e.code,'final_url':url,'html':'','error':str(e)}
    except Exception as e: return {'status':None,'final_url':url,'html':'','error':str(e)}

class Meta(HTMLParser):
    def __init__(self): super().__init__(); self.meta={}; self.title=''; self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta':
            k=a.get('property') or a.get('name')
            if k in ('description','og:title','og:description','og:url','twitter:title','twitter:description'):
                self.meta[k]=a.get('content','')[:1000]
        if tag=='title': self.in_title=True
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
    def handle_data(self,data):
        if self.in_title: self.title+=data

def profile(username):
    u=handle(username); url='https://x.com/'+u
    print(color('[SCAN] Public webpage metadata: '+url,1))
    result=fetch(url); parser=Meta()
    if result['html']:
        try: parser.feed(result['html'])
        except Exception: pass
    out={'username':u,'url':url,'http_status':result['status'],'final_url':result['final_url'],
         'page_title':parser.title.strip()[:300], 'public_metadata':parser.meta,'error':result['error'],
         'caution':'HTTP 200 does not confirm account existence; login/interstitial pages are common.'}
    print(json.dumps(out,indent=2,ensure_ascii=False)); save_json('profile_'+u,out)
    return out

def search_url(query, engine='x'):
    if engine=='x': return 'https://x.com/search?q='+urllib.parse.quote(query,safe='')+'&src=typed_query&f=live'
    return 'https://www.google.com/search?q='+urllib.parse.quote('site:x.com '+query,safe='')

def research(username):
    u=handle(username)
    q={
        'profile':'https://x.com/'+u,
        'posts':search_url('from:'+u),
        'replies':search_url('from:'+u+' filter:replies'),
        'media':search_url('from:'+u+' filter:media'),
        'links':search_url('from:'+u+' filter:links'),
        'mentions':search_url('@'+u),
        'quoted_mentions':search_url('"@'+u+'"'),
        'reposts_research':search_url('from:'+u+' filter:nativeretweets'),
        'google_indexed':search_url('"'+u+'"','google'),
        'google_posts':search_url('"'+u+'" status','google'),
    }
    for k,v in q.items(): print(color(k.ljust(21),3)+v)
    save_json('research_links_'+u,q); return q

def keywords(query):
    query=query.strip()
    if not query or len(query)>200: raise ValueError('Enter a keyword/hashtag query up to 200 characters')
    links={'X_latest':search_url(query),'X_media':search_url(query+' filter:media'),
           'X_links':search_url(query+' filter:links'),'Google_indexed':search_url(query,'google')}
    for k,v in links.items(): print(color(k+': ',1)+v)
    save_json('keyword_links',{'query':query,'links':links}); return links

def read_posts(path):
    p=pathlib.Path(path).expanduser()
    if not p.is_file() or p.stat().st_size>20_000_000: raise ValueError('File missing or larger than 20 MB')
    if p.suffix.lower()=='.csv':
        with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    elif p.suffix.lower()=='.json':
        obj=json.loads(p.read_text(encoding='utf-8'))
        rows=obj.get('posts',[]) if isinstance(obj,dict) else obj
    else: raise ValueError('Use a CSV or JSON file')
    if not isinstance(rows,list): raise ValueError('Expected a list of posts')
    return [{k:str(v or '') for k,v in row.items()} for row in rows[:10000] if isinstance(row,dict)]

def analyze(rows,term='',since='',until=''):
    selected=[]
    for r in rows:
        body=r.get('text',r.get('full_text',''))
        date=r.get('date',r.get('created_at',''))[:10]
        if term and term.casefold() not in body.casefold(): continue
        if since and date and date<since: continue
        if until and date and date>until: continue
        selected.append(r)
    tags=collections.Counter(); mentions=collections.Counter(); domains=collections.Counter(); words=collections.Counter(); authors=collections.Counter()
    for r in selected:
        body=r.get('text',r.get('full_text',''))
        tags.update(x.lower() for x in re.findall(r'(?<!\w)#[\w]+',body))
        mentions.update(x.lower() for x in re.findall(r'(?<!\w)@[A-Za-z0-9_]{1,15}',body))
        authors.update([r.get('username','unknown') or 'unknown'])
        for url in re.findall(r'https?://[^\s<>"\']+',body):
            domain=urllib.parse.urlsplit(url.rstrip('.,!?)')).hostname
            if domain: domains[domain.lower()]+=1
        words.update(w for w in re.findall(r"[a-zA-Z]{4,}",body.lower()) if w not in {'that','this','with','from','your','have','they','will','https','http','about'})
    result={'count':len(selected),'filter':{'keyword':term,'since':since,'until':until},
            'top_hashtags':tags.most_common(25),'top_mentions':mentions.most_common(25),
            'top_domains':domains.most_common(25),'top_words':words.most_common(30),
            'authors':authors.most_common(25),'posts':selected}
    print(color('[INTEL] '+str(len(selected))+' imported posts matched.',4))
    for name in ('top_hashtags','top_mentions','top_domains','top_words'):
        print(color('\n'+name.upper(),0),result[name][:12])
    save_json('post_analysis',result)
    return result

def export_csv(rows):
    HOME.mkdir(parents=True,exist_ok=True)
    p=HOME/('posts_export_'+stamp()+'.csv')
    fields=list(dict.fromkeys(POST_FIELDS+[k for r in rows for k in r.keys()]))
    with p.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
    print(color('[CSV] '+str(p),4))

def dashboard(data):
    HOME.mkdir(parents=True,exist_ok=True)
    p=HOME/('dashboard_'+stamp()+'.html')
    def esc(v): return html.escape(str(v),quote=True)
    cards=''.join('<div class="card"><h3>'+esc(k.replace('_',' ').title())+'</h3><p>'+esc(', '.join(str(x[0])+': '+str(x[1]) for x in data.get(k,[])[:12]))+'</p></div>' for k in ('top_hashtags','top_mentions','top_domains','top_words'))
    posts=''.join('<article><small>'+esc(r.get('date',''))+' · '+esc(r.get('username',''))+'</small><p>'+esc(r.get('text',r.get('full_text','')))+'</p>'+('<a href="'+esc(r['url'])+'" rel="noopener noreferrer">Source link</a>' if r.get('url','').startswith('https://x.com/') else '')+'</article>' for r in data.get('posts',[])[:300])
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RosieGlitchbyte HackGirl Intel</title><style>body{background:#090912;color:#e9e8ff;font:16px system-ui;margin:0;padding:25px}main{max-width:1050px;margin:auto}h1{color:#ff4fcf;text-shadow:2px 2px #0ff}h2{color:#5af5fa}.card,article{background:#171527;border:1px solid #694d85;border-radius:12px;padding:16px;margin:12px 0;overflow-wrap:anywhere}small{color:#a8b2c8}a{color:#61edff}</style><main><h1>♡ ROSIEGLITCHBYTE // HACKGIRL INTEL</h1><p>Local public-data research dashboard. Imported posts only; no live X feed.</p><h2>Signals</h2>'''+cards+'<h2>Imported posts ('+str(data.get('count',0))+')</h2>'+posts+'</main></html>'
    p.write_text(page,encoding='utf-8'); print(color('[HTML] '+str(p),4))

def menu():
    banner()
    print('  [1] Public X profile metadata   [2] Account research links')
    print('  [3] Keyword/hashtag links       [4] Import CSV/JSON + analyze')
    print('  [5] Filter imported posts       [6] Export imported posts CSV')
    print('  [7] HTML intel dashboard        [8] Full public research bundle')
    print('  [9] Make sample CSV             [0] Exit')
    rows=[]; latest=None
    while True:
        try:
            choice=input(color('\n[ROSIE@INTEL] Select > ',0)).strip()
            if choice=='0': break
            if choice=='1': profile(input('X username: '))
            elif choice=='2': research(input('X username: '))
            elif choice=='3': keywords(input('Search words/hashtags: '))
            elif choice in ('4','5','6','7'):
                if choice=='4' or not rows:
                    rows=read_posts(input('Path to CSV or JSON: ')); print(color('[IMPORT] '+str(len(rows))+' posts loaded',4))
                if choice in ('4','5'):
                    term=input('Keyword filter (blank = all): ').strip()
                    since=input('From YYYY-MM-DD (optional): ').strip()
                    until=input('To YYYY-MM-DD (optional): ').strip()
                    latest=analyze(rows,term,since,until)
                elif choice=='6': export_csv(rows)
                elif choice=='7': dashboard(latest if latest else analyze(rows))
            elif choice=='8':
                u=input('X username: '); profile(u); research(u)
                q=input('Optional keyword search (Enter to skip): ').strip()
                if q: keywords(q)
            elif choice=='9': sample()
            else: print('Choose a listed option.')
        except (ValueError, OSError, json.JSONDecodeError) as e: print(color('[ERROR] '+str(e),2))
        except (KeyboardInterrupt,EOFError): print('\n[ROSIE] Signal closed.'); break

def sample():
    HOME.mkdir(parents=True,exist_ok=True)
    p=HOME/'sample_posts.csv'
    rows=[{'date':'2026-10-01','username':'demo','text':'Hello #CyberArt from @ExampleUser https://example.org','url':'https://x.com/demo/status/1'},
          {'date':'2026-10-02','username':'demo','text':'Love the neon glitch #CyberArt #GlitchByte','url':'https://x.com/demo/status/2'}]
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=POST_FIELDS);w.writeheader();w.writerows(rows)
    print(color('[SAMPLE] '+str(p),4))

def main():
    a=argparse.ArgumentParser(description='RosieGlitchbyte HackGirl public X research (no API)')
    a.add_argument('--username',help='Public username to research')
    a.add_argument('--keyword',help='Generate X keyword research links')
    a.add_argument('--import-file',help='Analyze local CSV or JSON post archive')
    a.add_argument('--filter',default='',help='Filter imported posts by keyword')
    a.add_argument('--html',action='store_true',help='Create HTML dashboard for imported posts')
    a.add_argument('--sample',action='store_true',help='Generate sample CSV')
    args=a.parse_args()
    if not any((args.username,args.keyword,args.import_file,args.sample)): return menu()
    banner()
    try:
        if args.username: profile(args.username);research(args.username)
        if args.keyword: keywords(args.keyword)
        if args.sample: sample()
        if args.import_file:
            data=analyze(read_posts(args.import_file),args.filter)
            if args.html: dashboard(data)
    except (ValueError,OSError,json.JSONDecodeError) as e:
        print(color('[ERROR] '+str(e),2));sys.exit(1)

if __name__=='__main__': main()
