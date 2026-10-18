#!/usr/bin/env python3
"""GHOSTMARK: read-only, offline SHA-256 file integrity and duplicate atlas."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

APP = "GHOSTMARK INTEGRITY ATLAS"
CHUNK = 1024 * 1024


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def inventory(root, *, max_files=5000, max_bytes=100 * 1024 * 1024,
              exclude=None):
    """Collect visible relative paths without following symlinks; never modify files."""
    root = Path(root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Input must be a local directory")
    if not 1 <= max_files <= 100000:
        raise ValueError("--max-files must be between 1 and 100000")
    if max_bytes < 1:
        raise ValueError("--max-mb must be positive")
    exclude = Path(exclude).expanduser().resolve() if exclude else None
    records = []
    skipped = []
    hit_limit = False
    for base, dirs, files in os.walk(root, followlinks=False):
        basepath = Path(base)
        dirs[:] = sorted(d for d in dirs
                         if not (basepath / d).is_symlink()
                         and not (exclude and ((basepath / d).resolve() == exclude
                                  or (basepath / d).resolve().is_relative_to(exclude))))
        for name in sorted(files):
            item = basepath / name
            if item.is_symlink():
                skipped.append({"path": str(item.relative_to(root)), "reason": "symlink"})
                continue
            if exclude and (item.resolve() == exclude or item.resolve().is_relative_to(exclude)):
                continue
            if len(records) >= max_files:
                hit_limit = True
                break
            relative = item.relative_to(root).as_posix()
            try:
                before = item.stat()
                if not item.is_file():
                    skipped.append({"path": relative, "reason": "not a regular file"})
                    continue
                if before.st_size > max_bytes:
                    skipped.append({"path": relative, "reason": "exceeds file size cap"})
                    continue
                fingerprint = sha256_file(item)
                after = item.stat()
                if ((before.st_size, before.st_mtime_ns, before.st_ino)
                        != (after.st_size, after.st_mtime_ns, after.st_ino)):
                    skipped.append({"path": relative, "reason": "changed during scan"})
                    continue
                records.append({"path": relative, "size": after.st_size,
                                "sha256": fingerprint})
            except OSError as exc:
                skipped.append({"path": relative, "reason": f"unreadable: {exc.strerror or 'I/O error'}"})
        if hit_limit:
            break
    return {"format": 1, "app": APP, "root": str(root),
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "files": records, "skipped": skipped,
            "partial": hit_limit or any(s["reason"] not in ("symlink",)
                                        for s in skipped),
            "limit_files": max_files, "limit_bytes_each": max_bytes,
            "notes": ["Offline, read-only hashing. SHA-256 identifies equal content, not ownership.",
                      "File paths in exported reports may be sensitive.",
                      "Symlinks are never followed.",
                      "Files changing during a scan are omitted."]}


def duplicates(records):
    by_hash = defaultdict(list)
    for item in records:
        by_hash[item["sha256"]].append(item["path"])
    return [{"sha256": key, "paths": sorted(paths)}
            for key, paths in sorted(by_hash.items())
            if len(paths) > 1]


def compare(current, baseline):
    if baseline.get("app") != APP or baseline.get("format") != 1:
        raise ValueError("Baseline is not a GHOSTMARK v1 JSON report")
    if baseline.get("root") != current["root"]:
        raise ValueError("Baseline refers to a different input directory")
    prior = {item["path"]: item for item in baseline["files"]}
    now = {item["path"]: item for item in current["files"]}
    return {"added": sorted(now.keys() - prior.keys()),
            "removed": sorted(prior.keys() - now.keys()),
            "changed": sorted(k for k in prior.keys() & now.keys()
                              if prior[k]["sha256"] != now[k]["sha256"]),
            "unchanged": sum(prior[k]["sha256"] == now[k]["sha256"]
                             for k in prior.keys() & now.keys()),
            "warning": ("Comparison can be incomplete if either scan is partial."
                        if baseline.get("partial") or current.get("partial") else "")}


def make_html(manifest, art=None):
    esc = lambda value: html.escape(str(value), quote=True)
    icon = "<div class='fallback'>🌹</div>"
    if art:
        picture = Path(art).expanduser()
        if (picture.is_file() and picture.suffix.lower() in (".png", ".jpg", ".jpeg")
                and picture.stat().st_size <= 2500000):
            import base64
            mime = "image/png" if picture.suffix.lower() == ".png" else "image/jpeg"
            payload = base64.b64encode(picture.read_bytes()).decode("ascii")
            icon = "<img class='hero' alt='Rosie Phantom Labs artwork' src='data:" + mime + ";base64," + payload + "'>"
    files = manifest["files"]
    doubles = manifest["duplicates"]
    comparison = manifest.get("comparison")
    rows = "".join(
        "<tr><td>" + esc(f["path"]) + "</td><td>" + esc(f["size"]) +
        "</td><td><code>" + esc(f["sha256"]) + "</code></td></tr>"
        for f in files
    )
    duphtml = "".join(
        "<li><code>" + esc(group["sha256"][:16]) + "…</code><ul>" +
        "".join("<li>" + esc(path) + "</li>" for path in group["paths"]) +
        "</ul></li>" for group in doubles
    )
    comparehtml = "<p>No baseline selected. Use --baseline with a prior JSON report.</p>"
    if comparison is not None:
        comparehtml = "".join(
            "<h3>" + esc(label.capitalize()) + " (" + str(len(comparison[label])) +
            ")</h3><ul>" + ("".join("<li>" + esc(v) + "</li>"
                            for v in comparison[label]) or "<li>None</li>") + "</ul>"
            for label in ("added", "changed", "removed")
        ) + "<p>" + esc(comparison["warning"]) + "</p>"
    notes = "".join("<li>" + esc(v) + "</li>" for v in manifest["notes"])
    skipped = "".join("<tr><td>" + esc(v["path"]) + "</td><td>" +
                      esc(v["reason"]) + "</td></tr>" for v in manifest["skipped"])
    template = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GHOSTMARK | GLITCHBYTE PHANTOM LABS</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}
body{margin:0;background:radial-gradient(ellipse at 5% 0,#28223f,#0a1017 56%,#05060a);
color:#e5f5ef;font:15px system-ui,sans-serif}
main{max-width:1190px;margin:auto;padding:24px}header{display:flex;gap:28px;
align-items:center;padding:28px;background:#151528;border:1px solid #abf75e;
border-radius:18px;box-shadow:0 0 45px #75ff6520}
.hero{width:125px;height:125px;object-fit:contain}.fallback{font-size:84px}
small{color:#80e7e1;letter-spacing:.18em}h1{font-size:clamp(38px,7vw,78px);
line-height:.98;letter-spacing:-.075em;color:#b6ff68;margin:12px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,410px),1fr));gap:16px;margin:22px 0}
section{border:1px solid #364957;border-radius:14px;background:#131b25;padding:22px;overflow:auto}
h2{color:#ff77bd;font-size:19px}h3{color:#83eeeb;font-size:15px}
table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:9px;
border-bottom:1px solid #33414b;vertical-align:top;overflow-wrap:anywhere}
th{color:#8be4df}code{font-size:12px;color:#a9ff9b;overflow-wrap:anywhere}
li{margin:7px 0}footer{color:#9ab5b1;padding:20px 0;font-size:13px}
@media(max-width:650px){header{flex-direction:column;text-align:center}}
</style></head><body><main><header>__ICON__
<div><small>GLITCHBYTE PHANTOM LABS / OFFLINE INTEGRITY</small>
<h1>GHOSTMARK<br>ATLAS_</h1><p>READ ONLY · SHA-256 · FILE CONSTELLATION</p>
</div></header><div class="grid">
<section><h2>01 / INVENTORY</h2><p><strong>Root:</strong> __ROOT__</p>
<p><strong>Files hashed:</strong> __COUNT__</p>
<p><strong>Partial scan:</strong> __PARTIAL__</p>
<p><strong>UTC:</strong> __CREATED__</p></section>
<section><h2>02 / DUPLICATE CONTENT</h2><p>__DUPCOUNT__ matching SHA-256 groups.</p><ul>__DUPS__</ul></section>
<section><h2>03 / CHANGE DETECTOR</h2>__COMPARE__</section>
<section><h2>04 / SCAN NOTES</h2><ul>__NOTES__</ul></section>
<section><h2>05 / FILE SIGNATURES</h2><table><thead><tr>
<th>Relative path</th><th>Bytes</th><th>SHA-256</th></tr></thead><tbody>__ROWS__</tbody></table></section>
<section><h2>06 / SKIPPED ITEMS</h2><table><thead><tr><th>Path</th>
<th>Reason</th></tr></thead><tbody>__SKIPPED__</tbody></table></section>
</div><footer>Files were not modified or uploaded. Reports contain local paths.</footer></main></body></html>"""
    replacements = {
        "__ICON__": icon,
        "__ROOT__": esc(manifest["root"]),
        "__COUNT__": str(len(files)),
        "__PARTIAL__": esc(manifest["partial"]),
        "__CREATED__": esc(manifest["created_utc"]),
        "__DUPCOUNT__": str(len(doubles)),
        "__DUPS__": duphtml or "<li>No duplicate-content groups found.</li>",
        "__COMPARE__": comparehtml,
        "__NOTES__": notes,
        "__ROWS__": rows,
        "__SKIPPED__": skipped,
    }
    for token, content in replacements.items():
        template = template.replace(token, content)
    return template


