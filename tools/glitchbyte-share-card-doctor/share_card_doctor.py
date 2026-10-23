#!/usr/bin/env python3
"""GLITCHBYTE // SHARE CARD DOCTOR: public Open Graph & X-card diagnostic.

Read-only; standard library only; never posts to a social network.
Only requests the user's public GlitchByte Hangout host.
"""
import argparse
import html.parser
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

HOST = "glitchbyte.alwaysdata.net"
DEFAULT_URL = "https://" + HOST + "/hangout"
KEEP_QUERY = {"page"}  # strip fbclid, utm_source, and other tracking keys
USER_AGENT = "GlitchByte-Share-Card-Doctor/1.0 (+read-only preview check)"


def canonicalize(raw):
    value = urllib.parse.urlsplit(raw.strip())
    if value.scheme != "https" or (value.hostname or "").lower() != HOST:
        raise ValueError("Only https://" + HOST + " public pages are supported")
    if value.username or value.password or value.port:
        raise ValueError("Credentials and nonstandard ports are not permitted")
    path = value.path or "/hangout"
    if not (path == "/hangout" or path == "/welcome"):
        raise ValueError("Use the public /hangout or /welcome link, not a private invite")
    query = urllib.parse.urlencode([
        (k, v) for k, v in urllib.parse.parse_qsl(value.query, keep_blank_values=True)
        if k in KEEP_QUERY
    ])
    return urllib.parse.urlunsplit(("https", HOST, path, query, ""))


class MetaTags(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            name = (attrs.get("property") or attrs.get("name") or "").lower()
            if name and "content" in attrs and name not in self.meta:
                self.meta[name] = attrs["content"]
        elif tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonical = attrs.get("href")


def get_public(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,image/jpeg,image/png,image/webp,*/*"
    })
    with urllib.request.urlopen(req, timeout=12) as res:
        final = urllib.parse.urlsplit(res.geturl())
        if (final.hostname or "").lower() != HOST or final.scheme != "https":
            raise ValueError("Redirect left the approved GlitchByte host")
        typ = res.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if method == "HEAD":
            return res.status, typ, b""
        return res.status, typ, res.read(2_000_001)


def diagnose(url):
    page = canonicalize(url)
    status, mime, body = get_public(page)
    if status != 200 or mime != "text/html":
        raise ValueError("Public page returned HTTP %s (%s)" % (status, mime))
    if len(body) > 2_000_000:
        raise ValueError("Page exceeded diagnostic's 2 MB safety limit")
    tags = MetaTags()
    tags.feed(body.decode("utf-8", "replace"))
    meta = tags.meta
    image = meta.get("og:image")
    results = {
        "clean_url": page,
        "og:url": meta.get("og:url"),
        "og:title": meta.get("og:title"),
        "og:description": meta.get("og:description"),
        "og:image": image,
        "twitter:card": meta.get("twitter:card"),
        "canonical": tags.canonical,
        "image_http": None,
        "image_mime": None,
        "checks": {},
        "facebook_debugger": "https://developers.facebook.com/tools/debug/",
    }
    results["checks"]["title"] = bool(meta.get("og:title"))
    results["checks"]["description"] = bool(meta.get("og:description"))
    results["checks"]["clean_canonical"] = meta.get("og:url") == page
    results["checks"]["large_x_card"] = meta.get("twitter:card") == "summary_large_image"
    if image:
        absolute = urllib.parse.urljoin(page, image)
        parsed = urllib.parse.urlsplit(absolute)
        if parsed.scheme == "https" and (parsed.hostname or "").lower() == HOST and not parsed.port:
            try:
                code, image_type, _ = get_public(absolute, "HEAD")
                results["image_http"] = code
                results["image_mime"] = image_type
                results["checks"]["image"] = code == 200 and image_type.startswith("image/")
            except urllib.error.HTTPError as e:
                results["image_http"] = e.code
                results["checks"]["image"] = False
            except (urllib.error.URLError, ValueError) as e:
                results["checks"]["image"] = False
                results["image_error"] = str(e)
        else:
            results["checks"]["image"] = False
            results["image_error"] = "Preview image must be HTTPS on approved host"
    else:
        results["checks"]["image"] = False
    return results


def main():
    p = argparse.ArgumentParser(description="Read-only GlitchByte OG and X share card check.")
    p.add_argument("--url", default=DEFAULT_URL, help="Public Hangout or Welcome URL")
    p.add_argument("--json", action="store_true", help="Show machine-readable findings")
    a = p.parse_args()
    try:
        r = diagnose(a.url)
    except (ValueError, urllib.error.URLError, TimeoutError, OSError) as e:
        print("[ERROR] " + str(e), file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print("╔══════════════════════════════════════════════════╗")
        print("║ GLITCHBYTE // SHARE CARD DOCTOR                 ║")
        print("╚══════════════════════════════════════════════════╝")
        print("[LINK]  " + r["clean_url"])
        for k in ("og:title", "og:description", "og:image", "twitter:card"):
            print("[" + k + "] " + str(r[k]))
        for k, ok in r["checks"].items():
            print(("[PASS] " if ok else "[CHECK] ") + k)
        print("[META DEBUGGER] " + r["facebook_debugger"])
        print("[NOTE] Press Scrape Again there; this program cannot clear Facebook's cache.")
    return 0 if all(r["checks"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
