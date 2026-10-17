#!/usr/bin/env python3
"""GlitchbyteRosie X Intel Phantom: public X API research CLI.
Requires X API bearer token and access to corresponding endpoints.
No third-party dependencies. Python 3.9+.
"""
import argparse, collections, csv, datetime as dt, json, os, pathlib, re, sys, time
import urllib.error, urllib.parse, urllib.request

BASE = 'https://api.x.com/2'
RESET='\033[0m'; COLORS=['\033[95m','\033[96m','\033[91m','\033[93m','\033[92m','\033[94m']
def color(s, i=0): return (COLORS[i%len(COLORS)]+str(s)+RESET) if sys.stdout.isatty() and not os.getenv('NO_COLOR') else str(s)
def say(s,i=0): print(color(s,i))
def banner():
    print('\n'+color('═'*66,0));say('  GLITCHBYTEROSIE // X_INTEL_PHANTOM.EXE',1);say('  PUBLIC SIGNALS  •  POSTS  •  REPOSTS  •  KEYWORDS',2);print(color('═'*66,0))

class APIError(Exception): pass
class XAPI:
    def __init__(self, token): self.token=token.strip()
    def get(self, endpoint, params=None):
        url=BASE+endpoint
        if params: url+='?'+urllib.parse.urlencode(params, doseq=True)
        req=urllib.request.Request(url,headers={'Authorization':'Bearer '+self.token,'User-Agent':'GlitchbyteRosiePublicIntel/1.0','Accept':'application/json'})
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req,timeout=25) as resp: return json.load(resp)
            except urllib.error.HTTPError as e:
                body=e.read(1000).decode('utf-8','replace')
                if e.code==429 and attempt==0:
                    say('[RATE LIMIT] Waiting 15 seconds before one retry...',2);time.sleep(15);continue
                raise APIError(f'HTTP {e.code}: {body}') from None
            except (urllib.error.URLError,TimeoutError) as e: raise APIError(f'Network error: {e}') from None
        raise APIError('Rate limited')

USER_FIELDS='created_at,description,entities,location,name,profile_image_url,protected,public_metrics,url,username,verified,verified_type'
TWEET_FIELDS='created_at,author_id,conversation_id,entities,lang,public_metrics,referenced_tweets,attachments,in_reply_to_user_id,possibly_sensitive'
EXPANSIONS='author_id,referenced_tweets.id,attachments.media_keys'
MEDIA_FIELDS='type,url,preview_image_url,alt_text'
def opts(): return {'tweet.fields':TWEET_FIELDS,'expansions':EXPANSIONS,'media.fields':MEDIA_FIELDS,'user.fields':USER_FIELDS}
def lookup(api, username):
    return api.get('/users/by/username/'+urllib.parse.quote(username.lstrip('@'),safe=''),{'user.fields':USER_FIELDS})
def user_posts(api, uid, kind='tweets', pages=1):
    ep=f'/users/{uid}/'+kind
    params={'max_results':100,**opts()}
    return paginate(api,ep,params,pages)
def search(api,query,pages=1,start=None,end=None,archive=False):
    params={'query':query,'max_results':100,**opts()}
    if start: params['start_time']=iso(start)
    if end: params['end_time']=iso(end)
    return paginate(api,'/tweets/search/'+('all' if archive else 'recent'),params,pages)
def iso(v):
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}',v): v+='T00:00:00Z'
    return v
def paginate(api, endpoint, params, pages):
    pages=max(1,min(pages,10)); items=[]; includes={}; meta=[]
    for i in range(pages):
        say(f'[SCAN] Requesting page {i+1}/{pages} ...',i)
        result=api.get(endpoint,params)
        items.extend(result.get('data',[]));meta.append(result.get('meta',{}))
        for typ,values in result.get('includes',{}).items():
            includes.setdefault(typ,{})
            for v in values: includes[typ][v.get('id',v.get('media_key',str(len(includes[typ]))))]=v
        token=result.get('meta',{}).get('next_token')
        if not token: break
        params=dict(params,pagination_token=token)
        time.sleep(.5)
    return {'data':items,'includes':{k:list(v.values()) for k,v in includes.items()},'meta':meta}