def write_report(report, directory, art=None):
    directory = Path(directory).expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    stem = "ghostmark_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:10]
    jsonpath = directory / (stem + ".json")
    htmlpath = directory / (stem + ".html")
    with jsonpath.open("x", encoding="utf-8") as fp:
        json.dump(report, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
    with htmlpath.open("x", encoding="utf-8") as fp:
        fp.write(make_html(report, art))
    return jsonpath, htmlpath


def main(argv=None):
    parser = argparse.ArgumentParser(description=APP + ": offline read-only local file inventory")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--folder", help="Local folder to hash; no symlinks followed")
    group.add_argument("--demo", action="store_true", help="Generate synthetic demonstration in a temporary folder")
    parser.add_argument("--baseline", help="Previous GHOSTMARK JSON for changes; must match --folder")
    parser.add_argument("--max-files", type=int, default=5000)
    parser.add_argument("--max-mb", type=int, default=100, help="Maximum size for each file, in MiB")
    parser.add_argument("--out", default=str(Path.home() / "GhostmarkAtlasReports"))
    parser.add_argument("--artwork", help="Optional local Rosie PNG/JPEG for header")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    if args.demo and args.baseline:
        parser.error("--baseline requires --folder, not --demo")
    try:
        # Never scan report outputs when --out is inside --folder.
        output = Path(args.out).expanduser().resolve()
        if args.demo:
            with tempfile.TemporaryDirectory(prefix="ghostmark-sample-") as temp:
                sample = Path(temp)
                (sample / "hello.txt").write_text("GHOSTMARK: original local demo\n", encoding="utf-8")
                (sample / "same.txt").write_text("GHOSTMARK: original local demo\n", encoding="utf-8")
                (sample / "other.txt").write_text("Rose signal atlas\n", encoding="utf-8")
                report = inventory(sample, max_files=args.max_files, max_bytes=args.max_mb * 1024 * 1024)
                report["root"] = "[synthetic temporary demonstration]"
        else:
            report = inventory(args.folder, max_files=args.max_files,
                               max_bytes=args.max_mb * 1024 * 1024, exclude=output)
        report["duplicates"] = duplicates(report["files"])
        if args.baseline:
            baseline = json.loads(Path(args.baseline).expanduser().read_text(encoding="utf-8"))
            report["comparison"] = compare(report, baseline)
        artwork = args.artwork or str(Path(__file__).with_name("rosie_header.png"))
        record, page = write_report(report, output, artwork)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("[ERROR]", exc, file=sys.stderr)
        return 1
    print("[SAVED] JSON:", record)
    print("[SAVED] HTML:", page)
    print("[SUMMARY]", len(report["files"]), "files;",
          len(report["duplicates"]), "duplicate groups;",
          len(report["skipped"]), "skipped.")
    if not args.no_browser:
        browser = shutil.which("firefox")
        if browser:
            try:
                subprocess.Popen([browser, str(page)], stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 start_new_session=True)
                print("[OPEN] Firefox launched.")
            except OSError as exc:
                print("[INFO] Firefox launch failed:", exc)
        else:
            print("[INFO] Firefox unavailable; open the HTML report manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
