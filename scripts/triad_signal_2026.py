#!/usr/bin/env python3
"""GlitchByte Phantom Labs TRIAD SIGNAL: bounded, passive, installed-tool companion.

Noninteractive Python 3 standard-library companion to the original local
Triad Forge installers. It does not install tools or modify the workshop ZIP.
Results come only from real installed CLI output. Amass itself may write
its own cache/database; the companion never asks for a report unless -o/--o.
"""
import argparse
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from urllib.parse import urlsplit

NAME = "TRIAD SIGNAL // PHANTOM LABS"
MODULES = ("amass", "gau", "waybackurls")
MAX_PER_MODULE = 2500
DOMAIN = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$")
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def normalize(line, target):
    text = ANSI.sub("", line.strip())
    if not text or len(text) > 2048:
        return None
    if text.lower().startswith(("https://", "http://")):
        try:
            url = urlsplit(text)
            host = (url.hostname or "").lower().rstrip(".")
        except ValueError:
            return None
        if url.username or not (host == target or host.endswith("." + target)):
            return None
        return text
    host = text.lower().rstrip(".")
    if DOMAIN.fullmatch(host) and (host == target or host.endswith("." + target)):
        return host
    return None


def command_for(module, target):
    if module == "amass":
        return ["amass", "enum", "-passive", "-d", target]
    if module == "gau":
        # A single provider reduces time spent on multiple slow external APIs.
        return ["gau", "--providers", "wayback", "--threads", "2",
                "--timeout", "8", "--retries", "0", target]
    if module == "waybackurls":
        return ["waybackurls", target]
    raise ValueError(f"Unknown module {module}")


def terminate_group(proc):
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        try:
            proc.terminate()
        except ProcessLookupError:
            pass
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            try:
                proc.kill()
            except ProcessLookupError:
                pass
        proc.wait()


def probe(module, target, seconds, max_show, emit):
    binary = shutil.which(module)
    started = time.monotonic()
    if binary is None:
        emit(f"[{module.upper()}][MISSING] Executable not found in PATH")
        return {"module": module, "status": "missing", "count": 0,
                "seconds": 0.0, "results": []}
    args = command_for(module, target)
    args[0] = binary
    emit(f"[{module.upper()}][START] Public sources, {seconds}s limit")
    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                text=True, encoding="utf-8", errors="replace",
                                bufsize=1, start_new_session=True)
    except OSError as exc:
        emit(f"[{module.upper()}][ERROR] Could not start: {exc}")
        return {"module": module, "status": "failed", "count": 0,
                "seconds": round(time.monotonic() - started, 2), "results": []}

    found = set()
    notices = set()

    def reader():
        for raw in proc.stdout:
            result = normalize(raw, target)
            if result is not None:
                if len(found) < MAX_PER_MODULE and result not in found:
                    found.add(result)
                    if len(found) <= max_show:
                        emit(f"[{module.upper()}][FOUND] {result}")
            else:
                message = ANSI.sub("", raw.strip()).replace("\x00", "")
                if message and message not in notices and len(notices) < 3:
                    notices.add(message)
                    emit(f"[{module.upper()}][NOTICE] {message[:170]}")
        proc.stdout.close()

    worker = threading.Thread(target=reader, daemon=True)
    worker.start()
    timed_out = False
    try:
        proc.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        terminate_group(proc)
    worker.join(timeout=3)
    elapsed = round(time.monotonic() - started, 2)

    if timed_out:
        status = "partial-timeout" if found else "timeout"
    elif proc.returncode == 0:
        status = "complete" if found else "complete-no-results"
    else:
        status = "partial-exit" if found else f"failed-exit-{proc.returncode}"

    emit(f"[{module.upper()}][{status.upper()}] "
         f"{len(found)} real candidates | {elapsed}s"
         + (f" | {max(0, len(found)-max_show)} more hidden" if len(found) > max_show else ""))
    return {"module": module, "status": status, "count": len(found),
            "seconds": elapsed, "results": sorted(found)}