def links(post):
    return [u.get('expanded_url',u.get('url','')) for u in post.get('entities',{}).get('urls',[]) if u.get('expanded_url') or u.get('url')]
def analysis(data):
    posts=data.get('data',[]); tags=collections.Counter(); mentions=collections.Counter(); domains=collections.Counter(); langs=collections.Counter(); refs=collections.Counter(); engagement=collections.Counter(); urls=[]; media=[]
    for p in posts:
        ent=p.get('entities',{}); langs[p.get('lang','unknown')]+=1
        for t in ent.get('hashtags',[]): tags[t.get('tag','')]+=1
        for m in ent.get('mentions',[]): mentions[m.get('username','')]+=1
        for u in links(p):
            urls.append({'post_id':p.get('id'),'url':u}); host=urllib.parse.urlparse(u).hostname
            if host: domains[host.lower()]+=1
        for ref in p.get('referenced_tweets',[]): refs[ref.get('type','unknown')]+=1
        for k,v in p.get('public_metrics',{}).items():
            if isinstance(v,int): engagement[k]+=v
        for key in p.get('attachments',{}).get('media_keys',[]): media.append({'post_id':p.get('id'),'media_key':key})
    top=lambda c: c.most_common(40)
    return {'post_count':len(posts),'hashtags':top(tags),'mentions':top(mentions),'domains':top(domains),'languages':top(langs),'post_types':dict(refs),'engagement_totals':dict(engagement),'urls':urls,'media_references':media}

