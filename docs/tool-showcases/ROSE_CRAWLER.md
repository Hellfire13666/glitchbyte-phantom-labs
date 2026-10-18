<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹 ROSE CRAWLER // PHANTOM TOOL SHOWCASE

**Python 3 · Public social-profile link catalog · HTML, JSON and CSV reports · Standard library**

[Actual Python source](../../tools/rose_crawler.py) · [Phantom Tool Vault](../TOOL_VAULT.md) · [Starter guide](../TOOL_STARTER_GUIDE.md)

> **Twelve public platforms. One rose-lined evidence shelf.** Generated profile URLs are leads for manual review, not identity verification.

## What the existing tool does

ROSE CRAWLER supports **12 platforms**: GitHub, GitLab, Reddit, Mastodon.social, Bluesky, Pinterest, Tumblr, YouTube, TikTok, Instagram, X and Threads.

By default it **only generates profile URLs** and labels them `manual review` without contacting social platforms. With the optional `--fetch` flag it consults each platform's `robots.txt` and conditionally retrieves public HTML metadata, with a delay of at least two seconds before permitted profile requests. The tool prints a `[SCAN]` line and result for each platform as it finishes.

Its status labels are `manual review`, `restricted`, `uncertain`, `not found` and `reachable (unverified profile)`. An HTTP 200 response is **not evidence the named person owns an account**. Some platforms show login or placeholder pages.

Output formats are **searchable HTML, JSON and CSV**, all created together by the existing script. It is not a recursive crawler, authenticated account tool or a way to bypass robots restrictions.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

Six steps: **Install → Build → Test → Run → Find Results → Troubleshoot**.

This safe first run **never fetches social websites**. It uses a demonstration username and creates reports for candidate profile links only. Paste this entire block into a Bash terminal:

```bash
# PHANTOM LABS // ROSE CRAWLER first-run recipe
set -e

# 1. INSTALL: Python 3 and Git. No pip installs required.
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git required."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/rose-crawler-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

if [ ! -f glitchbyte-phantom-labs/tools/rose_crawler.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Unexpected existing folder. Inspect it; nothing overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: Python script, no compilation step.
python3 --version

# 3. TEST: syntax, help and list of supported platforms.
python3 -m py_compile glitchbyte-phantom-labs/tools/rose_crawler.py
python3 glitchbyte-phantom-labs/tools/rose_crawler.py --help
python3 glitchbyte-phantom-labs/tools/rose_crawler.py --list

# 4. RUN: generate offline candidate links for a fictional demo handle.
mkdir -p "$WORKSPACE/reports"
python3 glitchbyte-phantom-labs/tools/rose_crawler.py \
  phantomlabdemo --output "$WORKSPACE/reports"

# 5. FIND RESULTS: locate generated HTML, JSON and CSV files.
echo "Report folder: $WORKSPACE/reports"
find "$WORKSPACE/reports" -maxdepth 1 -type f \
  \( -name '*.html' -o -name '*.json' -o -name '*.csv' \) -print

# Display a sample of the first JSON file, if available.
REPORT=$(find "$WORKSPACE/reports" -maxdepth 1 -type f \
  -name '*.json' -print -quit)
if [ -n "$REPORT" ]; then
  python3 -m json.tool "$REPORT" | head -n 35
fi

echo "To open the HTML report on a Linux desktop:"
echo 'xdg-open "/actual/path/to/your/rose_report.html"'
```

**Important:** This does **not** verify or query the fictional demonstration handle. Do not treat its twelve URL rows as evidence that any account exists.

## Run with your own username

Use a public handle you have a legitimate reason to research. Run from any directory, using the actual Python source path:

```bash
python3 "$HOME/PhantomLabsBuilds/rose-crawler-station/glitchbyte-phantom-labs/tools/rose_crawler.py" \
  YOUR_PUBLIC_HANDLE \
  --platforms GitHub,GitLab,Reddit \
  --output "$HOME/PhantomLabsBuilds/rose-crawler-station/reports"
```

The command above is **offline**, since it omits `--fetch`. After reviewing platform conditions and your authorization, an optional network request mode is:

```bash
python3 "$HOME/PhantomLabsBuilds/rose-crawler-station/glitchbyte-phantom-labs/tools/rose_crawler.py" \
  YOUR_PUBLIC_HANDLE \
  --fetch --delay 3 \
  --platforms GitHub,GitLab \
  --output "$HOME/PhantomLabsBuilds/rose-crawler-station/reports"
```

Use `--list` for the exact platform spellings. The `--delay` minimum is **2 seconds** and the default is **2.5 seconds**. A robots.txt failure generally results in a restricted status rather than a profile fetch. A website's response or redirects can still produce uncertain results.

## 📊 Find and open results

The source constructs the filename as `rose_<username>_<YYYYMMDD_HHMMSS_microseconds>_<random-suffix>` and saves matching `.html`, `.json`, and `.csv` files under the directory supplied by `--output` (default: `~/RoseCrawlerReports`).

```bash
find "$HOME/PhantomLabsBuilds/rose-crawler-station/reports" -type f \
  \( -name '*.html' -o -name '*.json' -o -name '*.csv' \)
```

Use your **actual reported filename**:

```bash
python3 -m json.tool "/actual/path/to/rose_report.json" | less
xdg-open "/actual/path/to/rose_report.html"
head -n 10 "/actual/path/to/rose_report.csv"
```

The filename strings above are examples, not files known to exist on your machine. The HTML dashboard includes a text filter. Reports may contain publicly visible descriptions and URLs, which still deserve careful handling.

**Phase 25 reliability fix:** Filenames preserve periods in usernames and use microsecond timestamps plus a randomized suffix to avoid overwriting earlier reports. Use `find` to locate actual filenames; the CLI and generated HTML/JSON/CSV contents remain unchanged.

## 🛠️ Troubleshoot

| Situation | Practical check |
| --- | --- |
| `python3` or `git` missing | Install the package using your Linux distribution's package manager |
| `username must be 1-40 characters` | Use only letters, numbers, `_`, `.`, `-` |
| Unknown platform selected | Run `--list`, then use comma-separated exact platform names |
| `--delay must be at least 2 seconds` | Use 2 or greater |
| Report directory empty | Check permissions, `--output` and the final terminal `Saved:` line |
| Robots blocked/unavailable | Respect the restriction; do not force a fetch |
| `reachable (unverified profile)` | It is not confirmed identity or even proof of a valid profile |
| HTML fails to open | Use a desktop with `xdg-open` or inspect JSON/CSV locally |
| `BrokenPipeError` while piping JSON to `head` | Re-run `python3 -m json.tool` directly without piping, or open the JSON in an editor |

## 🧪 Review and safety notes

The flags, platform list, report formats and behavior above were inspected in [the current source](../../tools/rose_crawler.py). The full Bash recipe has **not been run end-to-end in your Ubuntu environment**, and no social website was queried as part of this documentation update. A syntax check is recommended; it is not proof that a live profile fetch will work.

Phase 25 changes only the report filename construction in the original source; platform research logic is unchanged. Respect platforms, privacy and the repository's [SECURITY.md](../../SECURITY.md) and [LICENSE-NOTICE.md](../../LICENSE-NOTICE.md). Do not commit sensitive reports or use a matching username to make identity accusations.

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Official homepage](../../README.md)
