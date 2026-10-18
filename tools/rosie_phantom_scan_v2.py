#!/usr/bin/env python3
"""ROSIE PHANTOM SCAN V2: bounded public domain intel, not a vulnerability scanner."""
import argparse
import base64
from datetime import datetime, timezone
import html
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import shutil
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

APP = "ROSIE PHANTOM SCAN V2"
UA = "RosiePhantomScan/2.0 (bounded public-domain research)"
RECORD_TYPES = ("A", "AAAA", "MX", "NS", "SOA", "CAA", "TXT")
HEADERS = ("strict-transport-security", "content-security-policy",
           "x-frame-options", "x-content-type-options", "referrer-policy",
           "permissions-policy", "cross-origin-opener-policy")


class PageMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.description, self.canonical, self.links = [], "", "", []
        self.in_title = False
        self.social = {}

    def handle_starttag(self, tag, attrs):
        attrs = {k.lower(): v for k, v in attrs if k and isinstance(v, str)}
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            if attrs.get("name", "").lower() == "description":
                self.description = attrs.get("content", "")[:400]
            if attrs.get("property", "").lower().startswith("og:"):
                self.social[attrs["property"][:50]] = attrs.get("content", "")[:250]
        if tag == "link" and "canonical" in attrs.get("rel", ""):
            self.canonical = attrs.get("href", "")[:300]
        if tag == "a" and len(self.links) < 30:
            target = attrs.get("href", "")
            if target.startswith("/") and not target.startswith("//"):
                path = urllib.parse.urlsplit(target).path[:160]
                if path and path not in self.links:
                    self.links.append(path)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and sum(map(len, self.title)) < 250:
            self.title.append(data)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, url):
        return None


def valid_domain(domain):
    if not isinstance(domain, str) or len(domain) > 253 or "." not in domain:
        return False
    try:
        ipaddress.ip_address(domain)
        return False
    except ValueError:
        pass
    return all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", part)
               for part in domain.split("."))


def public_ip(value):
    try:
        return ipaddress.ip_address(value).is_global
    except ValueError:
        return False


def fetch(url, *, timeout=8, limit=180000, redirect=False):
    opener = urllib.request.build_opener() if redirect else urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=timeout) as response:
        blob = response.read(limit + 1)
        if len(blob) > limit:
            raise ValueError("HTTP response exceeded bounded size")
        return response.status, dict(response.headers), blob, response.geturl()


def dns_record(domain, record_type, notes):
    url = "https://dns.google/resolve?" + urllib.parse.urlencode(
        {"name": domain, "type": record_type})
    try:
        data = json.loads(fetch(url, limit=80000)[2])
        records = list(dict.fromkeys(str(item.get("data", ""))[:500]
                                    for item in data.get("Answer", [])[:30]))
        return {"records": [v for v in records if v], "status": data.get("Status")}
    except (OSError, ValueError, TypeError) as exc:
        notes.append(f"DNS {record_type}: {exc!s}"[:160])
        return {"records": [], "status": "unavailable"}


def rdap(domain, notes):
    # Redirects are required by the RDAP bootstrap service. No redirects to the target site.
    try:
        url = "https://rdap.org/domain/" + urllib.parse.quote(domain)
        response = json.loads(fetch(url, timeout=10, limit=350000, redirect=True)[2])
        return {
            "handle": response.get("handle"),
            "status": response.get("status", []),
            "events": [{"action": e.get("eventAction"), "date": e.get("eventDate")}
                       for e in response.get("events", [])[:20]],
            "nameservers": [x.get("ldhName") for x in response.get("nameservers", [])[:30]],
            "entities": [{"roles": x.get("roles"), "handle": x.get("handle")}
                         for x in response.get("entities", [])[:15]],
            "notice": "RDAP/WHOIS entries may be stale or privacy-redacted.",
        }
    except (OSError, ValueError, TypeError) as exc:
        notes.append(f"RDAP/WHOIS: {exc!s}"[:160])
        return {"error": "Registration data unavailable"}


def normalize_subdomain(item, domain):
    value = str(item).strip().lower().removeprefix("*.")
    return value if valid_domain(value) and value != domain and value.endswith("." + domain) else None


def certificate_names(domain, notes):
    url = "https://crt.sh/?" + urllib.parse.urlencode({"q": "%." + domain, "output": "json"})
    try:
        data = json.loads(fetch(url, timeout=12, limit=800000)[2])
        results = set()
        for row in data[:3000]:
            for name in str(row.get("name_value", "")).splitlines():
                normalized = normalize_subdomain(name, domain)
                if normalized:
                    results.add(normalized)
        return sorted(results)[:150]
    except (OSError, ValueError, TypeError) as exc:
        notes.append(f"crt.sh passive certificates: {exc!s}"[:160])
        return []


