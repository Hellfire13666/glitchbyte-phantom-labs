#!/usr/bin/env python3
"""RosieGlitchByte IP Shadow Scraper: public IP research, no API key."""
import argparse, datetime, ipaddress, json, os, pathlib, re, socket, ssl, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

PINK='\033[95m'; CYAN='\033[96m'; BLUE='\033[94m'; GREEN='\033[92m'; RED='\033[91m'; GOLD='\033[93m'; RESET='\033[0m'
OUT=pathlib.Path.home()/'RosieGlitchByte_IP_Shadow_Reports'
ART=pathlib.Path(__file__).with_name('rosie_ip_shadow_art.png')
TIMEOUT=5

def line(s='', color=CYAN): print(color+str(s)+RESET)
def banner():
    print('\033[2J\033[H',end='')
    for c,s in [(PINK,'   /\\_/\\   .----.    ROSIEGLITCHBYTE'),(CYAN,'  ( o.o ) / /\\ \\   IP SHADOW SCRAPER 2.0'),(PINK,'   > ^ <  | |  | |  HACKGIRL NETWORK INTEL'),(BLUE,'  ~~~~~~~ \\_\\/_/   NEON SIGNALS // PUBLIC DATA')]: line(s,c)
    line('  '+ '='*58,PINK)
    line('  No API keys | No login cookies | Public IP intelligence',GREEN)
    print()

def parse_ip(raw):
    try: return ipaddress.ip_address(raw.strip())
    except ValueError: raise ValueError('Enter one valid IPv4 or IPv6 address (not a hostname).')

def get_json(url):
    req=urllib.request.Request(url,headers={'User-Agent':'RosieGlitchByte-IP-Research/2.0 (public RDAP lookup)','Accept':'application/rdap+json, application/json'})
    with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
        return json.load(r)

def identity(ip):
    return {'ip':str(ip),'version':ip.version,'global':ip.is_global,'private':ip.is_private,'loopback':ip.is_loopback,'link_local':ip.is_link_local,'multicast':ip.is_multicast,'reserved':ip.is_reserved,'compressed':ip.compressed,'reverse_pointer':ip.reverse_pointer}

def reverse_dns(ip):
    try: return {'hostname':socket.gethostbyaddr(str(ip))[0]}
    except (OSError,socket.herror) as e: return {'hostname':None,'note':str(e)}

def rdap(ip):
    if not ip.is_global: return {'note':'Public RDAP skipped for non-global IP.'}
    try:
        data=get_json('https://rdap.org/ip/'+urllib.parse.quote(str(ip),safe=':'))
        events=[{'action':x.get('eventAction'),'date':x.get('eventDate')} for x in data.get('events',[])][:12]
        entities=[{'handle':x.get('handle'),'roles':x.get('roles',[])} for x in data.get('entities',[])][:15]
        return {'name':data.get('name'),'handle':data.get('handle'),'country':data.get('country'),'type':data.get('type'),'startAddress':data.get('startAddress'),'endAddress':data.get('endAddress'),'parentHandle':data.get('parentHandle'),'events':events,'entities':entities,'source':data.get('links',[{}])[0].get('href'),'note':'RDAP country is registration data, not precise device geolocation.'}
    except Exception as e: return {'error':str(e)}

def tls(ip,port=443):
    try:
        ctx=ssl.create_default_context()
        # TLS certificate retrieval without claiming a verified hostname match.
        ctx.check_hostname=True
        ctx.verify_mode=ssl.CERT_REQUIRED
        with socket.create_connection((str(ip),port),timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock) as wrapped:
                der=wrapped.getpeercert(binary_form=True)
                return {'tls_version':wrapped.version(),'cipher':wrapped.cipher()[0] if wrapped.cipher() else None,'certificate_sha256':__import__('hashlib').sha256(der).hexdigest() if der else None,'note':'Certificate fingerprint only; no hostname verification performed.'}
    except Exception as e: return {'error':str(e)}

def http_head(ip,scheme='https'):
    # HEAD only, no redirects, no cookie collection. Explicit opt-in for authorized systems.
    import http.client
    cls=http.client.HTTPSConnection if scheme=='https' else http.client.HTTPConnection
    try:
        kw={'timeout':TIMEOUT}
        if scheme=='https': kw['context']=ssl.create_default_context()
        conn=cls(str(ip),443 if scheme=='https' else 80,**kw)
        try:
            conn.request('HEAD','/',headers={'User-Agent':'RosieGlitchByte-IP-Research/2.0'})
            r=conn.getresponse()
            safe={k:v for k,v in r.getheaders() if k.lower() not in ('set-cookie','cookie','authorization','proxy-authorization')}
            return {'status':r.status,'reason':r.reason,'headers':safe,'note':'IP-only request; virtual-host websites may respond differently.'}
        finally: conn.close()
    except Exception as e: return {'error':str(e)}

