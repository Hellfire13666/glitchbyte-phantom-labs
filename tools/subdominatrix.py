#!/usr/bin/env python3
"""SUBDOMINATRIX: bounded passive subdomain discovery and optional public-host verification.

Python 3 standard library only. No brute force, port scanning, credential use, exploit
testing or follow-on crawling. DNS and HTTPS checks are opt-in and limited.
"""
import argparse
import csv
from datetime import datetime, timezone
import html
import ipaddress
import json
from pathlib import Path
import re
import secrets
import shutil
import socket
import ssl
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.error
import urllib.parse
import urllib.request
import uuid

APP = "SUBDOMINATRIX"
UA = "Subdominatrix/1.0 (GlitchByte Phantom Labs public-domain research)"
RECORD_LIMIT = 3000
MAX_RESPONSE = 1_800_000
SOURCES = ("crt.sh", "AlienVault OTX", "HackerTarget", "urlscan.io")
VALID_LABEL = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z")


def valid_domain(value):
    if not isinstance(value, str) or len(value) > 253 or "." not in value:
        return False
    try:
        ipaddress.ip_address(value)
        return False
    except ValueError:
        pass
    labels = value.split(".")
    return all(VALID_LABEL.fullmatch(part) for part in labels)


def normalize(candidate, domain):
    """Accept only bona fide child hostnames of the exact requested domain."""
    if not isinstance(candidate, str):
        return None
    name = candidate.strip().strip(".").lower()
    if name.startswith("*."):
        name = name[2:]
    if len(name) > 253 or name == domain or not name.endswith("." + domain):
        return None
    return name if valid_domain(name) else None


def fetch_json(url, timeout=10):
    # URLs are assembled only from hard-coded trusted service origins and domain values.
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError("HTTP status " + str(response.status))
        raw = response.read(MAX_RESPONSE + 1)
    if len(raw) > MAX_RESPONSE:
        raise ValueError("Response exceeded 1.8 MB safe limit")
    return json.loads(raw.decode("utf-8", errors="replace"))


def fetch_source(source, domain, timeout=10):
    quoted = urllib.parse.quote(domain, safe="")
    names = set()
    if source == "crt.sh":
        data = fetch_json("https://crt.sh/?" + urllib.parse.urlencode(
            {"q": "%." + domain, "output": "json"}), timeout)
        if not isinstance(data, list):
            raise ValueError("crt.sh did not return a JSON array")
        for item in data[:RECORD_LIMIT]:
            if isinstance(item, dict):
                for name in str(item.get("name_value", "")).splitlines():
                    if (normalized := normalize(name, domain)):
                        names.add(normalized)
    elif source == "AlienVault OTX":
        data = fetch_json(
            "https://otx.alienvault.com/api/v1/indicators/domain/" + quoted + "/passive_dns",
            timeout)
        if not isinstance(data, dict):
            raise ValueError("OTX returned an unexpected response")
        for item in data.get("passive_dns", [])[:RECORD_LIMIT]:
            if isinstance(item, dict):
                if (normalized := normalize(item.get("hostname", ""), domain)):
                    names.add(normalized)
    elif source == "HackerTarget":
        request = urllib.request.Request(
            "https://api.hackertarget.com/hostsearch/?" +
            urllib.parse.urlencode({"q": domain}), headers={"User-Agent": UA})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(MAX_RESPONSE + 1)
        if len(body) > MAX_RESPONSE:
            raise ValueError("HackerTarget response exceeded limit")
        decoded = body.decode("utf-8", errors="replace")
        if decoded.lower().startswith(("error", "api count", "you have reached")):
            raise ValueError(decoded[:150])
        for line in decoded.splitlines()[:RECORD_LIMIT]:
            if (normalized := normalize(line.split(",", 1)[0], domain)):
                names.add(normalized)
    elif source == "urlscan.io":
        data = fetch_json(
            "https://urlscan.io/api/v1/search/?" +
            urllib.parse.urlencode({"q": "domain:" + domain, "size": 100}), timeout)
        if not isinstance(data, dict):
            raise ValueError("urlscan returned an unexpected response")
        for item in data.get("results", [])[:100]:
            if not isinstance(item, dict):
                continue
            for record in (item.get("page", {}), item.get("task", {})):
                if isinstance(record, dict):
                    if (normalized := normalize(record.get("domain", ""), domain)):
                        names.add(normalized)
    return sorted(names)[:RECORD_LIMIT]


