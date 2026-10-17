#!/usr/bin/env python3
"""RosieGlitchByte Domain Phantom: public, single-site domain research."""
import argparse
import datetime as dt
import html.parser
import ipaddress
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PINK='\033[95m'; CYAN='\033[96m'; BLUE='\033[94m'; RED='\033[91m'; GREEN='\033[92m'; GOLD='\033[93m'; RESET='\033[0m'; BOLD='\033[1m'
OUT=Path.home()/'RosieGlitchByte_Domain_Intel'
AGENT='RosieGlitchByte-DomainPhantom/2.0 (public-domain-research)'
TIMEOUT=8

class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.title=''; self.in_title=False; self.links=[]; self.description=''; self.headings=[]; self.in_heading=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='title': self.in_title=True
        if tag in ('h1','h2'): self.in_heading=True
        if tag=='a' and attrs.get('href'): self.links.append(attrs['href'])
        if tag=='meta' and attrs.get('name','').lower()=='description': self.description=attrs.get('content','')
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
        if tag in ('h1','h2'): self.in_heading=False
    def handle_data(self,data):
        if self.in_title: self.title+=data
        if self.in_heading and data.strip(): self.headings.append(data.strip())

def say(msg,color=CYAN): print(color+msg+RESET)
def intro(animate=True):
    art=r'''
        .-~~~~~~~~~-._       .-~~~~~~~~~-.
       /   ROSIE       \_____/  GLITCHBYTE \
      |   /\_ /\      [  o  o ]     /\_/\  |
      |  (  >.<  )     \  --  /    ( >.< )  |
       \  /|___|\       |====|      /|___|\ /
        '-----------  [ HACKGIRL ]  --------'
       << DOMAIN PHANTOM // NEON INTEL >>
'''
    print(PINK+BOLD+art+RESET)
    for msg,color in [('[BOOT] RosieGlitchByte signal online...',CYAN),('[SYSTEM] Public domain intelligence modules ready.',GREEN),('[NOTICE] Respect robots.txt, access rules, and privacy.',GOLD)]:
        say(msg,color)
        if animate: time.sleep(.12)

def host_from(raw):
    raw=raw.strip()
    if not raw: raise ValueError('Enter a domain.')
    if '://' not in raw: raw='https://'+raw
    p=urllib.parse.urlsplit(raw)
    if p.username or p.password or p.port not in (None,80,443): raise ValueError('Only ordinary public domains are supported.')
    host=(p.hostname or '').lower().rstrip('.')
    if not host or len(host)>253 or not re.fullmatch(r'[a-z0-9.-]+',host) or '.' not in host or '..' in host: raise ValueError('Enter a valid domain, e.g. example.org')
    return host

def public_ips(host):
    ips=sorted({item[4][0] for item in socket.getaddrinfo(host,None,type=socket.SOCK_STREAM)})
    if not ips or any(not ipaddress.ip_address(ip).is_global for ip in ips): raise ValueError('Target resolves to a non-public address. Scan refused.')
    return ips

def request_public(url,host,max_bytes=450000):
    # No redirects: prevents a public site redirecting requests into internal networks.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl): return None
    opener=urllib.request.build_opener(NoRedirect)
    req=urllib.request.Request(url,headers={'User-Agent':AGENT,'Accept':'text/html,text/plain;q=0.9,*/*;q=0.5'})
    try:
        with opener.open(req,timeout=TIMEOUT) as response:
            body=response.read(max_bytes+1)
            return {'status':response.status,'url':response.url,'headers':dict(response.headers.items()),'body':body[:max_bytes].decode('utf-8','replace'),'truncated':len(body)>max_bytes}
    except urllib.error.HTTPError as exc:
        return {'status':exc.code,'url':url,'headers':dict(exc.headers.items()),'body':'','truncated':False,'note':'HTTP error or redirect; redirect not followed'}

def dns(host):
    try: return {'hostname':host,'ip_addresses':public_ips(host)}
    except Exception as exc: return {'error':str(exc)}

def website(host):
    public_ips(host)
    result=request_public('https://'+host+'/',host)
    parser=PageParser()
    if result['body']:
        parser.feed(result['body'])
    headers={k.lower():v for k,v in result['headers'].items()}
    return {'status':result['status'],'url':result['url'],'title':parser.title.strip()[:250], 'description':parser.description[:400], 'headings':parser.headings[:15], 'server':headers.get('server'), 'content_type':headers.get('content-type'), 'location':headers.get('location'), 'truncated':result['truncated']}

