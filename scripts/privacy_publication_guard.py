"""Check tracked publication files for accidentally embedded workstation paths.

This is a preventive working-tree check, not a historical secret scanner.
It prints relative file names and line numbers only; never the matched text.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = re.compile(r"(?<![A-Za-z0-9])/(?:home|Users)/([A-Za-z0-9_.-]+)/")
SECRETS = re.compile(r"(?<![A-Za-z0-9_])(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})")
SAFE_NAMES = {"example", "runner", "yourname", "username", "user", "testuser", "demo"}
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".zip", ".gz", ".pdf", ".woff", ".ttf", ".mp4"}
MAX_BYTES = 2_000_000

def tracked():
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        capture_output=True, check=True,
    )
    return [ROOT / p.decode("utf-8", "surrogateescape")
            for p in result.stdout.split(b"\0") if p]

def inspect(content):
    for number, line in enumerate(content.splitlines(), 1):
        if SECRETS.search(line):
            yield number, "possible credential"
        elif any(m.group(1).lower() not in SAFE_NAMES
                 for m in HOME.finditer(line)):
            yield number, "non-example workstation path"

def main():
    errors = 0
    for path in tracked():
        if not path.is_file() or path.suffix.lower() in SKIP_EXTS:
            continue
        if path.stat().st_size > MAX_BYTES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line, category in inspect(content):
            print(f"[REVIEW] {path.relative_to(ROOT)}:{line}: {category}")
            errors += 1
    if errors:
        print(f"[FAIL] {errors} possible exposures; review before publishing")
        return 1
    print("[PASS] No matching workstation paths or token-shaped strings in tracked text files")
    print("[NOTE] Not a full history scan or secrets audit")
    return 0

if __name__ == "__main__":
    sys.exit(main())