def optional_cli(program, domain, timeout=30):
    binary = shutil.which(program)
    if not binary:
        return None, {"source": program, "status": "missing (optional)", "count": 0,
                      "seconds": 0, "detail": "Install separately to enable this source"}
    command = [binary, "-d", domain, "-silent"] if program == "subfinder" else [
        binary, "-t", domain, "-q"]
    started = time.monotonic()
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout,
                              errors="replace", check=False)
        output = proc.stdout[:MAX_RESPONSE]
        names = {n for line in output.splitlines()[:RECORD_LIMIT]
                 if (n := normalize(line, domain))}
        status = "ok" if proc.returncode == 0 else "failed"
        info = (proc.stderr or "").strip()[:180] if proc.returncode else "Installed local executable"
        return sorted(names), {"source": program, "status": status, "count": len(names),
                               "seconds": round(time.monotonic()-started, 2),
                               "detail": info}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], {"source": program, "status": "failed", "count": 0,
                    "seconds": round(time.monotonic()-started, 2), "detail": str(exc)[:180]}


def public_ip(value):
    try:
        return ipaddress.ip_address(value).is_global
    except ValueError:
        return False


def dns_check(host, timeout=5):
    # socket DNS resolution time may be platform-dependent; executor bounds workers.
    try:
        raw = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        ips = sorted({record[4][0] for record in raw})
        if not ips:
            return {"dns": "unresolved", "ips": [], "detail": "No addresses"}
        if not all(public_ip(ip) for ip in ips):
            return {"dns": "nonpublic", "ips": ips[:8],
                    "detail": "At least one private/reserved IP; HTTPS check disabled"}
        return {"dns": "public", "ips": ips[:8], "detail": ""}
    except OSError as exc:
        return {"dns": "unresolved", "ips": [], "detail": str(exc)[:120]}


def head_https(host, ips, timeout=4):
    """A single HTTPS HEAD to a resolved *public IP* with verified hostname and no redirects."""
    target = next((ip for ip in ips if public_ip(ip)), None)
    if target is None or not all(public_ip(ip) for ip in ips):
        return {"http": "skipped", "detail": "No verified exclusively public addresses"}
    try:
        with socket.create_connection((target, 443), timeout=timeout) as sock:
            with ssl.create_default_context().wrap_socket(
                sock, server_hostname=host) as tls:
                tls.settimeout(timeout)
                request = ("HEAD / HTTP/1.1\r\nHost: " + host +
                           "\r\nUser-Agent: " + UA +
                           "\r\nAccept: */*\r\nConnection: close\r\n\r\n")
                tls.sendall(request.encode("ascii"))
                payload = bytearray()
                while b"\r\n\r\n" not in payload and len(payload) < 15000:
                    chunk = tls.recv(min(2048, 15000-len(payload)))
                    if not chunk:
                        break
                    payload.extend(chunk)
                header_text = payload.decode("iso-8859-1", errors="replace").split("\r\n\r\n")[0]
                lines = header_text.split("\r\n")
                match = re.match(r"HTTP/\d(?:\.\d)?\s+(\d{3})", lines[0] if lines else "")
                if not match:
                    return {"http": "failed", "detail": "No HTTP response status"}
                headers = {}
                for line in lines[1:]:
                    if ":" in line:
                        key, val = line.split(":", 1)
                        headers[key.strip().lower()] = val.strip()[:250]
                stack = []
                server = headers.get("server", "").lower()
                powered = headers.get("x-powered-by", "").lower()
                for needle, label in (("nginx", "nginx"), ("apache", "Apache"),
                                      ("cloudflare", "Cloudflare"), ("iis", "Microsoft IIS"),
                                      ("openresty", "OpenResty"), ("litespeed", "LiteSpeed")):
                    if needle in server:
                        stack.append(label)
                for needle, label in (("express", "Express"), ("php", "PHP"),
                                      ("asp.net", "ASP.NET")):
                    if needle in powered:
                        stack.append(label)
                if "cf-ray" in headers and "Cloudflare" not in stack:
                    stack.append("Cloudflare")
                if "x-vercel-id" in headers:
                    stack.append("Vercel")
                if "x-nf-request-id" in headers:
                    stack.append("Netlify")
                return {"http": "observed", "status": int(match.group(1)),
                        "tls": tls.version(), "tech": sorted(set(stack)),
                        "server": headers.get("server", "")[:100],
                        "detail": "HTTPS HEAD; redirects not followed"}
    except (OSError, ssl.SSLError, ValueError) as exc:
        return {"http": "failed", "detail": str(exc)[:120]}


