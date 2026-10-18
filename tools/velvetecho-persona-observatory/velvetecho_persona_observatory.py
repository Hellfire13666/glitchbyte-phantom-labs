#!/usr/bin/env python3
"""VELVETECHO: public username observatory and offline phone-format scanner.

No network until --live --authorized, for usernames only. Standard library.
Phone checks never call numbers or check account registrations.
"""
import argparse
import csv
from datetime import datetime, timezone
import html
from http.client import HTTPException
import ipaddress
import json
from pathlib import Path
import re
import secrets
import socket
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, quote_plus, urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.robotparser import RobotFileParser
import webbrowser

VERSION = '1.2.0'
UA = 'GlitchByte-VelvetEcho/1.0 (public profile audit; contact: local-user)'
MAX_BYTES = 160_000
SITES = [
    ('GitHub', 'development', 'https://github.com/{username}'),
    ('GitLab', 'development', 'https://gitlab.com/{username}'),
    ('Codeberg', 'development', 'https://codeberg.org/{username}'),
    ('DEV Community', 'writing', 'https://dev.to/{username}'),
    ('Reddit', 'social', 'https://www.reddit.com/user/{username}/'),
    ('Tumblr', 'social', 'https://www.tumblr.com/{username}'),
    ('Pinterest', 'creative', 'https://www.pinterest.com/{username}/'),
    ('Behance', 'creative', 'https://www.behance.net/{username}'),
    ('Twitch', 'gaming', 'https://www.twitch.tv/{username}'),
    ('Ko-fi', 'creator support', 'https://ko-fi.com/{username}'),
]

# Offline structural checks only. This limited list is a dial-code hint, not
# validation of subscriber assignment, carrier, owner, or real-world existence.
DIAL_CODES = {
    '1': 'NANP (US/Canada/etc.)', '44': 'United Kingdom', '61': 'Australia',
    '49': 'Germany', '33': 'France', '81': 'Japan', '91': 'India',
    '64': 'New Zealand', '31': 'Netherlands', '34': 'Spain',
    '39': 'Italy', '55': 'Brazil', '52': 'Mexico', '27': 'South Africa',
    '82': 'South Korea', '86': 'China', '971': 'United Arab Emirates',
}
ESC = '\x1b['
COLORS = {'HEADER': '95', 'POSSIBLE': '92', 'FORMAT_OK': '96', 'INVALID': '91',
          'UNKNOWN': '93', 'CANDIDATE': '94', 'NOT_FOUND': '90', 'ERROR': '91',
          'PHONE': '35', 'END': '0'}


def paint(message, kind='HEADER', enabled=False):
    return ESC + COLORS.get(kind, '97') + 'm' + str(message) + ESC + '0m' if enabled else str(message)


def masked_phone(digits):
    """Default private output: keep at most four last digits."""
    return '+' + ('•' * (len(digits) - 4)) + digits[-4:] if len(digits) > 4 else '+' + '•' * len(digits)