def links(host):
    public_ips(host)
    result=request_public('https://'+host+'/',host)
    parser=PageParser(); parser.feed(result['body'])
    urls=[]
    for link in parser.links:
        absolute=urllib.parse.urljoin('https://'+host+'/',link)
        parsed=urllib.parse.urlsplit(absolute)
        if parsed.scheme in ('http','https') and parsed.hostname:
            clean=urllib.parse.urlunsplit((parsed.scheme,parsed.netloc,parsed.path,'',''))
            if clean not in urls: urls.append(clean)
    return {'total_found':len(urls),'links':urls[:100], 'external_domains':sorted({urllib.parse.urlsplit(u).hostname for u in urls if urllib.parse.urlsplit(u).hostname!=host})[:100], 'limited_to':100}

def security(host):
    public_ips(host)
    result=request_public('https://'+host+'/',host)
    h={k.lower():v for k,v in result['headers'].items()}
    names=['strict-transport-security','content-security-policy','x-content-type-options','referrer-policy','permissions-policy','x-frame-options']
    return {'http_status':result['status'],'security_headers':{n:h.get(n,'Not observed') for n in names},'note':'Missing headers do not alone establish a vulnerability.'}

def tls(host):
    public_ips(host)
    ctx=ssl.create_default_context()
    with socket.create_connection((host,443),timeout=TIMEOUT) as sock:
        with ctx.wrap_socket(sock,server_hostname=host) as conn:
            cert=conn.getpeercert()
            return {'tls_version':conn.version(),'cipher':conn.cipher()[0],'subject':str(cert.get('subject')),'issuer':str(cert.get('issuer')),'not_before':cert.get('notBefore'),'not_after':cert.get('notAfter'),'subject_alt_names':[v for k,v in cert.get('subjectAltName',[]) if k=='DNS'][:30]}

def robots(host):
    public_ips(host)
    result=request_public('https://'+host+'/robots.txt',host,max_bytes=25000)
    return {'status':result['status'],'preview':result['body'][:8000], 'note':'For information only; this tool does not crawl blocked paths.'}

def rdap(host):
    # IANA RDAP bootstrap via rdap.org redirect is intentionally not followed;
    # provide a browser-accessible research link instead of claiming parsed records.
    return {'public_rdap_lookup':'https://rdap.org/domain/'+urllib.parse.quote(host), 'note':'Open the link to review registration records; availability varies.'}

MODES={'1':('DNS / IP lookup',dns),'2':('Website metadata',website),'3':('Public page links',links),'4':('Security headers',security),'5':('TLS certificate',tls),'6':('robots.txt',robots),'7':('RDAP research link',rdap)}

def run(host,choice):
    report={'brand':'RosieGlitchByte // Domain Phantom 2.0','domain':host,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'modules':{}}
    selections=list(MODES) if choice=='8' else [choice]
    for key in selections:
        name,fn=MODES[key]
        say(f'\n[{key}] {name}...',PINK)
        try: data=fn(host)
        except Exception as exc: data={'error':str(exc)}
        report['modules'][name]=data
        print(json.dumps(data,indent=2,ensure_ascii=False)[:13000])
    OUT.mkdir(parents=True,exist_ok=True)
    stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    dest=OUT/f'{host.replace(".","_")}_{stamp}.json'
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    say('\n[ARCHIVED] '+str(dest),GREEN)

def main():
    ap=argparse.ArgumentParser(description='RosieGlitchByte themed public domain research (no API key)')
    ap.add_argument('domain',nargs='?',help='Domain to research, e.g. example.org')
    ap.add_argument('--mode',choices=[*MODES,'8'],default=None,help='1-7 single module, 8 all')
    ap.add_argument('--no-animation',action='store_true')
    args=ap.parse_args(); intro(not args.no_animation)
    host=args.domain
    while True:
        if not host:
            host=input(PINK+'\n[ROSIE] Enter a public domain (or q to quit): '+RESET).strip()
        if host.lower() in ('q','quit','exit'): break
        try: host=host_from(host)
        except ValueError as exc: say('[ERROR] '+str(exc),RED); host=None; continue
        say('\n'+'='*54,PINK)
        for key,(name,_) in MODES.items(): say(f'  [{key}] {name}',CYAN if int(key)%2 else PINK)
        say('  [8] FULL GLITCHBYTE DOMAIN REPORT',GREEN)
        say('  [9] Change domain    [0] Exit',GOLD)
        choice=args.mode or input(PINK+'\n[HACKGIRL] Select module: '+RESET).strip()
        if choice=='0': break
        if choice=='9': host=None; continue
        if choice not in (*MODES,'8'): say('[ERROR] Choose 0-9.',RED); continue
        run(host,choice)
        if args.mode: break
        host=None
    say('[ROSIE] Signal closed. Stay curious. <3',PINK)

if __name__=='__main__':
    try: main()
    except (KeyboardInterrupt,EOFError): print('\n[ROSIE] Session ended.')