def local_command(argv, seconds=15, limit=18000):
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=seconds)
        return {"exit_code": result.returncode,
                "output": (result.stdout or result.stderr)[:limit]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"error": str(exc)[:180]}


def collect(domain, passive=False, findomain=False, whois_cli=False, offline=False):
    if not valid_domain(domain):
        raise ValueError("Please provide a domain like example.com (no scheme or path)")
    notes = []
    data = {
        "app": APP, "domain": domain,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "offline" if offline else "bounded public lookups",
        "ip_addresses": [], "dns": {}, "rdap": {}, "tls": {},
        "website": {}, "security_headers": {}, "crtsh_subdomains": [],
        "findomain": {"installed": False, "names": []}, "whois_cli": {}, "notes": notes,
    }
    if offline:
        notes.append("Offline preview. All network and optional CLI checks skipped.")
        return data
    try:
        ips = sorted({row[4][0] for row in socket.getaddrinfo(
            domain, 443, type=socket.SOCK_STREAM)})
        data["ip_addresses"] = ips
    except OSError as exc:
        notes.append(f"DNS resolution: {exc!s}"[:160])
        ips = []
    if ips and all(public_ip(ip) for ip in ips):
        try:
            with socket.create_connection((domain, 443), timeout=6) as connection:
                with ssl.create_default_context().wrap_socket(
                    connection, server_hostname=domain) as secure:
                    cert = secure.getpeercert()
                    data["tls"] = {
                        "protocol": secure.version(), "cipher": secure.cipher()[0],
                        "subject": cert.get("subject", []), "issuer": cert.get("issuer", []),
                        "valid_from": cert.get("notBefore"), "valid_until": cert.get("notAfter"),
                        "subject_alt_names": [v for kind, v in cert.get("subjectAltName", [])
                                              if kind == "DNS"][:40],
                        "certificate_validated": True,
                    }
        except (OSError, ssl.SSLError) as exc:
            notes.append(f"HTTPS certificate: {exc!s}"[:160])
            data["tls"] = {"certificate_validated": False, "error": str(exc)[:150]}
        try:
            status, headers, body, response_url = fetch("https://" + domain + "/")
            page = PageMetadata()
            page.feed(body.decode("utf-8", errors="replace"))
            headers = {k.lower(): str(v)[:250] for k, v in headers.items()}
            data["website"] = {
                "http_status": status, "url": response_url,
                "title": "".join(page.title)[:250], "description": page.description,
                "canonical_url": page.canonical, "open_graph": page.social,
                "same_site_paths": page.links, "server_header": headers.get("server", "Not observed"),
                "content_type": headers.get("content-type", "Not observed"),
                "redirect_location": headers.get("location", ""),
            }
            data["security_headers"] = {key: headers.get(key, "Not observed") for key in HEADERS}
        except urllib.error.HTTPError as exc:
            data["website"] = {"http_status": exc.code,
                               "redirect_location": exc.headers.get("Location", ""),
                               "notice": "Redirects and error pages were not followed."}
        except (OSError, ValueError, UnicodeError) as exc:
            notes.append(f"Homepage: {exc!s}"[:160])
    else:
        notes.append("HTTPS inspection skipped: target did not resolve exclusively to public IPs.")
    for record_type in RECORD_TYPES:
        data["dns"][record_type] = dns_record(domain, record_type, notes)
    data["rdap"] = rdap(domain, notes)
    if passive:
        data["crtsh_subdomains"] = certificate_names(domain, notes)
    if findomain:
        binary = shutil.which("findomain")
        if not binary:
            notes.append("Findomain not installed; optional check skipped.")
        else:
            response = local_command([binary, "-t", domain, "-q"], seconds=35, limit=60000)
            names = {v for line in response.get("output", "").splitlines()
                     if (v := normalize_subdomain(line, domain))}
            data["findomain"] = {
                "installed": True, "names": sorted(names)[:150],
                "exit_code": response.get("exit_code"), "error": response.get("error", ""),
            }
    if whois_cli:
        binary = shutil.which("whois")
        if binary:
            data["whois_cli"] = local_command([binary, domain])
        else:
            notes.append("WHOIS CLI not installed; RDAP still attempted.")
    return data


def esc(value):
    return html.escape(str(value), quote=True)


def pretty(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, indent=2)[:5000]
    return str(value) if value not in (None, "") else "Not available"