def phone_report_entry(raw, reveal=False, research=False):
    """Normalize a phone input locally. No phone lookup or identity claims."""
    value = raw.strip()
    if not value or len(value) > 64 or not re.fullmatch(r'[+\d\s().-]+', value):
        return dict(input='[REDACTED]', number='[REDACTED]', region='Unknown',
                    status='INVALID', digits=0, note='Unsupported phone characters or length',
                    research_url='')
    numbers = re.sub(r'\D', '', value)
    is_international = value.startswith('+')
    # US/Canada is the default for 10-digit local input. Other national plans
    # must be supplied with explicit +country-code prefixes.
    if not is_international and len(numbers) == 10:
        numbers = '1' + numbers
    elif not is_international and len(numbers) == 11 and numbers.startswith('1'):
        pass
    elif not is_international:
        label = masked_phone(numbers) if numbers else '[REDACTED]'
        status = 'INVALID' if len(numbers) < 8 or len(numbers) > 15 else 'UNKNOWN'
        return dict(input=label, number=label, region='Unknown', status=status,
                    digits=len(numbers), note='Too few or too many digits' if status == 'INVALID' else 'Use +countrycode for non-NANP numbers',
                    research_url='')
    matching = next((code for code in sorted(DIAL_CODES, key=len, reverse=True) if numbers.startswith(code)), None)
    region = DIAL_CODES.get(matching, 'Unlisted calling code')
    status, note = 'FORMAT_OK', 'Structure plausible, but number may be inactive, unassigned or spoofed'
    if not (8 <= len(numbers) <= 15):
        status, note = 'INVALID', 'E.164 normally requires 8-15 digits including the country code'
    elif numbers.startswith('1'):
        if len(numbers) != 11 or numbers[1] in '01' or numbers[4] in '01':
            status, note = 'INVALID', 'Invalid North American numbering-plan format'
    elif not matching:
        status, note = 'UNKNOWN', 'Calling code not recognized by the limited local catalog'
    label = '+' + numbers if reveal else masked_phone(numbers)
    # This URL is constructed offline. Never automatically open or fetch it.
    link = ('https://www.google.com/search?q=' + quote_plus('"+' + numbers + '"')) if research and status == 'FORMAT_OK' else ''
    return dict(input=label, number=label, region=region, status=status,
                digits=len(numbers), note=note, research_url=link)


def parse_phones(text, reveal=False, research=False):
    values = [item.strip() for item in re.split(r'[,\r\n]+', text) if item.strip()]
    if not (1 <= len(values) <= 25):
        raise ValueError('Provide 1-25 phone numbers, separated by commas')
    seen, rows = set(), []
    for entry in values:
        item = phone_report_entry(entry, reveal, research)
        fingerprint = re.sub(r'\D', '', entry)
        if len(fingerprint) == 10 and not entry.startswith('+'):
            fingerprint = '1' + fingerprint
        # Canonical dedup happens in memory; no full-digit artifact by default.
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        rows.append(item)
    return rows


def phone_demo():
    return [phone_report_entry('+1 202 555 0117'), phone_report_entry('+44 20 7946 0958'),
            phone_report_entry('123'), phone_report_entry('020 7946 0958')]


def print_signal(item, index, total, color=False):
    if item.get('kind') == 'phone':
        detail = '{} · {} · {}'.format(item['number'], item['region'], item['note'])
        kind = item['status']
    else:
        detail = '{} @{} · {}'.format(item['site'], item['handle'], item['note'])
        kind = item['status']
    header = '[{:02d}/{:02d}] {}'.format(index, total, kind)
    print(paint(header, kind, color) + ' ' + detail, flush=True)

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

OPENER = build_opener(NoRedirect())


def parse_handle(value):
    value = value.strip().lstrip('@')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,39}', value):
        raise ValueError('Usernames must be 1-40 characters: letters, numbers, period, hyphen, underscore')
    return value


def parse_handles(text):
    handles = list(dict.fromkeys(parse_handle(x) for x in text.split(',')))
    if len(handles) > 5:
        raise ValueError('Maximum 5 usernames per run')
    return handles


def validate_template(template):
    if template.count('{username}') != 1 or '{' in template.replace('{username}', '') or '}' in template.replace('{username}', ''):
        raise ValueError('Site URLs must contain exactly one {username} placeholder')
    parsed = urlsplit(template.replace('{username}', 'exampleuser'))
    host = parsed.hostname or ''
    if (parsed.scheme != 'https' or parsed.username or parsed.password or parsed.port or
        not re.fullmatch(r'[A-Za-z0-9.-]+', host) or '.' not in host or
        host.lower().endswith(('.local', '.internal', '.localhost', '.onion'))):
        raise ValueError('Site URL must be a public HTTPS hostname without credentials or custom port')
    try:
        ipaddress.ip_address(host)
        raise ValueError('Literal IP addresses are not allowed')
    except ValueError as err:
        if str(err) == 'Literal IP addresses are not allowed':
            raise
    return template


