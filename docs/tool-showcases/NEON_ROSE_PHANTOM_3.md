<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌺 NEON ROSE PHANTOM 3.0 // TOOL SHOWCASE

<!-- GLITCHBYTE-ART-COVER:START -->

![Neon Rose Phantom 3.0 | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/05_neon_rose_phantom_3.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · Single-domain public research · Eight modes · Timestamped JSON · Standard library**

[🐍 Original source](../../tools/rosieglitchbyte_neon_rose_phantom_3.py) · [🕷️ Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> The neon rose watches public website signals without claiming to find hidden people, vulnerabilities or private information. This is its **own** version 3.0 tool, separate from [Domain Phantom 2.0](DOMAIN_PHANTOM.md).

## Modes verified in the actual code

| `--mode` | Function | Network request? |
| --- | --- | --- |
| `1` | Resolve DNS/IP addresses and check whether all results are globally routable | Yes, DNS |
| `2` | Retrieve title, description, headings and headers from one HTTPS homepage | Yes |
| `3` | Extract up to 100 distinct homepage links, without crawling pages | Yes |
| `4` | Check six HTTP security-header names | Yes |
| `5` | Inspect HTTPS certificate, with system trust and hostname validation | Yes |
| `6` | Read a limited `robots.txt` preview | Yes |
| `7` | **Generate** a public RDAP research URL; no RDAP lookup is fetched | **No** |
| `8` | Run modes 1–7 and archive results | Yes, for most modes |

The tool offers `--no-animation` and an optional positional domain, and saves a JSON report after selected modules. It deliberately **does not follow HTTP redirects** for its page-fetch helper. Individual operations use an eight-second timeout, and the default homepage body limit is 450 KB. This is not a full crawler, vulnerability scan, or guarantee of network isolation. DNS can change between a public-address check and connection.

The source has **no `--output`, `--out`, `--json` or CSV/HTML export flags**. Do not copy command examples from the other Domain Phantom tools without checking their version-specific report paths.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu / Linux Bash

**Install → Build → Test → Run → Find / Read Results → Troubleshoot.**

Paste the entire block. It safely checks syntax and runs **mode 7** for the documentation domain `example.org`. This mode **only generates a URL**, without querying the domain, RDAP service, DNS or TLS. An initial repository clone, if needed, does contact GitHub.

```bash
# PHANTOM LABS // NEON ROSE PHANTOM 3.0
set -e

# 1. INSTALL: Python 3 and Git, no pip dependencies.
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/neon-rose-phantom-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

if [ ! -f glitchbyte-phantom-labs/tools/rosieglitchbyte_neon_rose_phantom_3.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "An existing directory is missing the tool. Inspect it; nothing overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

SCRIPT="$WORKSPACE/glitchbyte-phantom-labs/tools/rosieglitchbyte_neon_rose_phantom_3.py"

# 2. BUILD: standalone interpreted Python script.
python3 --version

# 3. TEST: syntax validation and actual CLI help, both offline.
python3 - "$SCRIPT" <<'PY'
import pathlib, sys
source = pathlib.Path(sys.argv[1])
compile(source.read_bytes(), str(source), "exec")
print("PASS: Neon Rose Phantom Python syntax")
PY
python3 "$SCRIPT" --help

# 4. RUN: offline RDAP-link generation only, not a site scan.
python3 "$SCRIPT" example.org --mode 7 --no-animation

# 5. FIND REPORTS: this tool uses a fixed directory in your home folder.
REPORT_DIR="$HOME/RosieGlitchByte_Neon_Rose_Reports"
echo "Report folder: $REPORT_DIR"
find "$REPORT_DIR" -maxdepth 1 -type f -name 'example_org_*.json' -print

# Validate the newest matching JSON report and mode name.
LATEST=$(find "$REPORT_DIR" -maxdepth 1 -type f -name 'example_org_*.json' \
  -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)
python3 - "$LATEST" <<'PY'
import json, pathlib, sys
report = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
assert report["domain"] == "example.org"
assert "RDAP research link" in report["modules"]
print("PASS: JSON contains the expected offline RDAP link module.")
print("Report:", sys.argv[1])
PY
```

**Output:** `~/RosieGlitchByte_Neon_Rose_Reports/example_org_YYYYMMDD_HHMMSS.json`, with the filename clock based on your machine's local time. Reports have `brand`, `domain`, `created_utc`, and `modules` fields. A rerun using the same domain in the same second can overwrite the matching file, so copy earlier findings to a separate folder when preserving every run matters.

## Optional public-domain checks

Only investigate sites that you own or have permission to assess. To inspect a domain's public DNS using the actual mode flag:

```bash
python3 "$HOME/PhantomLabsBuilds/neon-rose-phantom-station/glitchbyte-phantom-labs/tools/rosieglitchbyte_neon_rose_phantom_3.py" \
  your-authorized-domain.org --mode 1 --no-animation
```

Switch to `--mode 2` through `--mode 6` for other authorized public-site requests, or `--mode 8` to run all modules. The script refuses some non-public IP resolutions before web requests, but it does **not** establish that a target's owner granted permission. Missing security headers are observations, **not proof of vulnerabilities**.

## 📊 Inspect saved results

```bash
find "$HOME/RosieGlitchByte_Neon_Rose_Reports" -type f -name '*.json'
python3 -m json.tool "/actual/path/to/report.json" | less
```

The displayed `/actual/path/to/report.json` is a placeholder, not a generated filename. Use the path printed by `[ARCHIVED]` or by `find`.

## 🛠️ Troubleshooting

| Symptom | Fix |
| --- | --- |
| `python3` / `git` missing | Install them using the Ubuntu/Linux package manager |
| Unexpected repository folder exists | Inspect the existing contents rather than overwriting them |
| Invalid domain / prohibited port | Supply an ordinary public domain without credentials or nonstandard ports |
| Public IP check refuses a target | Stop; do not work around the non-public-address restriction |
| Redirect response instead of page | Expected: HTTP redirects are not followed by this fetcher |
| RDAP result only contains a URL | Expected: mode 7 constructs a link rather than downloading RDAP records |
| No output | Look in `~/RosieGlitchByte_Neon_Rose_Reports`, and inspect the `[ARCHIVED]` message |
| `--out` or `--output` rejected | The program does not support either flag |
| TLS verification fails | Check certificates and hostname rather than disabling TLS verification |

## 🧪 Verification and safety

The flags, eight modules, JSON structure and report path were verified by inspecting the [original Python file](../../tools/rosieglitchbyte_neon_rose_phantom_3.py). The full recipe **has not been executed end-to-end on the user's Ubuntu system** and no live target was queried in this documentation task.

Respect the repository's [security policy](../../SECURITY.md), [custom source-available license](../../LICENSE-NOTICE.md), network permissions and privacy expectations. Do not upload sensitive report output or infer individual identities from shared infrastructure.

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Homepage](../../README.md)
