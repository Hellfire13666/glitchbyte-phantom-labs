#!/usr/bin/env python3
"""GlitchbyteRosie: public X research and offline post analysis. No API keys."""
import argparse, collections, csv, datetime as dt, html, json, pathlib, re, socket, ssl, sys, time
from html.parser import HTMLParser
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

C={'red':'\033[91m','pink':'\033[95m','cyan':'\033[96m','green':'\033[92m','yellow':'\033[93m','reset':'\033[0m'}
def say(s, color='cyan'):
    print(C.get(color,'')+str(s)+C['reset'])
def banner():
    say('\n'+'═'*62,'pink'); say('  GLITCHBYTEROSIE // X_SHADOW_INTEL.EXE','red'); say('  PUBLIC SIGNALS • KEYWORDS • POST ARCHIVE • REPORTS','cyan'); say('═'*62,'pink')
def username(s):
    s=s.strip().lstrip('@')
    if not re.fullmatch(r'[A-Za-z0-9_]{1,15}',s): raise ValueError('X username must be 1-15 letters, digits or underscores')
    return s
class Meta(HTMLParser):
    def __init__(self): super().__init__(); self.title=''; self.in_title=False; self.meta={}
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.in_title=True
        if tag=='meta':
            k=a.get('property') or a.get('name')
            if k and a.get('content'): self.meta[k]=a['content']
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
    def handle_data(self, data):
        if self.in_title: self.title+=data

def public_profile(name):
    name=username(name); url='https://x.com/'+name
    result={'username':name,'url':url,'checked_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
    req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; GlitchbyteRosiePublicResearch/1.0)'})
    try:
        with urlopen(req,timeout=12) as response:
            body=response.read(600000).decode('utf-8','replace'); parser=Meta(); parser.feed(body)
            result.update(http_status=response.status,final_url=response.url,title=html.unescape(parser.title.strip()),public_metadata={k:v for k,v in parser.meta.items() if k.startswith(('og:','twitter:'))})
            result['note']='Page metadata only; HTTP success does not prove a valid profile.'
    except HTTPError as e: result.update(http_status=e.code,note='X blocked, redirected, or did not serve a public page.')
    except (URLError,TimeoutError,ssl.SSLError,OSError) as e: result.update(error=str(e),note='Could not fetch public page.')
    return result

def searches(name='',query=''):
    terms=[]
    if name:
        n=username(name)
        terms=[('Profile','https://x.com/'+n),('Posts by account','from:'+n),('Mentions','@'+n),('Replies by account','from:'+n+' filter:replies'),('Reposts by account','from:'+n+' filter:nativeretweets'),('Media posts','from:'+n+' filter:media'),('Posts with links','from:'+n+' filter:links'),('Quotes of account','url:x.com/'+n+'/status/')]
    if query: terms += [('Keyword',query),('Recent keyword',query+' filter:links'),('Keyword media',query+' filter:media')]
    return [{'label':label,'url':term if term.startswith('https://') else 'https://x.com/search?q='+quote(term,safe='')+'&f=live'} for label,term in terms]

def load_posts(path):
    path=pathlib.Path(path).expanduser(); raw=path.read_text(encoding='utf-8-sig')
    if path.suffix.lower()=='.csv':
        rows=list(csv.DictReader(raw.splitlines()))
    elif path.suffix.lower() in ('.json','.jsonl'):
        data=[json.loads(x) for x in raw.splitlines() if x.strip()] if path.suffix.lower()=='.jsonl' else json.loads(raw)
        if isinstance(data,dict): data=data.get('posts',data.get('data',[]))
        if not isinstance(data,list): raise ValueError('JSON must contain a list of posts or a posts/data list')
        rows=data
    else: raise ValueError('Import CSV, JSON or JSONL only')
    posts=[]
    for r in rows:
        if not isinstance(r,dict): continue
        text=str(r.get('text') or r.get('full_text') or r.get('content') or '')
        author=str(r.get('username') or r.get('author') or r.get('screen_name') or '')
        date=str(r.get('created_at') or r.get('date') or r.get('timestamp') or '')
        url=str(r.get('url') or r.get('post_url') or '')
        if not url and r.get('id') and author: url='https://x.com/'+author.lstrip('@')+'/status/'+str(r['id'])
        posts.append({'text':text,'username':author,'date':date,'url':url,'likes':r.get('likes',r.get('like_count','')),'reposts':r.get('reposts',r.get('retweet_count','')),'replies':r.get('replies',r.get('reply_count',''))})
    return posts