def catalog(path=None):
    if path is None:
        return [{'name': n, 'category': c, 'url': validate_template(u)} for n, c, u in SITES]
    obj = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(obj, dict) or not isinstance(obj.get('sites'), list):
        raise ValueError('Catalog must contain a sites array')
    if not (1 <= len(obj['sites']) <= 40):
        raise ValueError('Catalog must contain 1-40 sites')
    results, seen = [], set()
    for raw in obj['sites']:
        if not isinstance(raw, dict):
            raise ValueError('Site entries must be objects')
        name, category = raw.get('name'), raw.get('category')
        if not isinstance(name, str) or not 1 <= len(name) <= 70 or not isinstance(category, str) or not 1 <= len(category) <= 40:
            raise ValueError('Each site requires a name and category')
        template = validate_template(raw.get('url', ''))
        if name.casefold() in seen:
            raise ValueError('Duplicate site name: ' + name)
        seen.add(name.casefold())
        results.append({'name': name, 'category': category, 'url': template})
    return results


def candidates(handles, sites):
    return [dict(handle=handle, site=s['name'], category=s['category'],
                 url=s['url'].replace('{username}', quote(handle, safe='')),
                 status='CANDIDATE', code=None, note='Offline URL only; profile existence not checked')
            for handle in handles for s in sites]


def resolve_public_domain(host):
    """Reject non-public DNS targets before any HTTPS request (not an anti-rebinding guarantee)."""
    try:
        ips = [ipaddress.ip_address(result[4][0]) for result in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)]
    except (OSError, ValueError) as exc:
        raise ValueError('Hostname cannot be safely resolved: ' + str(exc)) from exc
    if not ips or not all(ip.is_global for ip in ips):
        raise ValueError('Hostname resolves to a non-public address')


def http_read(url, timeout, limit=MAX_BYTES):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname:
        raise ValueError('Only HTTPS URLs are allowed')
    resolve_public_domain(parsed.hostname)
    request = Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,text/plain;q=0.8'})
    try:
        with OPENER.open(request, timeout=timeout) as response:
            payload = response.read(limit + 1)
            if len(payload) > limit:
                raise ValueError('Response exceeds size limit')
            return response.status, response.headers.get('Content-Type', ''), payload
    except HTTPError as exc:
        # Treat redirects as unknown, never follow to unrelated / private addresses.
        return exc.code, exc.headers.get('Content-Type', ''), b''


def robots_allowed(url, timeout):
    parsed = urlsplit(url)
    robots_url = f'https://{parsed.hostname}/robots.txt'
    try:
        code, ctype, payload = http_read(robots_url, timeout, limit=90_000)
    except (URLError, OSError, ValueError, TimeoutError, HTTPException) as exc:
        return False, 'Robots check failed: ' + type(exc).__name__
    if code in (404, 410):
        return True, 'Robots file absent'
    if code != 200:
        return False, 'Robots file unavailable (HTTP ' + str(code) + ')'
    rp = RobotFileParser()
    rp.parse(payload.decode('utf-8', errors='replace').splitlines())
    if not rp.can_fetch(UA, url):
        return False, 'Disallowed by robots.txt'
    return True, 'Allowed by robots.txt'