def reputation_links(ip):
    q=urllib.parse.quote(str(ip),safe='')
    return {'VirusTotal':'https://www.virustotal.com/gui/ip-address/'+q,'AbuseIPDB':'https://www.abuseipdb.com/check/'+q,'ARIN RDAP':'https://search.arin.net/rdap/?query='+q,'RIPEstat':'https://stat.ripe.net/'+q,'note':'Research links only; no reputation verdict inferred.'}

def local_network(ip):
    return {'reverse_pointer':ip.reverse_pointer,'network_examples': [str(ipaddress.ip_network(str(ip)+('/24' if ip.version==4 else '/64'),strict=False))], 'note':'Network prefix shown for context only; not a scan of neighboring hosts.'}

def save(ip, data):
    OUT.mkdir(parents=True,exist_ok=True)
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')
    name=f"rosie_ip_{str(ip).replace(':','_')}_{stamp}.json"
    path=OUT/name
    path.write_text(json.dumps({'brand':'RosieGlitchByte IP Shadow Scraper','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':data},indent=2,ensure_ascii=False),encoding='utf-8')
    line('Saved report: '+str(path),GREEN)

def show(title,data):
    line('\n[ '+title+' ]',PINK)
    print(json.dumps(data,indent=2,ensure_ascii=False))

def ask_authorized():
    return input('Only for systems you own or are authorized to test. Confirm (yes/no): ').strip().lower()=='yes'

def run(mode,ip,results):
    if mode=='1': data=identity(ip); title='IP identity and flags'
    elif mode=='2': data=reverse_dns(ip); title='Reverse DNS'
    elif mode=='3': data=rdap(ip); title='RDAP registration / network ownership'
    elif mode=='4': data=local_network(ip); title='Network prefix context'
    elif mode=='5': data=tls(ip); title='TLS certificate fingerprint'
    elif mode=='6':
        if not ask_authorized(): line('Skipped: authorization not confirmed.',GOLD); return
        data=http_head(ip); title='HTTPS HEAD response'
    elif mode=='7':
        if not ask_authorized(): line('Skipped: authorization not confirmed.',GOLD); return
        data=http_head(ip,'http'); title='HTTP HEAD response'
    elif mode=='8': data=reputation_links(ip); title='Public reputation research links'
    elif mode=='9':
        data={'identity':identity(ip),'reverse_dns':reverse_dns(ip),'rdap':rdap(ip),'network_context':local_network(ip),'tls':tls(ip),'reputation_links':reputation_links(ip)}
        title='Full passive IP intelligence report'
    else: line('Unknown option.',RED); return
    results[title]=data
    show(title,data)
    save(ip,results)

def menu():
    line(' [1] IP classification + IPv4/IPv6 flags',GREEN)
    line(' [2] Reverse DNS / PTR hostname',CYAN)
    line(' [3] Public RDAP ownership + allocation',PINK)
    line(' [4] Network prefix context',BLUE)
    line(' [5] TLS handshake + certificate fingerprint',GOLD)
    line(' [6] HTTPS headers (authorized hosts)',GREEN)
    line(' [7] HTTP headers (authorized hosts)',CYAN)
    line(' [8] Reputation research links',PINK)
    line(' [9] FULL PASSIVE GLITCHBYTE REPORT',GREEN)
    line(' [A] Open Rosie HackGirl artwork',PINK)
    line(' [C] Change IP address',CYAN)
    line(' [0] Exit',RED)

def open_art():
    if not ART.exists(): line('Optional artwork not found next to script.',GOLD); return
    try: subprocess.Popen(['xdg-open',str(ART)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); line('Opening Rosie artwork...',GREEN)
    except OSError: line('Open image manually: '+str(ART),GOLD)

def main():
    parser=argparse.ArgumentParser(description='RosieGlitchByte public IP research tool; no API key')
    parser.add_argument('ip',nargs='?',help='IPv4 or IPv6 address')
    parser.add_argument('--mode',choices=[str(x) for x in range(1,10)])
    parser.add_argument('--art',action='store_true',help='Open companion Rosie artwork')
    args=parser.parse_args()
    banner()
    if args.art: open_art()
    raw=args.ip or input('Enter IP address to research: ').strip()
    try: ip=parse_ip(raw)
    except ValueError as e: line(str(e),RED); return 2
    results={}
    if args.mode: run(args.mode,ip,results); return 0
    while True:
        line('\nTARGET: '+str(ip),GOLD); menu()
        choice=input(PINK+'ROSIE@IP-SPECTER > '+RESET).strip().upper()
        if choice=='0': line('Signal closed. Stay glitchy. <3',PINK); break
        if choice=='A': open_art(); continue
        if choice=='C':
            try: ip=parse_ip(input('New IP: ')); results={}
            except ValueError as e: line(str(e),RED)
            continue
        run(choice,ip,results)
    return 0

if __name__=='__main__': sys.exit(main())