def table(items):
    return "<table>" + "".join("<tr><th>" + esc(key) + "</th><td>" +
                               esc(pretty(value)) + "</td></tr>" for key, value in items) + "</table>"


def card(title, contents, tag="PUBLIC DATA"):
    return "<section><div class='tag'>" + esc(tag) + "</div><h2>" + esc(title) + "</h2>" + contents + "</section>"


def render(data, artwork=None):
    domain = data["domain"]
    picture = Path(artwork).expanduser() if artwork else None
    icon = "<div class='fallback'>🌹</div>"
    if picture and picture.is_file() and picture.suffix.lower() in (".png", ".jpg", ".jpeg") and picture.stat().st_size < 3000000:
        mime = "image/png" if picture.suffix.lower() == ".png" else "image/jpeg"
        icon = "<img class='rosie' alt='Rosie Phantom Labs header artwork' src='data:" + mime + ";base64," + base64.b64encode(picture.read_bytes()).decode("ascii") + "'>"
    sections = []
    sections.append(card("01 / DOMAIN + IP SIGNALS", table([
        ("Domain", domain), ("Public IPs", data.get("ip_addresses", [])),
        ("Timestamp UTC", data.get("created_utc")), ("Mode", data.get("mode"))])))
    sections.append(card("02 / DNS RECORD VAULT", "".join(
        "<h3>" + esc(t) + "</h3><pre>" + esc("\n".join(data.get("dns", {}).get(t, {}).get("records", [])) or "Not observed / unavailable") + "</pre>"
        for t in RECORD_TYPES)))
    sections.append(card("03 / TLS CERTIFICATE", table(data.get("tls", {}).items())))
    sections.append(card("04 / WEBSITE FINGERPRINT", table(data.get("website", {}).items())))
    sections.append(card("05 / SECURITY HEADERS", table(data.get("security_headers", {}).items()) +
                         "<p class='muted'>Missing headers do not prove a security vulnerability.</p>"))
    sections.append(card("06 / WHOIS + RDAP", table(data.get("rdap", {}).items())))
    crt = data.get("crtsh_subdomains", [])
    sections.append(card("07 / CERTIFICATE TRANSPARENCY",
                         "<p>" + str(len(crt)) + " names observed. Historical evidence only.</p><pre>" +
                         esc("\n".join(crt) or "Not requested / none available") + "</pre>", "OPT-IN PASSIVE"))
    findo = data.get("findomain", {})
    sections.append(card("08 / FINDOMAIN",
                         table([("Installed", findo.get("installed")),
                                ("Exit code", findo.get("exit_code")),
                                ("Names", findo.get("names", []))]), "OPTIONAL LOCAL TOOL"))
    whois = data.get("whois_cli", {})
    sections.append(card("09 / WHOIS COMMAND", "<pre>" +
                         esc(whois.get("output", whois.get("error", "Not requested / unavailable"))) +
                         "</pre>", "OPTIONAL LOCAL TOOL"))
    q = urllib.parse.quote(domain)
    portals = [("RDAP", "https://rdap.org/domain/" + q),
               ("crt.sh", "https://crt.sh/?q=" + q),
               ("Google DNS", "https://dns.google/query?name=" + q),
               ("Internet Archive", "https://web.archive.org/web/*/" + q),
               ("ICANN", "https://lookup.icann.org/en/lookup")]
    sections.append(card("10 / INTEL RESEARCH PORTALS", "<ul>" + "".join(
        '<li><a rel="noopener noreferrer" target="_blank" href="' + esc(url) + '">' +
        esc(name) + "</a></li>" for name, url in portals) +
        "</ul><p>External portals open only when clicked.</p>"))
    notes = data.get("notes", []) + [
        "Public records can be incomplete, stale or privacy-redacted.",
        "Subdomains from certificates do not establish ownership or current activity.",
        "No port scanning or vulnerability exploitation is performed.",
    ]
    sections.append(card("11 / NOTES + LIMITS", "<ul>" + "".join(
        "<li>" + esc(note) + "</li>" for note in notes) + "</ul>", "CONTEXT"))
    style = """
:root{color-scheme:dark}*{box-sizing:border-box}
body{margin:0;background:radial-gradient(ellipse at 5% 0,#39122e,#0e1421 48%,#080b10);
color:#edf1f5;font:15px system-ui,sans-serif}
main{max-width:1270px;margin:auto;padding:22px}
header{display:flex;gap:25px;align-items:center;background:#1c1125;border:1px solid #ff149381;
padding:24px;border-radius:20px;box-shadow:0 0 38px #ff149322}
.rosie{width:145px;height:145px;object-fit:contain;border-radius:15px}.fallback{font-size:92px}
.eyebrow{font-size:12px;letter-spacing:.18em;color:#00f5ff}
h1{font-size:clamp(36px,6vw,71px);letter-spacing:-.065em;line-height:1;color:#ff5fb8;margin:10px 0}
header p{color:#b6ff00}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,390px),1fr));gap:16px;margin:23px 0}
section{background:#111927;border:1px solid #343b52;border-radius:14px;padding:22px;overflow-wrap:anywhere;min-width:0}
h2{font-size:17px;color:#b6ff00;margin:10px 0 17px}h3{color:#00f5ff;font-size:13px}
.tag{font-size:10px;letter-spacing:.14em;color:#8cdedc}
table{width:100%;border-collapse:collapse;table-layout:fixed}th,td{border-bottom:1px solid #343b4f;padding:10px 4px;text-align:left;vertical-align:top;white-space:pre-wrap;overflow-wrap:anywhere}
th{width:40%;color:#91e0ed;font-weight:500}
pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:330px;overflow-y:auto;background:#071318;border:1px solid #38464d;color:#bcebcf;padding:13px;border-radius:9px}
a{color:#82eaff}li{margin:8px 0}.muted,footer{color:#b0b8c8;font-size:12px}footer{padding:24px 0}
@media(max-width:650px){header{flex-direction:column;text-align:center}.rosie{width:120px;height:120px}}
"""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            'content="width=device-width,initial-scale=1"><title>ROSIE PHANTOM SCAN V2 | ' +
            esc(domain) + '</title><style>' + style + '</style></head><body><main><header>' +
            icon + '<div><div class="eyebrow">GLITCHBYTE PHANTOM LABS / DOMAIN INTEL STUDIO</div>'
            '<h1>ROSIE PHANTOM<br>SCAN V2</h1><p>' + esc(domain) +
            ' • PUBLIC INTELLIGENCE</p></div></header><div class="grid">' + "".join(sections) +
            '</div><footer>Public-data research only. No identity or vulnerability claims.</footer></main></body></html>')


