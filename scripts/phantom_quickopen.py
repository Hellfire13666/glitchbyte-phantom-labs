#!/usr/bin/env python3
"""Phantom Labs one-paste launchers for verified HTML-exporting Python tools.

The launcher only fetches first-party GitHub files into its dedicated workspace.
It does not alter a checkout, delete originals, or run remote shell commands.
Review source before executing downloaded code.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

RAW = "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/"
TOOLS = {
    "hexwake": "hexwake_palette_foundry.py",
    "cipherbox": "phantom_cipherbox.py",
    "rosie-scan": "rosie_phantom_scan_v2.py",
    "ghostmark": "ghostmark_integrity_atlas.py",
}
MAX_DOWNLOAD = 300_000


def install_source(relative_path, destination, source_dir=None, refresh=False):
    """Use local repo for CI, or fetch a bounded first-party file if not cached."""
    destination = Path(destination)
    if destination.exists() and not refresh:
        return destination
    if source_dir is not None:
        payload = (Path(source_dir) / relative_path).read_bytes()
    else:
        request = urllib.request.Request(
            RAW + relative_path, headers={"User-Agent": "PhantomLabsQuickOpen/1.0"})
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = response.read(MAX_DOWNLOAD + 1)
    if len(payload) > MAX_DOWNLOAD:
        raise ValueError("Remote file is larger than the safe download limit")
    if not payload:
        raise ValueError("Downloaded empty source file")
    if relative_path.endswith(".py"):
        compile(payload, relative_path, "exec")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=destination.parent, prefix=".quickopen-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
        os.replace(temp_path, destination)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    return destination


def newest_new_html(folder, before):
    after = {p.resolve() for p in folder.glob("*.html") if p.is_file()}
    new_files = after - before
    return max(new_files, key=lambda p: p.stat().st_mtime_ns) if new_files else None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Copy-paste-and-open Ubuntu launchers, no Git pull or shell exit")
    parser.add_argument("tool", choices=sorted(TOOLS))
    parser.add_argument("--seed", type=int, default=7831)
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--base", default="#FF1493")
    parser.add_argument("--stages", type=int, default=3, choices=(2, 3, 4))
    parser.add_argument("--message", default="The rose survived the static",
                        help="Cipherbox demo text (a shell argument is saved in shell history)")
    parser.add_argument("--message-file", help="Cipherbox local message file; avoids text in shell history")
    parser.add_argument("--domain", default="example.com", help="Public domain for Rosie Scan")
    parser.add_argument("--live", action="store_true", help="Explicitly enable live public-domain lookups")
    parser.add_argument("--passive-subdomains", action="store_true")
    parser.add_argument("--findomain", action="store_true")
    parser.add_argument("--whois-cli", action="store_true")
    parser.add_argument("--folder", help="Local folder to hash with Ghostmark; otherwise demo only")
    parser.add_argument("--baseline", help="GHOSTMARK previous report JSON")
    parser.add_argument("--refresh", action="store_true", help="Refresh cached source from GitHub")
    parser.add_argument("--source-dir", help=argparse.SUPPRESS)
    parser.add_argument("--workspace", default=str(Path.home() / "PhantomLabsLaunchers"))
    parser.add_argument("--no-browser", action="store_true", help="Useful for headless/offline tests")
    args = parser.parse_args(argv)
    if args.live and args.tool != "rosie-scan":
        parser.error("--live only applies to rosie-scan")
    if args.baseline and (args.tool != "ghostmark" or not args.folder):
        parser.error("--baseline requires ghostmark --folder")
    if args.message_file and args.tool != "cipherbox":
        parser.error("--message-file only applies to cipherbox")
    if args.live and args.domain == "example.com":
        # example.com is safe to use with --live, but require user to name it deliberately.
        print("[INFO] Running the bounded public example.com sample.")
    workspace = Path(args.workspace).expanduser()
    output = workspace / "reports" / args.tool
    output.mkdir(parents=True, exist_ok=True)
    filename = TOOLS[args.tool]
    try:
        source = install_source("tools/" + filename, workspace / "code" / filename,
                                args.source_dir, args.refresh)
        artwork = workspace / "artwork" / "rosie_header.png"
        if args.tool in ("rosie-scan", "ghostmark") and not artwork.exists():
            try:
                install_source("artwork/labface2.png", artwork, args.source_dir)
            except (OSError, ValueError, urllib.error.URLError) as exc:
                print("[INFO] Rosie artwork unavailable; rose header will still work:", exc)
        arguments = [sys.executable, str(source)]
        if args.tool == "hexwake":
            arguments += ["--seed", str(args.seed), "--count", str(args.count),
                          "--base", args.base, "--out", str(output)]
        elif args.tool == "cipherbox":
            if args.message_file:
                arguments += ["--message-file", args.message_file]
            else:
                arguments += ["--message", args.message]
            arguments += ["--seed", str(args.seed), "--stages", str(args.stages),
                          "--out", str(output)]
        elif args.tool == "rosie-scan":
            arguments += [args.domain, "--out", str(output), "--no-browser"]
            if not args.live:
                arguments += ["--offline"]
            else:
                if args.passive_subdomains:
                    arguments += ["--passive-subdomains"]
                if args.findomain:
                    arguments += ["--findomain"]
                if args.whois_cli:
                    arguments += ["--whois-cli"]
            if artwork.exists():
                arguments += ["--artwork", str(artwork)]
        else:
            arguments += ["--folder", args.folder] if args.folder else ["--demo"]
            if args.baseline:
                arguments += ["--baseline", args.baseline]
            arguments += ["--out", str(output), "--no-browser"]
            if artwork.exists():
                arguments += ["--artwork", str(artwork)]
        before = {p.resolve() for p in output.glob("*.html") if p.is_file()}
        print("[RUN]", args.tool, "| workspace:", workspace, flush=True)
        result = subprocess.run(arguments, check=False)
        if result.returncode:
            print("[ERROR] Tool failed with status", result.returncode, file=sys.stderr)
            return result.returncode
        page = newest_new_html(output, before)
        if not page:
            print("[ERROR] No new HTML gallery was generated.", file=sys.stderr)
            return 1
        print("[REPORT] Open this HTML file:", page, flush=True)
        if args.tool == "cipherbox":
            print("[PRIVACY] Never share the .answer.txt solution file.")
        if not args.no_browser:
            firefox = shutil.which("firefox")
            if firefox:
                try:
                    subprocess.Popen([firefox, str(page)],
                                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL, start_new_session=True)
                    print("[OPEN] Firefox launched with the new gallery.")
                except OSError as exc:
                    print("[INFO] Could not start Firefox:", exc)
            else:
                print("[INFO] Firefox not found; open the HTML file above in a browser.")
        return 0
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print("[ERROR]", exc, file=sys.stderr)
        print("[INFO] Existing files are preserved. Your terminal remains open.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
