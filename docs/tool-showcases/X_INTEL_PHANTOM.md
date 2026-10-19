<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🛰️ GLITCHBYTEROSIE X INTEL PHANTOM // TOOL SHOWCASE

<!-- GLITCHBYTE-ART-COVER:START -->

![X Intel Phantom | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/12_x_intel_phantom.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3.9+ · Official X API v2 · Public account/post research · JSON + CSV exports**

[🐍 Original Python source](../../tools/glitchbyterosie_x_intel.py) · [🕷️ Phantom Tool Vault](../TOOL_VAULT.md) · [📚 Tool Starter Guide](../TOOL_STARTER_GUIDE.md)

> A source-grounded guide to the **official API** version. This is a separate tool from `glitchbyterosie_x_no_api.py`; the latter requires its **own** independent showcase.

## What it really does

The existing `glitchbyterosie_x_intel.py` supports **16 menu choices**, including account profile/stats, recent posts, replies, reposts/quotes, keyword and hashtag search, mentions, date-range search, shared URLs, engagement, media references, follower/following results where permitted, and custom search/export.

It calls `https://api.x.com/2` using an `X_BEARER_TOKEN` supplied by **you** via the environment. API availability, pricing, search history, and rate limits depend on your developer account's current access. Its account and search routines request up to **10 pages** (`--pages`, up to 100 requested records per page), but the actual number returned may be smaller.

**Important accuracy notes:**
- Modes 4 and 5 fetch authored posts and **filter** the returned results for replies and reposts/quotes; do not interpret them as guaranteed exhaustive account histories.
- Modes 10–13 and 15 reuse fetched posts and compute or display derived fields; some summaries are not independently queried API endpoints.
- 401/403/429 errors can reflect access tiers, authentication, rate limits or platform changes.
- A post/username match is **not** proof of real-world identity or misconduct.
- The source prints per-page `[SCAN]` progress and waits 15 seconds before one retry after an initial HTTP 429. It does not offer a free unlimited or guaranteed full-archive scan.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

**Install → Build → Test → Run → Find Results → Troubleshoot.**

The first recipe checks local prerequisites, checks Python syntax and shows CLI help. **It makes no X API requests and never needs a token.** It does contact GitHub if the repository must be cloned. Paste this entire block into a Bash terminal:

```bash
# PHANTOM LABS // X INTEL PHANTOM (SAFE FIRST RUN)
set -e

# 1. INSTALL: Python 3.9+ and Git, no third-party Python packages.
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3.9+ first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }
WORKSPACE="$HOME/PhantomLabsBuilds/x-intel-phantom-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

if [ ! -f glitchbyte-phantom-labs/tools/glitchbyterosie_x_intel.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Existing folder is not the expected tool checkout. Inspect it; not overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: interpreted Python; no compiler or pip install required.
python3 --version

# 3. TEST: offline syntax and available flags.
python3 -m py_compile glitchbyte-phantom-labs/tools/glitchbyterosie_x_intel.py
python3 glitchbyte-phantom-labs/tools/glitchbyterosie_x_intel.py --help

# 4. RUN: optional authenticated API use is in the next block.
echo "No X API call made. Follow the separate opt-in recipe below if you have access."

# 5. FIND RESULTS: future exports can be saved in this private workspace.
mkdir -p "$WORKSPACE/reports"
find "$WORKSPACE/reports" -type f \( -name '*.json' -o -name '*.csv' \) -print
echo "Report directory: $WORKSPACE/reports"
```

### Optional X API run with **your own authorized credentials**

This second block is **not free or guaranteed to work** without developer access for the selected API endpoint. It prompts privately for your own X bearer token rather than putting the secret in the command itself. Run only when you are entitled to use that endpoint. Replace the sample handle with a public handle you own or are authorized to research.

```bash
# Run in Bash after completing the safe setup block above.
set -e
WORKSPACE="$HOME/PhantomLabsBuilds/x-intel-phantom-station"
cd "$WORKSPACE"
read -r -s -p "X developer bearer token (input hidden): " X_BEARER_TOKEN
printf '\n'
if [ -z "$X_BEARER_TOKEN" ]; then
  echo "No token given; no API request made."
else
  export X_BEARER_TOKEN
  python3 glitchbyte-phantom-labs/tools/glitchbyterosie_x_intel.py \
    --username YOUR_OWN_PUBLIC_HANDLE \
    --mode 1 --pages 1 \
    --output "$WORKSPACE/reports"
  unset X_BEARER_TOKEN
fi
```

**Security:** Do not paste your bearer token into GitHub, commit it in a file, place it in a URL, or share terminal screenshots with credentials. The token is held in the current shell environment only for this optional run. `unset` is reached when the command completes successfully; if it fails under `set -e`, explicitly type `unset X_BEARER_TOKEN` before continuing. Review shell access and process environments on shared machines.

## 🛰️ Actual flags and other supported examples

| Flag | Meaning |
| --- | --- |
| `--username` | X account handle |
| `--query` | X search query |
| `--mode` | Select menu 1–16 (see source for implementation) |
| `--pages` | Request 1–10 pages; defaults to 1 |
| `--start`, `--end` | Search range (YYYY-MM-DD or ISO timestamp) |
| `--archive` | Full-archive search endpoint; requires suitable API access |
| `--output` | Export directory; default is `glitchbyte_reports` relative to current directory |

For authorized search access, mode 6 selects a keyword search:

```bash
python3 glitchbyte-phantom-labs/tools/glitchbyterosie_x_intel.py \
  --mode 6 --query "your research keyword" --pages 1 \
  --output "$HOME/PhantomLabsBuilds/x-intel-phantom-station/reports"
```

The above **requires** `X_BEARER_TOKEN` to be set beforehand and proper search endpoint access. Without a token, the CLI exits with a setup message instead of making API calls.

## 📊 Saved report recipe

A completed API request writes **one JSON file and one CSV file** with names resembling:

```text
glitchbyte_<label>_YYYYMMDD_HHMMSS.json
glitchbyte_<label>_YYYYMMDD_HHMMSS.csv
```

`<label>` is derived from the handle or search term, sanitized for filenames. If two runs have the same label within the same second, their outputs may overwrite each other. Preserve earlier output in a separate directory if necessary.

```bash
find "$HOME/PhantomLabsBuilds/x-intel-phantom-station/reports" -type f \
  \( -name '*.json' -o -name '*.csv' \)
# Replace the placeholder with the exact file path printed by [SAVED].
python3 -m json.tool "/actual/path/to/report.json" | less
head -n 10 "/actual/path/to/report.csv"
```

The JSON export includes collection metadata and API result data; the CSV lists a subset of post fields. Modes returning profiles or relationships without post records can produce a CSV with only headers. The script does not produce an HTML dashboard.

## 🛠️ Troubleshooting

| Symptom | Check |
| --- | --- |
| Python/Git not installed | Install Python 3.9+ and Git |
| `[SETUP] Set X_BEARER_TOKEN` | Add your own developer credential in the optional private prompt; do not post it |
| HTTP 401 or 403 | Credential invalid, insufficient API tier, or endpoint not granted |
| HTTP 429 | Rate limited: respect cooldown and access terms; the program retries once |
| API search returns few/no posts | Access tier, date windows, platform indexing and API filtering vary |
| CSV appears empty except header | Some modes return profiles or relationships, not post records |
| No output created | Check `--output`, read the exception, and verify request completed successfully |
| Sensitive data in report | Keep exports private; never commit bearer tokens or unreviewed research output |

## 🧪 Verification and ownership

All flags, API endpoints, pagination, saved formats and token requirements were verified by **reading** [the current Python source](../../tools/glitchbyterosie_x_intel.py). The complete copy/paste commands have **not** been executed on the user's Ubuntu system, and **no live X API request** was made during this documentation update.

Follow the [security policy](../../SECURITY.md), the [custom source-available license](../../LICENSE-NOTICE.md), developer platform terms and applicable privacy law.

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Homepage](../../README.md)

## 💾 Easy Save: `-o name.txt` or `--o name.txt`

First install the shared [Phantom Easy Save runner](../EASY_SAVE_ALL_TOOLS.md). It saves what this existing tool **prints in the terminal**, not its hidden data or structured files. Both `-o` and `--o` work **on the runner** before the `--` separator:

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
# From your HQ repository checkout root:
python3 "$SAVER" --o x_intel_phantom_help.txt -- python3 -u tools/glitchbyterosie_x_intel.py --help
```

This non-network first test saves **help text**, not research results. Replace the `--help` after the separator with the real run arguments documented elsewhere on this page to save actual printed outcomes. Choose a new output filename each time, because it won't overwrite an existing file. **Legacy exports are unchanged**: the wrapper doesn't disable this tool's own HTML/JSON/CSV/report saving, supply browser interfaces, or produce a clean structured export. For interactive tools or graphics prefer their native options. Future builds implement native `-o` / `--o` when appropriate.