def inspect(row, timeout=6):
    row = dict(row)
    try:
        allowed, reason = robots_allowed(row['url'], timeout)
        if not allowed:
            row.update(status='UNKNOWN', code=None, note=reason)
            return row
        code, content_type, payload = http_read(row['url'], timeout)
        row['code'] = code
        if code in (404, 410):
            row.update(status='NOT_FOUND', note='HTTP {} at profile URL'.format(code))
        elif code == 200 and 'text/html' in content_type.lower():
            snippet = payload.decode('utf-8', errors='replace').lower()
            handle = row['handle'].lower()
            mentions = bool(re.search(r'(?<![a-z0-9])' + re.escape(handle) + r'(?![a-z0-9])', snippet))
            row.update(status='POSSIBLE', note='HTML page returned; handle {}. Manual review required.'.format('mentioned' if mentions else 'not confirmed'))
        elif code in (301, 302, 303, 307, 308, 401, 403, 429):
            row.update(status='UNKNOWN', note='HTTP {}; redirects/blocked requests are inconclusive'.format(code))
        else:
            row.update(status='UNKNOWN', note='HTTP {}; no reliable profile evidence'.format(code))
    except (URLError, OSError, ValueError, TimeoutError, HTTPException) as exc:
        row.update(status='ERROR', code=None, note=type(exc).__name__ + ': ' + str(exc)[:140])
    return row


def demo_rows():
    return [
        dict(handle='rosie_demo', site='Fictional Rose Garden', category='creative', url='https://example.com/demo/rosie_demo', status='POSSIBLE', code=200, note='SYNTHETIC example only, not a real lookup'),
        dict(handle='rosie_demo', site='Fictional Night Archive', category='social', url='https://example.com/demo/night', status='NOT_FOUND', code=404, note='SYNTHETIC example only, not a real lookup'),
        dict(handle='rosie_demo', site='Fictional Velvet Station', category='development', url='https://example.com/demo/velvet', status='UNKNOWN', code=403, note='SYNTHETIC example only, not a real lookup'),
        dict(handle='rosie_demo', site='Fictional Phantom Lounge', category='creative', url='https://example.com/demo/lounge', status='CANDIDATE', code=None, note='SYNTHETIC link, no lookup'),
    ]


