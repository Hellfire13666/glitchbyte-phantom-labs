#!/usr/bin/env python3
"""RosieGlitchbyte public username research helper. Standard library only."""
import argparse
import datetime as dt
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RESET='\033[0m'; PINK='\033[95m'; CYAN='\033[96m'; RED='\033[91m'; GREEN='\033[92m'; GOLD='\033[93m'
PLATFORMS = {
    'GitHub': ('https://github.com/{}', True),
    'GitLab': ('https://gitlab.com/{}', True),
    'Codeberg': ('https://codeberg.org/{}', True),
    'Reddit': ('https://www.reddit.com/user/{}/', True),
    'X': ('https://x.com/{}', False),
    'Instagram': ('https://www.instagram.com/{}/', False),
    'TikTok': ('https://www.tiktok.com/@{}', False),
    'Twitch': ('https://www.twitch.tv/{}', False),
}

def check(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'RosieUsernameIntel/1.0 (public profile research; standard Python urllib)', 'Accept': 'text/html'})
    try:
        with urllib.request.urlopen(request, timeout=7) as response:
            status = response.status
            final = response.geturl()
            if status == 200:
                return 'POSSIBLE PROFILE (verify manually)', status, final
            return 'UNCERTAIN', status, final
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 'NOT FOUND (HTTP 404)', 404, url
        if e.code in (401, 403, 429):
            return 'RESTRICTED / RATE LIMITED', e.code, url
        return 'UNCERTAIN', e.code, url
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return 'NETWORK ERROR', None, url

def main():
    parser=argparse.ArgumentParser(description='Public username OSINT link and status checker')
    parser.add_argument('username', nargs='?', help='Public username to research')
    parser.add_argument('--links-only', action='store_true', help='Generate links without web requests')
    args=parser.parse_args()
    username=(args.username or input('Username to research: ')).strip().lstrip('@')
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,39}', username):
        parser.error('Use 1-39 letters, numbers, underscores, periods or hyphens.')
    print(PINK + '\n' + '='*54 + '\n ROSIEGLITCHBYTE // USERNAME_INTEL.EXE\n' + '='*54 + RESET)
    print(CYAN + f'[TARGET] @{username}\n[MODE] Public profile discovery only' + RESET)
    results=[]
    for i,(site,(template,checkable)) in enumerate(PLATFORMS.items(),1):
        url=template.format(urllib.parse.quote(username, safe=''))
        print(GOLD+f'[{i:02}/{len(PLATFORMS):02}] Checking {site}...' + RESET)
        if args.links_only or not checkable:
            state,code,final='LINK ONLY (not checked)',None,url
        else:
            state,code,final=check(url)
            time.sleep(0.4)
        color=GREEN if state.startswith('POSSIBLE') else RED if state.startswith('NOT FOUND') else CYAN
        print(color+f'  {state}'+RESET+'  '+url)
        results.append({'platform':site,'url':url,'result':state,'http_status':code,'final_url':final})
    report={'username':username,'checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(), 'disclaimer':'A 200 response is not proof that the profile exists or belongs to the same person. Verify manually.', 'results':results}
    out=Path.cwd()/f'rosie_intel_{username}.json'
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(PINK+f'\n[REPORT SAVED] {out}'+RESET)
    print('Note: Same username across sites does not establish a shared identity.')

if __name__=='__main__':
    main()
