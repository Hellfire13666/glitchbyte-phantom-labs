<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 👻 ROSIEGLITCHBYTE DOMAIN PHANTOM // TOOL SPOTLIGHT

<!-- GLITCHBYTE-ART-COVER:START -->

![Domain Phantom | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/04_domain_phantom.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · Single-domain public research · Eight modules · JSON reports · Standard library**

[🐍 Actual Python source](../../tools/rosieglitchbyte_domain_phantom.py) · [🕷️ Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> **A lantern for public domain signals, not private networks.** Domain Phantom is a distinct existing project from [GlitchByte Domain Intel](DOMAIN_INTEL.md); the two have different modes, safeguards and output locations.

## 🔎 What the current code does

| Mode | Existing module | Description |
| --- | --- | --- |
| `1` | DNS / IP lookup | Resolves hostname and rejects results including non-public addresses |
| `2` | Website metadata | Retrieves public HTTPS homepage metadata and selected response headers |
| `3` | Public page links | Collects up to 100 distinct links from the homepage, without crawling linked pages |
| `4` | Security headers | Observes six response-header names; absence does not prove a vulnerability |
| `5` | TLS certificate | Connects to HTTPS port 443 and reads verified certificate fields |
| `6` | robots.txt | Reads a limited robots.txt preview for information only |
| `7` | RDAP research link | **Constructs** a public RDAP URL; does not retrieve or parse registration data |
| `8` | Full report | Runs modes 1–7, with separate per-module error reporting |

The current tool displays a completion summary for each selected module. It uses Python's standard library, an 8-second timeout for certain network operations, a maximum 450 KB homepage response body, and deliberately **does not follow HTTP redirects** for public-page requests.

**Safety limitation:** The source checks DNS results for public addresses before many requests and rejects non-public results. DNS can change between checking and connecting, so this is **not a complete SSRF/network isolation guarantee**. Use only domains you own or are authorized to inspect, and do not expose this CLI as an untrusted public service.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

**Install → Build → Test → Run → Find Results → Troubleshoot.**

This first run uses **mode 7 only**, which constructs a research link for `example.org` **without making a DNS, web, TLS, or RDAP network request**. The initial `git clone` naturally contacts GitHub. Paste the whole block in Bash:

```bash
# PHANTOM LABS // DOMAIN PHANTOM first-run recipe
set -e

# 1. INSTALL: check Python and Git.
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git required."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/domain-phantom-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/rosieglitchbyte_domain_phantom.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "An unexpected repository directory exists. Inspect it rather than overwrite."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: Python script, no compilation or third-party modules needed.
python3 --version

# 3. TEST: validate actual syntax and CLI help.
python3 -m py_compile glitchbyte-phantom-labs/tools/rosieglitchbyte_domain_phantom.py
python3 glitchbyte-phantom-labs/tools/rosieglitchbyte_domain_phantom.py --help

# 4. RUN: offline RDAP URL generation only. No site is checked.
python3 glitchbyte-phantom-labs/tools/rosieglitchbyte_domain_phantom.py \
  example.org --mode 7 --no-animation

# 5. FIND RESULTS: output location is fixed by the source.
REPORT_DIR="$HOME/RosieGlitchByte_Domain_Intel"
echo "Report directory: $REPORT_DIR"
find "$REPORT_DIR" -maxdepth 1 -type f -name 'example_org_*.json' -print

# Read the most recently modified matching report, if present.
LATEST=$(find "$REPORT_DIR" -maxdepth 1 -type f -name 'example_org_*.json' \
  -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)
if [ -n "$LATEST" ]; then
  python3 -m json.tool "$LATEST"
fi
```

**Important:** The tool uses `~/RosieGlitchByte_Domain_Intel` as its output directory. Its CLI currently has **no `--out` flag**. Filename format is `<domain_with_underscores>_YYYYMMDD_HHMMSS.json`, using the machine's local clock. Running twice in the same second could replace a report. Keep copies in another folder if preserving every run matters.

The `find -printf` command is for GNU Find, standard on Ubuntu/Linux. This recipe is not intended for Windows PowerShell.

## 🌐 Optional authorized public-domain lookup

For a domain you control or are permitted to investigate, replace the placeholder with your actual domain:

```bash
cd "$HOME/PhantomLabsBuilds/domain-phantom-station"
python3 glitchbyte-phantom-labs/tools/rosieglitchbyte_domain_phantom.py \
  your-authorized-domain.org --mode 1 --no-animation
```

For additional public website, TLS or robots.txt lookups, change `--mode` to 2–6. `--mode 8` runs all seven modules, including network operations; don't select it unless you understand and authorize each check.

## 📊 Read the report

```bash
find "$HOME/RosieGlitchByte_Domain_Intel" -type f -name '*.json'
python3 -m json.tool "/full/path/to/actual_report.json" | less
```

Reports contain `brand`, `domain`, `created_utc`, and `modules` with the selected module's records or errors. This tool currently writes **JSON only**, not CSV or HTML.

## 🛠️ Troubleshooting

| Symptom | What to check |
| --- | --- |
| Python or Git missing | Install them using your distribution's package manager |
| `Only ordinary public domains are supported` | Remove credentials, unusual ports or unsupported URL schemes |
| `Target resolves to a non-public address` | Stop; the safety check refused the destination |
| TLS certificate or DNS failure | Check connectivity, authorization, certificate and DNS configuration; do not disable certificate verification |
| Redirect reported rather than followed | Expected: the HTTP requester disables redirects |
| RDAP mode has only a URL | Expected: mode 7 does **not** download RDAP data |
| No report found | Check `~/RosieGlitchByte_Domain_Intel` and the printed `[ARCHIVED]` path |
| Repeated report filename | Preserve the earlier JSON separately before rerunning within the same second |
| Terminal animation annoying | Use `--no-animation` |

## 🧪 Verification, privacy and licensing

This documentation was prepared by inspecting [the current Python source](../../tools/rosieglitchbyte_domain_phantom.py). It does **not** claim that a live external target was scanned or that the full Bash recipe has been executed in an Ubuntu terminal. Source inspection and syntax recommendations are not network integration tests.

Follow [SECURITY.md](../../SECURITY.md) and [LICENSE-NOTICE.md](../../LICENSE-NOTICE.md). Never commit credentials, private findings, cookies or sensitive reports.

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Official homepage](../../README.md)

## 💾 Easy-save output (`-o` / `--o`)

For this existing tool, use the tested shared [Phantom Easy Save runner](../EASY_SAVE_ALL_TOOLS.md) to capture its **printed terminal output** in a new plain TXT without changing the tool's own CLI. First install the runner using that linked guide, then **from the HQ repository root** try the harmless help-only test:

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
python3 "$SAVER" --o domain_phantom_terminal.txt -- python3 -u tools/rosieglitchbyte_domain_phantom.py --help
```

That saves **help text only**, not live results. For real output, replace the `--help` after the `--` separator with the **actual run options documented earlier on this page**; e.g. `python3 "$SAVER" -o domain_phantom_results.txt -- python3 -u tools/rosieglitchbyte_domain_phantom.py ACTUAL_TOOL_ARGS`. The runner saves terminal text, not a structured CSV/JSON export. Any files this legacy tool already writes are **still written**; this runner does not suppress its built-in save behavior or create a Firefox dashboard. Existing output names are never overwritten. Newly built tools will offer native `-o` and `--o` when meaningful.