def export(label,result,folder):
    folder=pathlib.Path(folder);folder.mkdir(parents=True,exist_ok=True)
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S')
    safe=re.sub(r'[^A-Za-z0-9_-]+','_',label)[:50] or 'research'
    stem=folder/f'glitchbyte_{safe}_{stamp}'
    report={'tool':'GlitchbyteRosie X Intel Phantom','collected_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'label':label,'result':result}
    (stem.with_suffix('.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    rows=result.get('data',[]) if isinstance(result,dict) else []
    with (stem.with_suffix('.csv')).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['id','created_at','author_id','text','post_url','likes','reposts','replies','quotes','links','hashtags'])
        w.writeheader()
        for p in rows:
            m=p.get('public_metrics',{}); pid=p.get('id','')
            w.writerow({'id':pid,'created_at':p.get('created_at',''),'author_id':p.get('author_id',''),'text':p.get('text',''),'post_url':f'https://x.com/i/web/status/{pid}' if pid else '', 'likes':m.get('like_count',''),'reposts':m.get('retweet_count',''),'replies':m.get('reply_count',''),'quotes':m.get('quote_count',''),'links':' | '.join(links(p)),'hashtags':' | '.join(h.get('tag','') for h in p.get('entities',{}).get('hashtags',[]))})
    say(f'[SAVED] {stem}.json',4);say(f'[SAVED] {stem}.csv',4)

def show(result):
    posts=result.get('data',[])
    for p in posts[:15]:
        say(f"\n[{p.get('created_at','?')}] https://x.com/i/web/status/{p.get('id','')}",1)
        print(p.get('text','').replace('\n',' ')[:250])
    if len(posts)>15: say(f'...and {len(posts)-15} more posts in exported report.',3)
    stats=analysis(result);say(f"\n[INTEL] {stats['post_count']} posts | Top tags: {stats['hashtags'][:8]}",4)
    say(f"[INTEL] Domains: {stats['domains'][:8]} | Post types: {stats['post_types']}",5)
    result['analysis']=stats

def main():
    ap=argparse.ArgumentParser(description='GlitchbyteRosie X public account research (official API)')
    ap.add_argument('--username',help='X username without @');ap.add_argument('--query',help='X search syntax')
    ap.add_argument('--mode',type=int,help='Menu option 1-16');ap.add_argument('--pages',type=int,default=1,help='Up to 10 pages of 100 results')
    ap.add_argument('--start',help='UTC start YYYY-MM-DD or ISO timestamp');ap.add_argument('--end',help='UTC end YYYY-MM-DD or ISO timestamp')
    ap.add_argument('--archive',action='store_true',help='Use full-archive search endpoint (requires plan access)')
    ap.add_argument('--output',default='glitchbyte_reports');args=ap.parse_args()
    banner()
    token=os.getenv('X_BEARER_TOKEN','').strip()
    if not token:
        say('[SETUP] Set X_BEARER_TOKEN in your environment first.',2)
        say('Example: export X_BEARER_TOKEN="your_own_developer_bearer_token"',1)
        say('Get API access from https://developer.x.com/ ; availability varies by plan.',3)
        return 2
    api=XAPI(token)
    modes={1:'Account profile',2:'Account stats and bio',3:'Recent posts',4:'Replies',5:'Reposts and quotes',6:'Keyword search',7:'Hashtag search',8:'Mentions',9:'Date-range search',10:'Shared URLs and domains',11:'Hashtags and keyword frequency',12:'Engagement summary',13:'Media references',14:'Public followers/following (plan permitting)',15:'Full account report',16:'Custom search + export'}
    for n,label in modes.items(): say(f' [{n:02}] {label}',n)
    try:
        mode=args.mode or int(input('\n[MODE] Select 1-16: ').strip())
        if mode not in modes: raise ValueError('Choose a menu option 1-16')
        username=args.username or (input('[TARGET] X username: ').strip().lstrip('@') if mode not in (6,7,16) else '')
        pages=max(1,min(args.pages,10));result={};label=username or 'search'
        if mode in (6,7,16):
            q=args.query or input('[SEARCH] Keyword / hashtag / X query: ').strip()
            if mode==7 and not q.startswith('#'): q='#'+q.lstrip('#')
            result=search(api,q,pages,args.start,args.end,args.archive);label=q
        elif mode==8:
            result=search(api,f'@{username}',pages,args.start,args.end,args.archive)
        elif mode==9:
            result=search(api,args.query or f'from:{username}',pages,args.start,args.end,args.archive)
        elif mode==14:
            u=lookup(api,username).get('data',{});uid=u.get('id')
            if not uid: raise APIError('Account not found or unavailable')
            relationship=input('[RELATION] followers or following? ').strip().lower()
            if relationship not in ('followers','following'): raise ValueError('Enter followers or following')
            result=paginate(api,f'/users/{uid}/{relationship}',{'max_results':100,'user.fields':USER_FIELDS},pages)
        else:
            user=lookup(api,username)
            if mode in (1,2): result={'profile':user.get('data',{}),'data':[]}
            else:
                uid=user.get('data',{}).get('id')
                if not uid: raise APIError('Account not found or unavailable')
                if mode==4: result=user_posts(api,uid,'tweets',pages) # authored replies
                elif mode==5: result=user_posts(api,uid,'tweets',pages)
                else: result=user_posts(api,uid,'tweets',pages)
                if mode==4: result['data']=[p for p in result['data'] if p.get('in_reply_to_user_id') or p.get('text','').lstrip().startswith('@')]
                if mode==5: result['data']=[p for p in result['data'] if any(r.get('type') in ('retweeted','quoted') for r in p.get('referenced_tweets',[]))]
                result['profile']=user.get('data',{})
        if 'profile' in result: say('[PROFILE] '+json.dumps(result['profile'],ensure_ascii=False,indent=2),0)
        if 'data' in result: show(result)
        export(label,result,args.output)
        say('[COMPLETE] Public intelligence archived. No cookies or login sessions collected.',4)
        return 0
    except (APIError,ValueError,KeyboardInterrupt) as e:
        say(f'[ERROR] {e}',2);return 1

if __name__=='__main__': sys.exit(main())
