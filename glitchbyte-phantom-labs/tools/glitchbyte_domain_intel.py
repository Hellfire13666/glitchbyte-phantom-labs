#!/usr/bin/env python3
"""ROSIEGLITCHBYTE DOMAIN_INTEL: public, low-impact domain research."""
import argparse
import datetime as dt
import html.parser
import json
import re
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

C = {'pink':'\033[95m','cyan':'\033[96m','red':'\033[91m','green':'\033[92m','yellow':'\033[93m','reset':'\033[0m'}
UA = 'RosieGlitchbyte-DomainIntel/1.0 (public research; single-page fetch)'
MAX_BYTES = 600_000

class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.title=''; self.in_title=False; self.description=''
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag=='title': self.in_title=True
        if tag=='meta' and a.get('name','').lower()=='description': self.description=a.get('content','')
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
    def handle_data(self, data):
        if self.in_title: self.title+=data

def normalize(value):
    value=value.strip()
    if not value: raise ValueError('Enter a domain name.')
    if '://' in value: value=urllib.parse.urlsplit(value).hostname or ''
    value=value.strip('.').lower().encode('idna').decode('ascii')
    if len(value)>253 or not re.fullmatch(r'[a-z0-9-]+(?:\.[a-z0-9-]+)+',value):
        raise ValueError('Enter a valid public domain such as example.org')
    return value

def fetch(url, accept='text/html'):
    req=urllib.request.Request(url, headers={'User-Agent':UA,'Accept':accept})
    try:
        with urllib.request.urlopen(req, timeout=9) as r:
            final=r.geturl(); status=r.status; headers=dict(r.headers.items()); body=r.read(MAX_BYTES+1)
            return {'status':status,'final_url':final,'headers':headers,'body':body[:MAX_BYTES].decode('utf-8','replace'),'truncated':len(body)>MAX_BYTES}
    except urllib.error.HTTPError as e:
        return {'status':e.code,'final_url':e.geturl(),'headers':dict(e.headers.items()),'error':str(e)}
    except Exception as e: return {'error':str(e)}

def dns(domain):
    result={}
    try: result['ip_addresses']=sorted({x[4][0] for x in socket.getaddrinfo(domain,None)})
    except Exception as e: result['error']=str(e)
    try:
        import dns.resolver
        for typ in ['A','AAAA','MX','NS','TXT','CAA']:
            try: result[typ]=[str(r) for r in dns.resolver.resolve(domain,typ,lifetime=5)][:25]
            except Exception: result[typ]=[]
    except ImportError: result['note']='Install optional dnspython for MX, NS, TXT, CAA and detailed DNS: python3 -m pip install dnspython'
    return result

def page(domain):
    result=fetch('https://'+domain+'/')
    if 'body' in result:
        parser=Links()
        try: parser.feed(result.pop('body'))
        except Exception as e: result['parse_warning']=str(e)
        result['title']=parser.title.strip()[:300]
        result['description']=parser.description[:500]
        result['links_raw']=parser.links[:1000]
    return result

def links(domain, page_data):
    base=page_data.get('final_url','https://'+domain+'/')
    items=[]
    for raw in page_data.get('links_raw',[]):
        absolute=urllib.parse.urljoin(base,raw)
        p=urllib.parse.urlsplit(absolute)
        if p.scheme in ('http','https') and p.hostname:
            clean=urllib.parse.urlunsplit((p.scheme,p.netloc,p.path,p.query,''))
            items.append(clean)
    items=list(dict.fromkeys(items))
    return {'links':items[:150],'external_domains':sorted({urllib.parse.urlsplit(x).hostname for x in items if urllib.parse.urlsplit(x).hostname != domain})[:100], 'links_found':len(items)}

