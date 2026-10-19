<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🦋 ROSIEGLITCHBYTE HACKGIRL INTEL // TOOL SHOWCASE

<!-- GLITCHBYTE-ART-COVER:START -->

![HackGirl Intel | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/14_hackgirl_intel.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · No X API key · Offline CSV/JSON post analysis · HTML and JSON reports**

[🐍 Actual source](../../tools/rosieglitchbyte_hackgirl.py) · [🕷️ Phantom Tool Vault](../TOOL_VAULT.md) · [📚 Starter Guide](../TOOL_STARTER_GUIDE.md)

> A neon research desk for material you already possess. This is a **separate program** from [X Shadow No-API](X_SHADOW_NO_API.md) and [X Intel Phantom (official API)](X_INTEL_PHANTOM.md). A shared handle, web response or downloaded sample is not proof of account ownership.

## What the current tool really does

The existing script has these real command-line flags:

| Flag | Behavior |
| --- | --- |
| `--sample` | Writes `~/RosieGlitchbyte_Intel/sample_posts.csv` with demonstration records; **overwrites that exact file** |
| `--import-file PATH` | Imports local CSV or JSON posts, analyzes hashtags, mentions, URLs/domains, words and authors; writes JSON |
| `--filter TEXT` | Limits an imported analysis to posts containing the text, case-insensitively |
| `--html` | With `--import-file`, also writes a standalone HTML dashboard (up to 300 displayed imported posts) |
| `--keyword TEXT` | Creates X/Google research links, **without contacting those sites** |
| `--username HANDLE` | **Does** request public X profile page metadata, and also writes research links |

With no flags, a nine-option **interactive** menu provides imports, optional CSV export, dashboard creation, a sample generator, and link research. The tool can read CSV or JSON imports of at most **20 MB**, takes the first **10,000** post records, and may limit display of dashboard posts to 300. It does not scrape posts, retrieve timelines or bypass X access restrictions.

`--username` makes a public X request with a 12-second timeout and at most 400 KB of the returned page; a 200 status is not verified account existence or identity. For a safe first run, use a **local sample CSV**, without `--username`.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu / Linux Bash

**Install → Build → Test → Run → Find / Read Reports → Troubleshoot**

The one-block first run below checks the actual source, builds a **unique demonstration CSV without overwriting the source's fixed sample file**, analyzes it offline, creates both JSON and HTML, and verifies the report. Apart from cloning the repository from GitHub if necessary, the run makes **no network requests**.

```bash
# PHANTOM LABS // HACKGIRL INTEL first-run recipe
set -e

# 1. INSTALL: Python 3 and Git. No pip requirements.
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/hackgirl-intel-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/rosieglitchbyte_hackgirl.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "An unexpected folder exists. Inspect it; nothing was overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
SCRIPT="$WORKSPACE/glitchbyte-phantom-labs/tools/rosieglitchbyte_hackgirl.py"

# 2. BUILD: interpreted Python 3, no compiler or API token.
python3 --version

# 3. TEST: source syntax and actual command-line options.
python3 - "$SCRIPT" <<'PY'
import pathlib, sys
source = pathlib.Path(sys.argv[1])
compile(source.read_bytes(), str(source), "exec")
print("PASS: HackGirl Intel Python syntax")
PY
python3 "$SCRIPT" --help

# 4. RUN: locally generated, fictional sample posts (offline).
mkdir -p "$WORKSPACE/sample-input"
SAMPLE=$(mktemp "$WORKSPACE/sample-input/hackgirl_demo_XXXXXXXX.csv")
printf '%s\n' \
  'date,username,text,url,likes,reposts,replies,quotes' \
  '2026-10-10,fictional_demo,"Neon signal #PhantomLabs https://example.org",,2,0,0,0' \
  '2026-10-11,fictional_demo,"Hello @ImaginaryAccount #PhantomLabs",,3,1,0,0' \
  > "$SAMPLE"
python3 "$SCRIPT" --import-file "$SAMPLE" --filter PhantomLabs --html

# 5. FIND / READ: the source writes under a fixed HOME directory.
REPORT_DIR="$HOME/RosieGlitchbyte_Intel"
echo "JSON and HTML reports:"
find "$REPORT_DIR" -maxdepth 1 -type f \
  \( -name 'post_analysis_*.json' -o -name 'dashboard_*.html' \) -print

# Verify the generated analysis without assuming a specific timestamp.
LATEST=$(find "$REPORT_DIR" -maxdepth 1 -type f -name 'post_analysis_*.json' \
  -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)
python3 - "$LATEST" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1])
data = json.loads(p.read_text(encoding="utf-8"))
assert "posts" in data and "count" in data
print("PASS: JSON report readable; imported posts:", data["count"])
print("Read report:", p)
PY

echo "To open an HTML dashboard on Linux, use xdg-open with its exact file path."
```

### Report locations and filenames

The original script writes to **`~/RosieGlitchbyte_Intel/`**, with timestamped filenames. `--import-file` creates `post_analysis_YYYYMMDD_HHMMSS.json`; `--html` also creates `dashboard_YYYYMMDD_HHMMSS.html`. The default command-line import mode does **not** automatically export CSV; the interactive menu's export function creates `posts_export_YYYYMMDD_HHMMSS.csv` when selected.

The current tool has **no `--output` or `--out` parameter**. Its report timestamps have one-second resolution. Rerunning the same output type within one second may replace an earlier file. Copy important reports elsewhere before rerunning.

```bash
find "$HOME/RosieGlitchbyte_Intel" -type f \
  \( -name '*.json' -o -name '*.html' -o -name '*.csv' \)
python3 -m json.tool "/actual/path/to/post_analysis_REPORT.json" | less
xdg-open "/actual/path/to/dashboard_REPORT.html"
```

Replace example paths with filenames found by `find`. `xdg-open` requires a desktop session; on a headless server, inspect JSON or transfer the HTML privately.

## Optional real-data and public-link commands

Import an **existing, lawfully obtained** file (replace the placeholder):

```bash
python3 "$HOME/PhantomLabsBuilds/hackgirl-intel-station/glitchbyte-phantom-labs/tools/rosieglitchbyte_hackgirl.py" \
  --import-file "$HOME/path-to-your-post-archive.csv" \
  --filter "chosen keyword" --html
```

Generate keyword search links without fetching X or Google:

```bash
python3 "$HOME/PhantomLabsBuilds/hackgirl-intel-station/glitchbyte-phantom-labs/tools/rosieglitchbyte_hackgirl.py" \
  --keyword "Phantom Labs"
```

The `--username` mode **fetches X profile metadata** and can yield a login page or rate-limit response rather than real profile details. Only use it for permitted public research; no private-account contents, login sessions or X post histories are obtained.

## 🛠️ Troubleshooting

| Symptom | Check |
| --- | --- |
| Python 3 / Git missing | Install from your Linux package manager |
| Repository folder exists but source missing | Inspect its contents; recipe refuses to overwrite |
| `File missing or larger than 20 MB` | Check import path, existence and size |
| `Use a CSV or JSON file` | JSONL is **not** supported by this particular script |
| `Expected a list of posts` | JSON must contain a list, or an object with a `posts` list |
| No HTML output | Add `--html` together with `--import-file` |
| No CSV output from CLI import | CSV export is a separate interactive menu feature |
| Report missing | Check `~/RosieGlitchbyte_Intel` and the printed `[SAVED]` path |
| `--sample` changed an existing CSV | That built-in option overwrites `sample_posts.csv`; use the safer unique sample recipe above |
| Profile result inconclusive | An HTTP response isn't evidence of a valid account or an identity link |
| HTML won't open on server | Use JSON or move HTML privately to a graphical browser |

## 🧪 Verification and safety

The flags, output paths, local data handling, sample overwrite behavior and live metadata distinctions were established by inspecting [the original source](../../tools/rosieglitchbyte_hackgirl.py). The complete Bash recipe **has not yet been executed end to end on your Ubuntu system**. The recipe's validation commands run *when you paste them*, and no live account was queried in preparing this documentation.

Imported post content and public descriptions can still include personal information. Do not post raw research reports without reviewing them. Follow [SECURITY.md](../../SECURITY.md) and the repository's [custom source-available license](../../LICENSE-NOTICE.md).

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Official homepage](../../README.md)