def render_html(report):
    rows = report['results']
    phones = report.get('phone_results', [])
    counts = {key: sum(r['status'] == key for r in rows) for key in ['CANDIDATE', 'POSSIBLE', 'NOT_FOUND', 'UNKNOWN', 'ERROR']}
    cards = ''.join(f'<div class="metric"><b>{html.escape(k)}</b><strong>{v}</strong></div>' for k,v in counts.items())
    phone_counts = {key:sum(p['status'] == key for p in phones) for key in ['FORMAT_OK', 'INVALID', 'UNKNOWN']}
    cards += ''.join(f'<div class="metric phone-metric"><b>PHONE {html.escape(k)}</b><strong>{v}</strong></div>' for k,v in phone_counts.items()) if phones else ''
    items = []
    for item in rows:
        e = lambda s: html.escape(str(s), quote=True)
        items.append('<article class="signal" data-search="{}"><div class="label"><span class="pill status-{}">{}</span><span class="site">{}</span></div><div class="meta">{} · @{}</div><a target="_blank" rel="noopener noreferrer" href="{}">{}</a><p>{}</p></article>'.format(
            e(' '.join(str(x) for x in item.values()).lower()), e(item['status']), e(item['status']), e(item['site']), e(item['category']),e(item['handle']),e(item['url']),e(item['url']),e(item['note'])))
    phone_cards = []
    for item in phones:
        esc = lambda s: html.escape(str(s), quote=True)
        link = ('<a target="_blank" rel="noopener noreferrer" href="{}">Manual public search</a>'.format(esc(item['research_url'])) if item.get('research_url') else '')
        phone_cards.append('<article class="signal phone-signal" data-search="{}"><div class="label"><span class="pill status-{}">{}</span><span class="site">{}</span></div><div class="meta">{} digits · {}</div><p>{}</p>{}</article>'.format(
            esc(' '.join(str(x) for x in item.values()).lower()), esc(item['status']), esc(item['status']),
            esc(item['number']), esc(item['digits']), esc(item['region']), esc(item['note']), link))
    title='VELVETECHO // PERSONA OBSERVATORY' 
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>VELVETECHO | GlitchByte Phantom Labs</title>
<style>
:root{color-scheme:dark;--night:#100c17;--pink:#ff4b87;--mint:#8fffe0;--gold:#ffd1a4;--muted:#b9adc6}*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 90% 10%,#532543 0%,transparent 45%),radial-gradient(ellipse at 10% 0%,#234d4f 0%,transparent 34%),var(--night);font:15px/1.55 system-ui,sans-serif;color:#fff6ff}main{max-width:1130px;margin:auto;padding:38px 23px 90px}.topline{letter-spacing:.27em;color:var(--mint);font-size:.73rem;font-weight:800}.hero{padding:35px;border:1px solid #9d5689;border-radius:22px;background:linear-gradient(115deg,#24162aef,#170d1ed9);position:relative;overflow:hidden}.hero:after{content:'✧';position:absolute;right:3%;top:-100px;font-size:380px;color:#fb4b841c;pointer-events:none}h1{font-size:clamp(2rem,7vw,5.3rem);letter-spacing:-.06em;line-height:.98;margin:20px 0;background:linear-gradient(95deg,var(--pink),#eab6fc,var(--mint));color:transparent;background-clip:text}h2{font-size:1.35rem;letter-spacing:.13em}p{color:var(--muted)}.warning{border-left:3px solid var(--gold);padding-left:12px;color:#efdcca;max-width:750px}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(135px,1fr));gap:12px;margin:25px 0}.metric{background:#211628;border:1px solid #51304d;padding:15px;border-radius:12px}.metric b{display:block;letter-spacing:.1em;color:#d7b8ce;font-size:.7rem}.metric strong{font-size:2rem;color:var(--mint)}input{width:100%;padding:16px;background:#17141d;color:white;border:1px solid #815477;border-radius:10px;font-size:1rem}.results{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:15px;margin-top:20px}.signal{padding:18px;background:#1e1725;border:1px solid #58374d;border-radius:15px;min-width:0;box-shadow:0 9px 38px #0003}.label{display:flex;align-items:center;gap:12px;justify-content:space-between}.pill{font-size:.66rem;letter-spacing:.08em;color:#150b19;font-weight:900;background:var(--mint);padding:4px 9px;border-radius:20px}.pill.status-INVALID{background:#ff647e}.pill.status-UNKNOWN{background:#ffd477}.pill.status-FORMAT_OK{background:#7bf1fb}.pill.status-NOT_FOUND{background:#b8a4d1}.pill.status-POSSIBLE{background:#bcff88}.pill.status-ERROR{background:#ff647e}.pill.status-CANDIDATE{background:#95caff}.phone-metric{border-color:#4c9c9a}.phone-signal{border-color:#327e8c;background:linear-gradient(150deg,#122832,#23172c)}.site{font-size:1.05rem;font-weight:750}.meta{font-size:.79rem;color:var(--gold);margin:14px 0 3px}.signal a{display:block;color:#8fffe0;overflow-wrap:anywhere;font-size:.87rem}.signal p{font-size:.85rem;margin-bottom:0}footer{color:#b9adc6;margin-top:32px;font-size:.83rem}footer strong{color:var(--pink)}
</style></head><body><main><section class="hero"><div class="topline">🌹 GLITCHBYTE PHANTOM LABS / VELVET SIGNAL DIVISION</div><h1>VELVETECHO<span style="color:#8fffe0">.EXE</span></h1><h2>PERSONA + PHONE SIGNAL OBSERVATORY</h2><p>PUBLIC PROFILE LINKS · LOCAL NUMBER FORMAT CHECKS · HONEST CONFIDENCE LABELS</p><div class="warning">Username matches never establish identity, relationships, or affiliation with any service. HTTP 200 means POSSIBLE only. Phone formats never prove a live line or its owner. Reports may contain personal identifiers; keep them private.</div></section><div class="stats">''' + cards + '''</div><p>MODE: <strong>''' + html.escape(report['mode']) + '''</strong> · GENERATED UTC: ''' + html.escape(report['created_at']) + '''</p><label for="filter">FILTER RECORDS</label><input id="filter" type="search" placeholder="Search usernames, phone summaries, sites, outcomes" oninput="document.querySelectorAll('.signal').forEach(x=>x.hidden=!x.dataset.search.includes(this.value.toLowerCase()))"><section class="results">''' + ''.join(items) + '''</section><h2>☎ PHONE SIGNAL READOUT</h2><p>Local-only structural checks. No SMS, call, account enumeration, or data-provider requests.</p><section class="results">''' + ''.join(phone_cards) + '''</section><footer><strong>GLITCHBYTE PHANTOM LABS</strong> · Original source files were not modified. Live checks respect robots.txt; offline candidates are not scanned. All reports are local. <br>✧ VELVETECHO © 2026</footer></main></body></html>'''


def write_reports(rows, out, mode, phone_rows=None):
    directory = Path(out).expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    nonce = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ') + '_' + secrets.token_hex(3)
    base = directory / ('velvetecho_signals_' + nonce)
    report = {'app': 'VELVETECHO', 'version': VERSION, 'created_at': datetime.now(timezone.utc).isoformat(), 'mode': mode, 'results': rows, 'phone_results': phone_rows or [],
              'limits': 'Public profile URL existence is not identity proof; live checks avoid robots-disallowed sites and redirects.'}
    json_path, csv_path, html_path = base.with_suffix('.json'), base.with_suffix('.csv'), base.with_suffix('.html')
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    with csv_path.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=['handle', 'site', 'category', 'url', 'status', 'code', 'note'])
        writer.writeheader(); writer.writerows(rows)
    if phone_rows:
        phone_csv_path = base.with_name(base.name + '_phones').with_suffix('.csv')
        with phone_csv_path.open('w', encoding='utf-8', newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=['input', 'number', 'region', 'status', 'digits', 'note', 'research_url'])
            writer.writeheader(); writer.writerows(phone_rows)
    html_path.write_text(render_html(report), encoding='utf-8')
    return json_path, csv_path, html_path


def main(argv=None):
    parser = argparse.ArgumentParser(description='VELVETECHO: privacy-aware public username observatory; offline by default')
    parser.add_argument('-u', '--usernames', help='Up to 5 public usernames, comma-separated')
    parser.add_argument('-p', '--phones', help='Up to 25 phone inputs for LOCAL format checks (comma-separated)')
    parser.add_argument('--phones-file', type=Path, help='Read your own/authorized numbers from a local UTF-8 text file (one per line)')
    parser.add_argument('--reveal-phone', action='store_true', help='Explicitly save full phone digits in reports (default masks digits)')
    parser.add_argument('--phone-research-links', action='store_true', help='Include optional manual web searches; requires --authorized; no automatic fetch')
    parser.add_argument('--color', choices=['auto','always','never'], default='auto', help='ANSI colored terminal readout')
    parser.add_argument('--catalog', type=Path, help='Custom public HTTPS site catalog JSON, replacing built-in sites')
    parser.add_argument('--list-sites', action='store_true', help='Print supported public profile URL patterns')
    parser.add_argument('--demo', action='store_true', help='Use four synthetic offline example results')
    parser.add_argument('--live', action='store_true', help='Opt into limited real HTTP checks')
    parser.add_argument('--authorized', action='store_true', help='Confirm you own or have permission to assess supplied identities')
    parser.add_argument('--max-sites', type=int, default=12, help='Max sites per username (1-20)')
    parser.add_argument('--timeout', type=int, default=6, help='Request timeout seconds (2-15)')
    parser.add_argument('--delay', type=float, default=1.0, help='Seconds between live checks (minimum 1)')
    parser.add_argument('--out', default='~/VelvetEchoReports', help='Local reports folder')
    parser.add_argument('--open-browser', action='store_true', help='Open saved report in local browser')
    args = parser.parse_args(argv)
    if args.max_sites not in range(1, 21) or args.timeout not in range(2,16) or args.delay < 1 or args.delay > 60:
        parser.error('Require max-sites 1-20, timeout 2-15 and delay 1-60')
    if args.phones and args.phones_file:
        parser.error('Choose either --phones or --phones-file, not both')
    if args.live and not args.usernames:
        parser.error('--live requires --usernames; phones are always inspected offline')
    if args.live and not args.authorized:
        parser.error('Live checks require --authorized; use offline mode otherwise')
    if args.phone_research_links and not args.authorized:
        parser.error('--phone-research-links requires --authorized and appropriate permission')
    if args.demo and (args.usernames or args.phones or args.phones_file or args.live):
        parser.error('--demo cannot be combined with usernames or live checks')
    try:
        sites = catalog(args.catalog)
        if args.list_sites:
            for site in sites: print('{}\t{}\t{}'.format(site['category'], site['name'], site['url']))
            return 0
        color = args.color == 'always' or (args.color == 'auto' and sys.stdout.isatty())
        print(paint('╔════════════════════════════════════════════════════════╗', 'HEADER', color))
        print(paint('║ VELVETECHO :: GLITCHBYTE PHANTOM LABS :: SIGNAL CORE    ║', 'HEADER', color))
        print(paint('╚════════════════════════════════════════════════════════╝', 'HEADER', color))
        phone_rows = []
        if args.demo:
            rows, phone_rows, mode = demo_rows(), phone_demo(), 'SYNTHETIC DEMO (NO NETWORK)'
        elif args.usernames or args.phones or args.phones_file:
            rows = candidates(parse_handles(args.usernames), sites[:args.max_sites]) if args.usernames else []
            phone_input = args.phones
            if args.phones_file:
                phone_path = args.phones_file.expanduser()
                if phone_path.stat().st_size > 4096:
                    raise ValueError('Phone input file exceeds 4096 bytes')
                phone_input = phone_path.read_text(encoding='utf-8')
            if phone_input:
                phone_rows = parse_phones(phone_input, reveal=args.reveal_phone, research=args.phone_research_links)
            mode = 'LIVE AUTHORIZED USERNAME CHECK + OFFLINE PHONE FORMATS' if args.live else 'OFFLINE USERNAME + PHONE FORMAT CHECKS'
            if args.live:
                checked = []
                for i, row in enumerate(rows, 1):
                    item = inspect(row, timeout=args.timeout)
                    checked.append(item)
                    print_signal(item, i, len(rows), color)
                    if i != len(rows): time.sleep(args.delay)
                rows = checked
        else:
            parser.error('Specify --demo, --usernames, --phones, --phones-file or --list-sites')
        for idx,item in enumerate(rows, 1):
            if not args.live: print_signal(item, idx, len(rows), color)
        for idx,item in enumerate(phone_rows, 1):
            print_signal({**item, 'kind':'phone'}, idx, len(phone_rows), color)
        paths = write_reports(rows, args.out, mode, phone_rows)
        summary = {key:sum(x['status']==key for x in rows) for key in ['CANDIDATE','POSSIBLE','NOT_FOUND','UNKNOWN','ERROR']}
        numbers = {key:sum(x['status']==key for x in phone_rows) for key in ['FORMAT_OK','INVALID','UNKNOWN']}
        print(paint('✧ OUTCOME: {} username signals; {} unique phone formats'.format(len(rows),len(phone_rows)), 'HEADER', color))
        print(paint('  USERNAME SIGNAL OUTCOME', 'HEADER', color))
        print('  ' + '  '.join(paint(f'{k}: {v}', k, color) for k,v in summary.items()))
        if phone_rows:
            print(paint('  PHONE SCANNER OUTCOME', 'PHONE', color))
            print('  ' + '  '.join(paint(f'{k}: {v}', k, color) for k,v in numbers.items()))
            print(paint('  Format checks only: no carrier/owner/activity verification', 'UNKNOWN', color))
        for path in paths: print('[REPORT] ' + str(path.resolve()))
        if args.open_browser:
            webbrowser.open(paths[2].resolve().as_uri())
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print('[ERROR] ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
