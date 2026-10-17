#!/usr/bin/env python3
"""RosieGlitchByte IP Specter: public IP intelligence and authorized checks."""
import argparse
import datetime
import ipaddress
import json
import pathlib
import socket
import ssl
import sys
import time
import urllib.request

PINK='\033[95m'; CYAN='\033[96m'; BLUE='\033[94m'; GREEN='\033[92m'; RED='\033[91m'; GOLD='\033[93m'; RESET='\033[0m'
OUT=pathlib.Path.home()/'RosieGlitchByte_IP_Reports'

def splash():
    art = [
        r'       .----.       /\       .----.',
        '      / .--. \\     /  \\     / .--. \\',
        r'     | | () | |---< <> >---| | () | |',
        r'      \ `--\ /     \  /     \ /--\ /',
        r'       `----\       \/       /----`',
        r'         [ ROSIEGLITCHBYTE ]',
        r'        IP SPECTER // 1.0',
    ]
    palette=[PINK,CYAN,BLUE,GOLD,GREEN]
    print('\n')
    for i,line in enumerate(art): print(palette[i%len(palette)]+line+RESET)
    print(PINK+'   HACKGIRL // PUBLIC NETWORK INTELLIGENCE'+RESET)
    print(CYAN+'   No API keys. No stealth. Just signals.\n'+RESET)
    for msg in ['[BOOT] Loading neon radar','[SCAN] Network intelligence online','[READY] Choose your module']:
        print(GREEN+msg+RESET); time.sleep(.07)

def ip_info(ip):
    a=ipaddress.ip_address(ip)
    return {'ip':str(a),'version':a.version,'is_global':a.is_global,'is_private':a.is_private,
            'is_loopback':a.is_loopback,'is_link_local':a.is_link_local,'is_multicast':a.is_multicast,
            'is_reserved':a.is_reserved,'reverse_pointer':a.reverse_pointer}

def reverse_dns(ip):
    try: return {'hostname':socket.gethostbyaddr(ip)[0]}
    except (OSError,socket.herror) as exc: return {'error':str(exc)}

def rdap(ip):
    if not ipaddress.ip_address(ip).is_global:
        return {'note':'Public RDAP lookup skipped for non-global address'}
    req=urllib.request.Request('https://rdap.org/ip/'+ip,headers={'User-Agent':'RosieGlitchByte-IP-Specter/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=8) as resp: data=json.load(resp)
        return {'name':data.get('name'),'handle':data.get('handle'),'country':data.get('country'),
                'startAddress':data.get('startAddress'),'endAddress':data.get('endAddress'),
                'entities':[{'handle':e.get('handle'),'roles':e.get('roles',[])} for e in data.get('entities',[])[:8]],
                'source':'https://rdap.org/ip/'+ip}
    except Exception as exc: return {'error':str(exc)}

def tls_check(ip,hostname):
    if not ipaddress.ip_address(ip).is_global:
        return {'error':'TLS inspection limited to public IPs'}
    ctx=ssl.create_default_context()
    try:
        with socket.create_connection((ip,443),timeout=4) as sock:
            with ctx.wrap_socket(sock,server_hostname=hostname) as s:
                cert=s.getpeercert()
                return {'tls_version':s.version(),'subject':cert.get('subject'),
                        'issuer':cert.get('issuer'),'notAfter':cert.get('notAfter'),
                        'subjectAltName':cert.get('subjectAltName',[])[:15]}
    except Exception as exc: return {'error':str(exc)}

def authorized_ports(ip,ports):
    results=[]
    for port in ports:
        try:
            with socket.create_connection((ip,port),timeout=1.5): status='open'
        except OSError: status='closed_or_filtered'
        results.append({'port':port,'status':status})
    return results

def save(ip,mode,data):
    OUT.mkdir(parents=True,exist_ok=True)
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')
    path=OUT/f'ip_specter_{ip.replace(":","-")}_{mode}_{stamp}.json'
    path.write_text(json.dumps({'tool':'RosieGlitchByte IP Specter 1.0','timestamp_utc':stamp,
                                'target':ip,'mode':mode,'results':data},indent=2,default=str),encoding='utf-8')
    print(GREEN+'\n[ARCHIVED] '+str(path)+RESET)

def run(ip,mode,hostname=None,permission=False):
    try: ip_info(ip)
    except ValueError:
        print(RED+'[ERROR] Enter a valid IPv4 or IPv6 address.'+RESET); return
    data={}
    if mode in ('1','6'): data['classification']=ip_info(ip)
    if mode in ('2','6'): data['reverse_dns']=reverse_dns(ip)
    if mode in ('3','6'): data['rdap']=rdap(ip)
    if mode=='4':
        if not hostname: print(GOLD+'[NOTICE] TLS requires a hostname for certificate verification.'+RESET); return
        data['tls']=tls_check(ip,hostname)
    if mode=='5':
        if not permission:
            print(RED+'[STOP] Port checks require explicit authorization. Use --authorized or confirm interactively.'+RESET); return
        data['connectivity']=authorized_ports(ip,[22,80,443])
    if mode not in ('1','2','3','4','5','6'):
        print(RED+'Unknown menu option.'+RESET); return
    print(CYAN+json.dumps(data,indent=2,default=str)+RESET)
    save(ip,mode,data)

def main():
    p=argparse.ArgumentParser(description='RosieGlitchByte IP Specter public IP intelligence')
    p.add_argument('ip',nargs='?',help='IPv4 or IPv6 address')
    p.add_argument('--mode',choices=list('123456'),help='1 classification, 2 reverse DNS, 3 RDAP, 4 TLS, 5 authorized ports, 6 public report')
    p.add_argument('--hostname',help='Hostname to verify against TLS certificate (mode 4)')
    p.add_argument('--authorized',action='store_true',help='Confirm you have permission to check ports')
    args=p.parse_args(); splash()
    ip=args.ip or input(PINK+'[TARGET IP] > '+RESET).strip()
    menu='''[1] IP identity & classification
[2] Reverse DNS hostname
[3] Public RDAP / network ownership
[4] TLS certificate (hostname required)
[5] Authorized connectivity (22, 80, 443)
[6] FULL PUBLIC IP REPORT
[0] Exit'''
    if args.mode: run(ip,args.mode,args.hostname,args.authorized); return
    while True:
        print('\n'+CYAN+menu+RESET)
        choice=input(PINK+'[SPECTER] Select > '+RESET).strip()
        if choice=='0': print(PINK+'[ROSIE] Signal closed. <3'+RESET); break
        hostname=None; authorized=False
        if choice=='4': hostname=input('Certificate hostname > ').strip()
        if choice=='5': authorized=input('Do you own this host or have explicit permission? (yes/no) > ').strip().lower()=='yes'
        run(ip,choice,hostname,authorized)

if __name__=='__main__': main()