def certificate(domain):
    try:
        ctx=ssl.create_default_context()
        with socket.create_connection((domain,443),timeout=8) as sock:
            with ctx.wrap_socket(sock,server_hostname=domain) as conn:
                cert=conn.getpeercert()
                return {'tls_version':conn.version(),'subject':str(cert.get('subject')),'issuer':str(cert.get('issuer')),'valid_from':cert.get('notBefore'),'valid_until':cert.get('notAfter'),'subject_alt_names':cert.get('subjectAltName',[])[:40]}
    except Exception as e: return {'error':str(e)}

def security(domain, page_data):
    h={k.lower():v for k,v in page_data.get('headers',{}).items()}
    keys=['strict-transport-security','content-security-policy','x-frame-options','x-content-type-options','referrer-policy','permissions-policy']
    return {'certificate':certificate(domain),'security_headers':{k:h.get(k,'NOT PRESENT') for k in keys},'note':'Missing headers are observations, not proof of a vulnerability.'}

def rdap(domain):
    data=fetch('https://rdap.org/domain/'+urllib.parse.quote(domain), 'application/rdap+json')
    if 'body' not in data: return {'status':data.get('status'),'error':data.get('error','No response body')}
    try:
        obj=json.loads(data['body'])
        return {'ldhName':obj.get('ldhName'),'status':obj.get('status'),'events':obj.get('events',[])[:20], 'nameservers':[x.get('ldhName') for x in obj.get('nameservers',[])][:25], 'entities':[{'roles':x.get('roles'),'handle':x.get('handle')} for x in obj.get('entities',[])][:20], 'notice':'RDAP may redact personal registration data.'}
    except Exception as e: return {'error':str(e),'http_status':data.get('status')}

def display(title, data):
    print(C['cyan']+'\n[ '+title+' ]'+C['reset'])
    print(json.dumps(data,indent=2,ensure_ascii=False,default=str)[:14000])

def main():
    ap=argparse.ArgumentParser(description='ROSIEGLITCHBYTE public domain intelligence')
    ap.add_argument('domain',nargs='?',help='Domain to research')
    ap.add_argument('--mode',choices=['1','2','3','4','5','6'],help='1 DNS, 2 website, 3 links, 4 TLS, 5 RDAP, 6 all')
    ap.add_argument('--no-color',action='store_true')
    args=ap.parse_args()
    if args.no_color:
        for k in C: C[k]=''
    print(C['pink']+'='*58+'\n ROSIEGLITCHBYTE // DOMAIN_INTEL.EXE\n PUBLIC SIGNALS • DOMAIN RESEARCH • REPORT ARCHIVE\n'+'='*58+C['reset'])
    try: domain=normalize(args.domain or input('Domain to investigate > '))
    except (ValueError,EOFError) as e: ap.error(str(e))
    print('\n  [1] DNS & IP intelligence\n  [2] Website metadata & HTTP headers\n  [3] Public link extraction\n  [4] TLS certificate & security headers\n  [5] RDAP registration intelligence\n  [6] FULL GLITCHBYTE SCAN')
    mode=args.mode or input('\nChoose module [1-6] > ').strip()
    if mode not in '123456' or len(mode)!=1: ap.error('Choose a number 1 through 6')
    report={'tool':'ROSIEGLITCHBYTE DOMAIN_INTEL','domain':domain,'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'mode':mode,'results':{}}
    def add(key,value): report['results'][key]=value; display(key.upper(),value)
    p=None
    if mode in ('1','6'): add('dns',dns(domain))
    if mode in ('2','3','4','6'):
        p=page(domain)
        if mode in ('2','6'):
            add('website',{k:v for k,v in p.items() if k!='links_raw'})
    if mode in ('3','6'): add('links',links(domain,p))
    if mode in ('4','6'): add('security',security(domain,p))
    if mode in ('5','6'): add('rdap',rdap(domain))
    filename='glitchbyte_'+re.sub('[^a-z0-9.-]','_',domain)+'_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S')+'.json'
    Path(filename).write_text(json.dumps(report,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
    print(C['green']+'\n[REPORT SAVED] '+str(Path(filename).resolve())+C['reset'])

if __name__=='__main__': main()