def collect(domain, *, demo=False, max_results=1500, max_verify=80,
            dns=False, http=False, subfinder=False, findomain=False, timeout=10):
    if not valid_domain(domain):
        raise ValueError("Provide only a DNS domain, e.g. example.com")
    if not 1 <= max_results <= 3000 or not 0 <= max_verify <= 250:
        raise ValueError("max-results must be 1..3000 and max-verify 0..250")
    if not 2 <= timeout <= 30:
        raise ValueError("timeout must be 2..30 seconds")
    if http and not dns:
        raise ValueError("--http-check requires --dns-check")
    started = datetime.now(timezone.utc).isoformat()
    findings, feedback = {}, []

    def merge(source, names):
        for name in names:
            if len(findings) >= max_results and name not in findings:
                break
            findings.setdefault(name, set()).add(source)

    if demo:
        demo_sources = {
            "crt.sh": ["www", "api", "docs", "status", "mail", "staging"],
            "AlienVault OTX": ["www", "api", "shop", "cdn", "support"],
            "HackerTarget": ["docs", "vpn", "portal", "beta"],
            "urlscan.io": ["www", "shop", "blog", "status"],
        }
        for source, labels in demo_sources.items():
            names = [label + "." + domain for label in labels]
            merge(source, names)
            feedback.append({"source": source, "status": "synthetic demo",
                             "count": len(names), "seconds": 0, "detail": "No network calls"})
        if subfinder or findomain:
            for name in ("subfinder", "findomain"):
                if (name == "subfinder" and subfinder) or (name == "findomain" and findomain):
                    feedback.append({"source": name, "status": "skipped in demo",
                                     "count": 0, "seconds": 0, "detail": "No tools executed"})
    else:
        # Public-source requests are concurrent, but only four well-known services.
        def run_one(source):
            tick = time.monotonic()
            try:
                names = fetch_source(source, domain, timeout)
                return source, names, {"source": source, "status": "ok",
                                      "count": len(names), "seconds": round(time.monotonic()-tick, 2),
                                      "detail": "Public data; can be historical or incomplete"}
            except (OSError, urllib.error.URLError, ValueError, TypeError, KeyError,
                    json.JSONDecodeError) as exc:
                return source, [], {"source": source, "status": "unavailable",
                                    "count": 0, "seconds": round(time.monotonic()-tick, 2),
                                    "detail": str(exc)[:180]}

        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {pool.submit(run_one, name): name for name in SOURCES}
            completed = {}
            for future in as_completed(futures):
                source, names, info = future.result()
                completed[source] = (names, info)
                print(f"[SOURCE] {source}: {info['status']} | {len(names)} records", flush=True)
        for source in SOURCES:
            names, info = completed[source]
            merge(source, names)
            feedback.append(info)
        for program, enabled in (("subfinder", subfinder), ("findomain", findomain)):
            if not enabled:
                continue
            names, info = optional_cli(program, domain, timeout=min(30, timeout*3))
            merge(program, names or [])
            feedback.append(info)
            print(f"[OPTIONAL] {program}: {info['status']} | {info['count']} records", flush=True)

    names = sorted(findings)[:max_results]
    records = [{"name": name, "sources": sorted(findings[name]), "dns": "not checked",
                "ips": [], "http": "not checked", "status": None, "tech": [],
                "detail": ""} for name in names]
    if dns and not demo:
        selected = records[:max_verify]
        print(f"[VERIFY] DNS checking {len(selected)} hosts (limit {max_verify})", flush=True)
        with ThreadPoolExecutor(max_workers=8) as pool:
            tasks = {pool.submit(dns_check, row["name"], timeout): row for row in selected}
            for future in as_completed(tasks):
                row = tasks[future]
                row.update(future.result())
        if http:
            permitted = [row for row in selected if row["dns"] == "public"]
            print(f"[VERIFY] HTTPS HEAD on {len(permitted)} public DNS hosts", flush=True)
            with ThreadPoolExecutor(max_workers=6) as pool:
                tasks = {pool.submit(head_https, row["name"], row["ips"], min(timeout, 6)):
                         row for row in permitted}
                for future in as_completed(tasks):
                    tasks[future].update(future.result())
    elif demo and (dns or http):
        feedback.append({"source": "DNS / HTTP", "status": "skipped in demo",
                         "count": 0, "seconds": 0, "detail": "Synthetic data; no active checks"})
    stats = {"names": len(records),
             "multi_source": sum(len(row["sources"]) > 1 for row in records),
             "dns_public": sum(row["dns"] == "public" for row in records),
             "http_observed": sum(row["http"] == "observed" for row in records),
             "unique_ips": len({ip for row in records for ip in row["ips"] if public_ip(ip)}),
             "technologies": sorted({tech for row in records for tech in row["tech"]})}
    return {
        "project": APP, "version": 1, "target": domain,
        "created_utc": started, "mode": "SYNTHETIC OFFLINE DEMO" if demo else "PUBLIC SOURCE COLLECTION",
        "settings": {"max_results": max_results, "max_verify": max_verify, "dns_check": dns,
                     "http_check": http, "subfinder": subfinder, "findomain": findomain},
        "stats": stats, "sources": feedback, "hosts": records,
        "notes": [
            "Third-party passive listings are not proof of control, current activity or ownership.",
            "DNS public resolution is not a vulnerability or proof of an active website.",
            "Technology labels are hints inferred solely from an HTTPS response header.",
            "Opt-in HTTPS uses one HEAD request per verified public host; no redirects, crawling or port scans.",
            "Screenshots, global geolocation and vulnerability scoring are not implemented.",
            "Demo names, counts and results are synthetic, not internet observations.",
        ]}