def export(data, directory, artwork=None):
    folder = Path(directory).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    stem = ("rosie_v2_" + data["domain"].replace(".", "_") + "_" +
            datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + "_" +
            uuid.uuid4().hex[:8])
    page, record = folder / (stem + ".html"), folder / (stem + ".json")
    with page.open("x", encoding="utf-8") as writer:
        writer.write(render(data, artwork))
    with record.open("x", encoding="utf-8") as writer:
        json.dump(data, writer, indent=2, ensure_ascii=False)
        writer.write("\n")
    return page, record


def main(argv=None):
    parser = argparse.ArgumentParser(description=APP + ": bounded public domain intelligence")
    parser.add_argument("domain", nargs="?", help="Domain, e.g. example.com; prompts if omitted")
    parser.add_argument("--passive-subdomains", action="store_true", help="Fetch crt.sh passive names")
    parser.add_argument("--findomain", action="store_true", help="Run installed Findomain (optional)")
    parser.add_argument("--whois-cli", action="store_true", help="Run installed whois command (optional)")
    parser.add_argument("--offline", action="store_true", help="Build safe preview without network")
    parser.add_argument("--artwork", help="Rosie PNG/JPEG for the report header")
    parser.add_argument("--out", default=str(Path.home() / "ROSIE_PHANTOM_SCAN_V2"))
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    if not args.domain:
        try:
            args.domain = input("🌹 Public domain [example.com]: ").strip() or "example.com"
        except (EOFError, KeyboardInterrupt):
            print("\nNo scan requested; terminal remains open.")
            return 0
    domain = args.domain.strip().lower().rstrip(".")
    try:
        result = collect(domain, passive=args.passive_subdomains, findomain=args.findomain,
                         whois_cli=args.whois_cli, offline=args.offline)
        artwork = args.artwork or str(Path(__file__).with_name("rosie_header.png"))
        page, record = export(result, args.out, artwork)
    except (ValueError, OSError) as exc:
        print("Scan could not finish:", exc, file=sys.stderr)
        return 1
    print("[SAVED] HTML:", page)
    print("[SAVED] JSON:", record)
    if not args.no_browser:
        browser = shutil.which("firefox")
        if browser:
            try:
                subprocess.Popen([browser, str(page)], stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 start_new_session=True)
                print("[OPEN] Firefox launched.")
            except OSError as exc:
                print("[INFO] Firefox could not start:", exc)
        else:
            print("[INFO] Firefox unavailable; open the saved HTML manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