def analyze(posts,keyword='',start='',end=''):
    selected=[]; hashtags=collections.Counter(); mentions=collections.Counter(); domains=collections.Counter(); words=collections.Counter()
    for p in posts:
        text=p['text']; date=p['date'][:10]
        if keyword and keyword.casefold() not in text.casefold(): continue
        if start and (not date or date<start): continue
        if end and (not date or date>end): continue
        selected.append(p)
        hashtags.update(x.lower() for x in re.findall(r'(?<!\w)#[A-Za-z0-9_]+',text))
        mentions.update(x.lower() for x in re.findall(r'(?<!\w)@[A-Za-z0-9_]+',text))
        for url in re.findall(r'https?://[^\s<>"\']+',text):
            host=urlparse(url.rstrip('.,;)')).hostname
            if host: domains[host.lower()]+=1
        words.update(w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b',text) if w.lower() not in {'https','that','this','with','from','have','your','they','will','about'})
    return {'post_count':len(selected),'top_hashtags':hashtags.most_common(25),'top_mentions':mentions.most_common(25),'shared_domains':domains.most_common(25),'top_words':words.most_common(30),'posts':selected}

def save_report(data,prefix='glitchbyte'):
    folder=pathlib.Path.home()/'glitchbyte_x_reports'; folder.mkdir(exist_ok=True)
    stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    file=folder/(prefix+'_'+stamp+'.json'); file.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    say('[SAVED] '+str(file),'green')
    if 'posts' in data:
        csvpath=folder/(prefix+'_'+stamp+'.csv')
        with csvpath.open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=['username','date','text','url','likes','reposts','replies']); writer.writeheader(); writer.writerows(data['posts'])
        say('[SAVED] '+str(csvpath),'green')

def show_links(items):
    for i in items: say('['+i['label']+'] '+i['url'],'pink')
def menu():
    banner(); say('01  Public profile metadata','green'); say('02  Account research search links','green'); say('03  Keyword and hashtag searches','green'); say('04  Import CSV/JSON posts and analyze','green'); say('05  Filter imported posts by keyword/date','green'); say('06  Full public research bundle','green'); say('00  Exit','yellow')
    choice=input('\n[ROSIE] Choose a module > ').strip()
    try:
        if choice=='0' or choice=='00': return False
        if choice=='1' or choice=='01':
            data=public_profile(input('X username > ')); print(json.dumps(data,indent=2)); save_report(data,'profile')
        elif choice=='2' or choice=='02':
            data=searches(name=input('X username > ')); show_links(data); save_report({'search_links':data},'links')
        elif choice=='3' or choice=='03':
            data=searches(query=input('Keyword or hashtag > ')); show_links(data); save_report({'search_links':data},'keywords')
        elif choice in ('4','04','5','05'):
            posts=load_posts(input('CSV / JSON / JSONL file path > '))
            keyword=input('Keyword filter (optional) > ') if choice in ('5','05') else ''
            start=input('Start date YYYY-MM-DD (optional) > ') if choice in ('5','05') else ''
            end=input('End date YYYY-MM-DD (optional) > ') if choice in ('5','05') else ''
            data=analyze(posts,keyword,start,end)
            for k,v in data.items():
                if k!='posts': say(f'{k}: {v}','cyan')
            save_report(data,'posts')
        elif choice in ('6','06'):
            name=username(input('X username > ')); query=input('Optional keyword > ')
            data={'profile':public_profile(name),'research_links':searches(name,query)}
            print(json.dumps(data,indent=2)); save_report(data,'full')
        else: say('Unknown option.','yellow')
    except (ValueError,OSError,KeyboardInterrupt) as e: say('[ERROR] '+str(e),'red')
    return True

def main():
    ap=argparse.ArgumentParser(description='GlitchbyteRosie X public research, no API')
    ap.add_argument('--username'); ap.add_argument('--keyword'); ap.add_argument('--import-file'); ap.add_argument('--filter',default=''); ap.add_argument('--start',default=''); ap.add_argument('--end',default=''); args=ap.parse_args()
    if args.import_file:
        data=analyze(load_posts(args.import_file),args.filter,args.start,args.end)
        say(f'[ROSIE] Analyzed {data["post_count"]} imported posts','green'); save_report(data,'posts')
    elif args.username or args.keyword:
        banner(); data={'research_links':searches(args.username or '',args.keyword or '')}
        if args.username: data['profile']=public_profile(args.username)
        show_links(data['research_links']); save_report(data,'research')
    else:
        while menu(): pass
if __name__=='__main__': main()