def render(report, artwork=None):
    esc = lambda value: html.escape(str(value), quote=True)
    image = '<div class="rose">🌹</div>'
    picture = Path(artwork).expanduser() if artwork else None
    if picture and picture.is_file() and picture.suffix.lower() in (".png", ".jpg", ".jpeg") and picture.stat().st_size < 3000000:
        import base64
        mime = "image/png" if picture.suffix.lower() == ".png" else "image/jpeg"
        image = '<img alt="Rosie GlitchByte Phantom Labs banner artwork" src="data:' + mime + ';base64,' + base64.b64encode(picture.read_bytes()).decode("ascii") + '" class="hero-art">'
    stats = report["stats"]
    tiles = "".join('<article class="stat"><strong>' + esc(stats[key]) + '</strong><span>' + esc(label) + '</span></article>'
                    for key, label in (("names", "UNIQUE NAMES"), ("multi_source", "MULTI-SOURCE"),
                                       ("dns_public", "DNS PUBLIC"), ("http_observed", "HTTPS OBSERVED"),
                                       ("unique_ips", "UNIQUE PUBLIC IPS")))
    source_rows = "".join("<tr><td>" + esc(source["source"]) + "</td><td>" +
                          esc(source["status"]) + "</td><td>" + esc(source["count"]) +
                          "</td><td>" + esc(source["seconds"]) + "s</td><td>" +
                          esc(source["detail"]) + "</td></tr>" for source in report["sources"])
    hosts = "".join(
        "<tr><td><code>" + esc(row["name"]) + "</code></td><td>" +
        esc(", ".join(row["sources"])) + "</td><td>" + esc(row["dns"]) + "</td><td>" +
        esc(", ".join(row["ips"])) + "</td><td>" + esc(row["http"]) +
        ((" " + esc(row["status"])) if row.get("status") is not None else "") +
        "</td><td>" + esc(", ".join(row["tech"])) + "</td></tr>"
        for row in report["hosts"])
    notes = "".join("<li>" + esc(note) + "</li>" for note in report["notes"])
    tech = ", ".join(stats["technologies"]) or "No technologies observed"
    css = """
:root{color-scheme:dark}*{box-sizing:border-box}
body{margin:0;background:radial-gradient(ellipse at 40% 0,#272043,#090b15 51%,#030408);
color:#e4f9fb;font:15px system-ui,sans-serif}main{max-width:1460px;margin:auto;padding:20px}
header{border:1px solid #e827ad;border-radius:17px;background:linear-gradient(115deg,#271026,#081520);
display:flex;align-items:center;gap:22px;padding:20px;box-shadow:0 0 28px #ff149333}
.hero-art{max-width:220px;max-height:170px;object-fit:contain;border-radius:10px}.rose{font-size:85px}
.eyebrow{color:#4cfafa;letter-spacing:.21em;font-size:11px}
h1{margin:5px 0;font-size:clamp(38px,7vw,85px);letter-spacing:-.075em;line-height:1;
color:#ff2fac;text-shadow:3px 2px #06e4ed}
.tagline{color:#b6ff00;font-weight:600}h2{color:#05f2f9;font-size:21px;margin:0 0 12px}
.wrap{display:flex;gap:12px;flex-wrap:wrap;margin:17px 0}
.stat{flex:1;min-width:135px;background:#101825;border:1px solid #8b2be282;padding:17px;border-radius:12px}
.stat strong{color:#ff3fab;font-size:36px;display:block}.stat span{color:#9fe8ef;font-size:11px;letter-spacing:.1em}
.panel{background:#0e1421;border:1px solid #3c4f62;border-radius:12px;padding:20px;margin:14px 0;overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:640px}
th{text-align:left;color:#bbff72;background:#101d21;font-weight:500;position:sticky;top:0}
td,th{padding:10px 9px;border-bottom:1px solid #273548;vertical-align:top;overflow-wrap:anywhere}
tr:nth-child(even){background:#121b29}td code{color:#6df0ff}
input{background:#070c14;color:#f6f6ff;border:1px solid #fd3cad;border-radius:9px;padding:12px;
font:inherit;width:min(100%,420px);margin:10px 0}
.pill{display:inline-block;padding:6px 13px;border:1px solid #b6ff00;color:#b6ff00;
border-radius:8px;font-size:12px;font-weight:700}
.note{color:#b5c9d1;line-height:1.65}li{margin:9px 0}
footer{color:#a2b3c5;font-size:12px;padding:20px}
@media(max-width:700px){header{display:block}.hero-art{width:100%;max-width:100%}}
"""
    script = """<script>
const q=document.getElementById('filter');
q.addEventListener('input',()=>{const needle=q.value.toLowerCase();
for(const tr of document.querySelectorAll('#hosts tbody tr'))
tr.hidden=!tr.textContent.toLowerCase().includes(needle)});
</script>"""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SUBDOMINATRIX • ' +
            esc(report["target"]) + '</title><style>' + css + '</style></head><body><main><header>' + image +
            '<div><div class="eyebrow">GLITCHBYTE PHANTOM LABS / ROSIEGLITCHBYTE</div>'
            '<h1>SUBDOMINATRIX</h1><div class="tagline">SAME DOMAINS. DIFFERENT PERSPECTIVE.</div>'
            '<p>SUBDOMAIN INTELLIGENCE • PUBLIC SOURCE FEEDBACK • VERIFIED REPORTING</p>'
            '<span class="pill">' + esc(report["mode"]) + '</span></div></header><div class="wrap">' +
            tiles + '</div><section class="panel"><h2>01 / SOURCE SIGNALS</h2><p class="note">Each source can be empty, blocked, or rate limited. Missing data is not a finding.</p>'
            '<table><thead><tr><th>Source</th><th>State</th><th>Names</th><th>Seconds</th><th>Feedback</th></tr></thead><tbody>' +
            source_rows + '</tbody></table></section><section class="panel"><h2>02 / SUBDOMAIN ATLAS</h2>'
            '<p class="note">Target: <b>' + esc(report["target"]) + '</b> · Timestamp UTC: ' +
            esc(report["created_utc"]) + '</p><input id="filter" aria-label="Filter hosts" placeholder="Filter hostnames, IPs, technology, sources…">'
            '<table id="hosts"><thead><tr><th>Hostname</th><th>Source(s)</th><th>DNS</th><th>Public IPs</th><th>HTTPS</th><th>Header tech hints</th></tr></thead><tbody>' +
            hosts + '</tbody></table></section><section class="panel"><h2>03 / TECHNOLOGY INDICATORS</h2><p>' +
            esc(tech) + '</p><p class="note">Only derived from opted-in HTTPS response headers, not a comprehensive stack audit.</p></section>'
            '<section class="panel"><h2>04 / CONFIDENCE AND LIMITS</h2><ul class="note">' + notes +
            '</ul></section><footer>No hidden scans • No user credentials • No fabricated live host counts • RosieGlitchbyte Phantom Labs</footer></main>' +
            script + '</body></html>')