def run(argv=None):
    parser = argparse.ArgumentParser(description=NAME + " | passive CLI-only integration")
    parser.add_argument("domain", nargs="?", default="example.com")
    parser.add_argument("--only", choices=MODULES, help="Check one specific Triad module")
    parser.add_argument("--amass-seconds", type=int, default=55)
    parser.add_argument("--gau-seconds", type=int, default=35)
    parser.add_argument("--wayback-seconds", type=int, default=25)
    parser.add_argument("--max-show", type=int, default=15,
                        help="Max printed candidates per module (all returned candidates counted)")
    parser.add_argument("-o", "--o", dest="output", metavar="NAME.txt",
                        help="Save deduplicated public-source hostname/URL candidates")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto")
    args = parser.parse_args(argv)
    target = args.domain.strip().lower().rstrip(".")
    if not DOMAIN.fullmatch(target):
        parser.error("Supply a DNS domain, for example example.com")
    for name in ("amass_seconds", "gau_seconds", "wayback_seconds"):
        if not 5 <= getattr(args, name) <= 120:
            parser.error(f"--{name.replace('_','-')} must be 5 to 120 seconds")
    if not 1 <= args.max_show <= 100:
        parser.error("--max-show must be 1 to 100")
    output = Path(args.output).expanduser() if args.output else None
    if output:
        if output.suffix.lower() != ".txt" or not output.parent.is_dir():
            parser.error("-o / --o requires a .txt filename in an existing directory")
        if output.exists():
            parser.error(f"Output exists and will not be overwritten: {output}")

    enabled = args.color == "always" or (args.color == "auto" and sys.stdout.isatty())
    colors = {"[START]": "\x1b[95m", "[FOUND]": "\x1b[92m",
              "[NOTICE]": "\x1b[93m", "[WAIT]": "\x1b[96m",
              "[COMPLETE]": "\x1b[92m", "[TIMEOUT]": "\x1b[93m"}
    lock = threading.Lock()

    def emit(message):
        label = next((x for x in colors if x in message), "")
        color = colors.get(label, "")
        with lock:
            print((color + message + "\x1b[0m") if enabled and color else message, flush=True)

    chosen = [args.only] if args.only else list(MODULES)
    limits = {"amass": args.amass_seconds, "gau": args.gau_seconds,
              "waybackurls": args.wayback_seconds}
    emit(f"[START] {NAME} :: {target} :: passive source observations")
    emit(f"[START] Independent caps: " + ", ".join(
         f"{module} {limits[module]}s" for module in chosen))
    emit("[START] Save: " + str(output) if output else "[START] Save OFF: no companion output file")

    completed = {}
    finish = threading.Event()

    def execute(module):
        completed[module] = probe(module, target, limits[module], args.max_show, emit)

    workers = [threading.Thread(target=execute, args=(module,), daemon=True)
               for module in chosen]
    try:
        for thread in workers:
            thread.start()
        while any(thread.is_alive() for thread in workers):
            finish.wait(timeout=5)
            running = [chosen[i] for i, thread in enumerate(workers) if thread.is_alive()]
            if running:
                emit("[WAIT] Still checking: " + ", ".join(running))
        for thread in workers:
            thread.join()
    except KeyboardInterrupt:
        emit("[INTERRUPTED] Ctrl+C received. Child processes should be stopped.")
        # Workers are daemon threads. New run handles its per-command timeout;
        # do not claim interruption produced a complete report.
        return 130

    all_results = sorted({entry for result in completed.values()
                          for entry in result["results"]})
    for module in chosen:
        result = completed[module]
        emit(f"[SUMMARY] {module}: {result['status']} / {result['count']} candidates")
    emit(f"[SUMMARY] {len(all_results)} unique candidate hostnames/URLs across {len(chosen)} tools")
    if output:
        try:
            with output.open("x", encoding="utf-8") as handle:
                handle.write("\n".join(all_results) + ("\n" if all_results else ""))
            emit(f"[SAVED] TXT {output} | {len(all_results)} candidate lines")
        except OSError as exc:
            emit(f"[ERROR] Could not save TXT: {exc}")
            return 2
    else:
        emit("[DONE] No companion report saved")
    emit("[DONE] Candidates are historical/public observations, not proof of active websites")
    return 0 if all(completed[x]["status"].startswith("complete") for x in chosen) else 1


if __name__ == "__main__":
    raise SystemExit(run())
