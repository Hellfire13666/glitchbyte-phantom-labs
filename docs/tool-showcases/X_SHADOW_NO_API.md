<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🪞 GLITCHBYTEROSIE X SHADOW INTEL // NO-API TOOL SHOWCASE

<!-- GLITCHBYTE-ART-COVER:START -->

![X Shadow No-API | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/13_x_shadow_no_api.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · Public X research links + offline post analysis · No API token · JSON / CSV**

[🐍 Actual source](../../tools/glitchbyterosie_x_no_api.py) · [🕷️ Phantom Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> This is the **No-API** tool, distinct from the [official API-based X Intel Phantom](X_INTEL_PHANTOM.md). It generates X search URLs, can request basic public profile page metadata, and analyzes posts **you import locally**. It does not retrieve X posts by scraping a timeline or bypassing X access controls.

## 🌑 Source-grounded features

| Mode or CLI flag | Existing behavior |
| --- | --- |
| Menu 01 | Retrieve a public profile page's title and selected open-graph / Twitter card metadata; HTTP success does not prove the account exists |
| Menu 02 | Generate account, mentions, replies, reposts, media and other X research search links |
| Menu 03 | Generate keyword/hashtag X search links |
| Menu 04 | Import local CSV, JSON or JSONL posts and summarize hashtags, mentions, domains and frequent words |
| Menu 05 | Filter imported posts by keyword and date, then export analysis |
| Menu 06 | Combine the profile metadata request with public research links |
| `--import-file` | **Offline local post analysis**; optionally add `--filter`, `--start` and `--end` |
| `--username` | Generate account links **and request X profile metadata**; it is **not offline** |
| `--keyword` | Generate public search URLs **without contacting X**, when used alone |

The real script accepts `--username`, `--keyword`, `--import-file`, `--filter`, `--start`, and `--end`. There is **no `--mode`, `--out` or `--links-only` flag**. Without arguments, it opens an interactive menu.

Its optional public page request uses a 12-second timeout and reads at most 600,000 bytes of the response. Platform restrictions, redirects and login placeholders can make metadata misleading. The script **does not authenticate, collect cookies or pull account timelines**.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu / Linux Bash

**Install → Build → Test → Run → Find Reports → Troubleshoot.** Paste this entire block. Its first demonstration uses a **local CSV of invented sample posts**. The only internet access is the initial Git clone when needed; the analysis itself stays offline.

```bash
# PHANTOM LABS // X SHADOW INTEL (NO API) first-run recipe
set -e

# 1. INSTALL: Python 3 and Git (no pip packages or X token).
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/x-shadow-no-api-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/glitchbyterosie_x_no_api.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "A different folder already exists. Inspect it; nothing overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: the script uses only Python's standard library.
python3 --version

# 3. TEST: syntax and actual help (these do not contact X).
python3 -m py_compile glitchbyte-phantom-labs/tools/glitchbyterosie_x_no_api.py
python3 glitchbyte-phantom-labs/tools/glitchbyterosie_x_no_api.py --help

# 4. RUN: create harmless offline sample posts in your private workspace.
mkdir -p "$WORKSPACE/sample-input"
SAMPLE="$WORKSPACE/sample-input/demo_posts.csv"
if [ ! -e "$SAMPLE" ]; then
  printf '%s\n' \
    'username,date,text,url,likes,reposts,replies' \
    'demo_account,2026-10-10,"Hello #PhantomLabs check https://example.org",,3,1,0' \
    'demo_account,2026-10-11,"A second #PhantomLabs sample @example",,5,2,1' \
    > "$SAMPLE"
else
  echo "Preserving existing sample input: $SAMPLE"
fi

python3 glitchbyte-phantom-labs/tools/glitchbyterosie_x_no_api.py \
  --import-file "$SAMPLE" --filter PhantomLabs

# 5. FIND REPORTS: source uses a fixed directory under HOME.
REPORT_DIR="$HOME/glitchbyte_x_reports"
echo "Generated JSON and CSV reports:"
find "$REPORT_DIR" -maxdepth 1 -type f \
  \( -name 'posts_*.json' -o -name 'posts_*.csv' \) -print

# Verify any generated JSON without displaying or sharing personal data.
for FILE in "$REPORT_DIR"/posts_*.json; do
  if [ -f "$FILE" ]; then
    python3 -m json.tool "$FILE" >/dev/null
  fi
done
echo "JSON validation completed."
```

**Report naming:** Files are saved as `~/glitchbyte_x_reports/<prefix>_YYYYMMDD_HHMMSS.json`, with `.csv` created **only when the report includes a `posts` array**. For offline imported posts the prefix is `posts`; link-only and profile reports ordinarily write JSON only. The source currently has **no output-directory option**. Repeated runs using the same prefix within one second can replace reports.

## Use your own local exports

The offline analyzer reads CSV with a header row, a JSON array, a JSON object containing a `posts` or `data` array, or JSONL with one JSON object per line. You must lawfully obtain and review input yourself; this tool **doesn't download exports**.

```bash
python3 "$HOME/PhantomLabsBuilds/x-shadow-no-api-station/glitchbyte-phantom-labs/tools/glitchbyterosie_x_no_api.py" \
  --import-file "$HOME/path-to-your-own-posts.csv" \
  --filter "chosen phrase" \
  --start 2026-01-01 --end 2026-12-31
```

Replace the example path with your actual file. Date filters compare the first ten characters of each imported date string with the YYYY-MM-DD boundaries; this is **text comparison**, not strict timestamp parsing. Missing dates will not match when a date boundary is provided.

### Generate search links without X API access

To generate **keyword-only** public X search links without an X network request:

```bash
python3 "$HOME/PhantomLabsBuilds/x-shadow-no-api-station/glitchbyte-phantom-labs/tools/glitchbyterosie_x_no_api.py" \
  --keyword "Phantom Labs"
```

This creates a `research_*.json` links report under `~/glitchbyte_x_reports`. It **does not fetch matching X posts**. Supplying `--username` also performs a public profile metadata request, so do not assume that option is offline.

## 📊 Find and read saved results

```bash
find "$HOME/glitchbyte_x_reports" -type f \( -name '*.json' -o -name '*.csv' \)
python3 -m json.tool "/actual/path/to/posts_report.json" | less
head -n 10 "/actual/path/to/posts_report.csv"
```

These last two filenames are placeholders; use the **exact saved paths** printed by the application. The analyzer summarizes hashtag, mention, shared-domain, and word frequencies only from imported data; it does not verify authorship or external links.

## 🛠️ Troubleshooting

| Symptom | What to check |
| --- | --- |
| `python3` / `git` not installed | Install with your Linux distribution's package manager |
| `Import CSV, JSON or JSONL only` | Use a supported extension with a valid structure |
| `JSON must contain a list of posts` | Supply a list of post objects or a `posts`/`data` array |
| No CSV export | Link/profile-only modes normally emit JSON only |
| Profile metadata missing or blocked | X may restrict responses, redirect to login or require interactive access |
| Report missing | Check `~/glitchbyte_x_reports` and the terminal's `[SAVED]` path |
| Filters produce zero posts | Check case-insensitive keyword matching and YYYY-MM-DD date format |
| Same-second report overwritten | Preserve older exports under a different filename or directory before rerunning |
| No API token | Expected: this tool does not require one |
| `--mode` or `--out` unrecognized | Neither is an existing flag; use the documented options |

## 🧪 Verification, privacy and license

Commands, mode distinctions, file formats and paths were checked against [the actual Python source](../../tools/glitchbyterosie_x_no_api.py). This documentation update **has not run the full recipe on your Ubuntu machine**, nor sent a request to X. The fictitious sample posts are test data, not account findings.

Respect privacy and platform policies. Avoid publishing imports containing private individuals' information. Follow the repository's [security policy](../../SECURITY.md) and [custom source-available license](../../LICENSE-NOTICE.md).

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Homepage](../../README.md)