def export(report, folder, artwork=None):
    folder = Path(folder).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    token = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    basename = "subdominatrix_" + report["target"].replace(".", "_") + "_" + token
    paths = {kind: folder / (basename + "." + kind) for kind in ("html", "json", "csv", "txt")}
    with paths["json"].open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with paths["html"].open("x", encoding="utf-8") as handle:
        handle.write(render(report, artwork))
    with paths["csv"].open("x", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("hostname", "sources", "dns", "public_ips", "https", "status", "technologies"))
        for row in report["hosts"]:
            writer.writerow((row["name"], "|".join(row["sources"]), row["dns"],
                             "|".join(row["ips"]), row["http"], row["status"] or "",
                             "|".join(row["tech"])))
    with paths["txt"].open("x", encoding="utf-8") as handle:
        handle.write("\n".join(row["name"] for row in report["hosts"]) + "\n")
    return paths


def main(argv=None):
    parser = argparse.ArgumentParser(description=APP + " • Multi-source passive domain intel")
    parser.add_argument("domain", nargs="?", default="example.com",
                        help="Only a hostname, e.g. example.com; default example.com")
    parser.add_argument("--offline-demo", action="store_true", help="Synthetic report with NO internet")
    parser.add_argument("--subfinder", action="store_true", help="Use installed Subfinder executable")
    parser.add_argument("--findomain", action="store_true", help="Use installed Findomain executable")
    parser.add_argument("--dns-check", action="store_true", help="Resolve limited discovered hostnames")
    parser.add_argument("--http-check", action="store_true",
                        help="Opt-in HTTPS HEAD against verified public IPs; requires --dns-check")
    parser.add_argument("--max-results", type=int, default=1500)
    parser.add_argument("--max-verify", type=int, default=80)
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--out", default=str(Path.home() / "SUBDOMINATRIX_REPORTS"))
    parser.add_argument("--artwork", help="Optional Rosie PNG/JPEG for dashboard header")
    parser.add_argument("--no-open", action="store_true", help="Do not launch Firefox")
    args = parser.parse_args(argv)
    domain = args.domain.strip().lower().strip(".")
    try:
        report = collect(domain, demo=args.offline_demo, max_results=args.max_results,
                         max_verify=args.max_verify, dns=args.dns_check,
                         http=args.http_check, subfinder=args.subfinder, findomain=args.findomain,
                         timeout=args.timeout)
        image = args.artwork or str(Path(__file__).with_name("rosie_header.png"))
        paths = export(report, args.out, image)
    except (OSError, ValueError) as exc:
        print("[ERROR]", exc, file=sys.stderr)
        return 1
    for fmt, path in paths.items():
        print("[SAVED]", fmt.upper(), path)
    print("[SUMMARY]", report["stats"]["names"], "unique names;",
          report["stats"]["multi_source"], "seen in 2+ sources;",
          report["stats"]["dns_public"], "public DNS;",
          report["stats"]["http_observed"], "observed HTTPS responses.")
    if not args.no_open:
        browser = shutil.which("firefox")
        if browser:
            try:
                subprocess.Popen([browser, str(paths["html"])], stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 start_new_session=True)
                print("[OPEN] Firefox launched")
            except OSError as exc:
                print("[INFO] Firefox unavailable:", exc)
        else:
            print("[INFO] Firefox not found; open saved HTML path manually")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
