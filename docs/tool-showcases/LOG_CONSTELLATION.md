<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# ✨ GLITCHBYTE LOG CONSTELLATION // PHANTOM TOOL SPOTLIGHT

<!-- GLITCHBYTE-ART-COVER:START -->

![Log Constellation | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/17_log_constellation.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · Offline log explorer · Searchable HTML dashboard + JSON · Standard library only**

[🔗 Actual Python source](../../tools/glitchbyte_log_constellation.py) · [🕷️ Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> 🌌 Your logs become constellations. Errors, warnings and event patterns become easier to explore without sending logs to a remote service.

## What this tool actually does

GlitchByte Log Constellation reads one or more **local** log/text files, detects severity labels (`TRACE`, `DEBUG`, `INFO`, `NOTICE`, `WARN`, `WARNING`, `ERROR`, `CRITICAL`, `FATAL`), counts IPv4-pattern mentions and URLs' hostnames, and saves two reports:

- `constellation.html`: standalone searchable dashboard with a severity selector and event list.
- `constellation.json`: structured counts, event records, filenames and SHA-256 hashes of source files.

It includes a **safe `--demo` option** that generates a sample log and analyzes it offline. Its basic redaction covers common secret-looking assignments and email addresses, but it **cannot guarantee removal of all sensitive data**. Review files and output carefully before sharing.

## 📋 COPY & PASTE BUILD RECIPE // Linux / Ubuntu (Bash)

**All six stages included: Install → Build → Test → Run → Find Results → Troubleshoot.** This version runs only the tool's self-generated sample data, so it makes **no website requests** and requires no real private logs.

Paste the complete block into your Bash terminal:

```bash
# PHANTOM LABS // LOG CONSTELLATION first-run recipe
set -e

# 1. INSTALL: check for Python 3 and Git (no pip packages needed).
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is needed."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git is needed."; exit 1; }

# Use a distinct workspace and avoid overwriting an existing clone.
mkdir -p "$HOME/PhantomLabsBuilds"
cd "$HOME/PhantomLabsBuilds"
if [ ! -f "glitchbyte-phantom-labs/tools/glitchbyte_log_constellation.py" ]; then
  if [ -e "glitchbyte-phantom-labs" ]; then
    echo "Existing folder is not the expected repository. Inspect it; nothing overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
cd glitchbyte-phantom-labs

# 2. BUILD: this Python tool is a script. No compiler or pip install needed.
python3 --version

# 3. TEST: check the exact source's Python syntax, then display actual help.
python3 -m py_compile tools/glitchbyte_log_constellation.py
python3 tools/glitchbyte_log_constellation.py --help

# 4. RUN: offline sample only. Output stays outside the repository.
mkdir -p "$HOME/PhantomLabsBuilds/log-constellation-reports"
python3 tools/glitchbyte_log_constellation.py \
  --demo --out "$HOME/PhantomLabsBuilds/log-constellation-reports"

# 5. FIND RESULTS: print exact paths and inspect the JSON.
echo "Your reports are:"
find "$HOME/PhantomLabsBuilds/log-constellation-reports" -type f \
  \( -name '*.html' -o -name '*.json' -o -name '*.csv' \)
python3 -m json.tool \
  "$HOME/PhantomLabsBuilds/log-constellation-reports/constellation.json" | head -n 35

# Open the dashboard if your Linux desktop supports xdg-open.
echo "HTML dashboard: $HOME/PhantomLabsBuilds/log-constellation-reports/constellation.html"
echo "Optional: xdg-open \"$HOME/PhantomLabsBuilds/log-constellation-reports/constellation.html\""
```

The `--demo` sample itself is written to `$HOME/GlitchbyteLogConstellation/samples/demo.log`, because this is the default demo source directory hard-coded by the existing script. The recipe's report files go to the separate, explicitly provided `--out` directory. Re-running creates/updates `constellation.html` and `constellation.json` there; **choose a new `--out` location if you need to preserve previous results**.

The script does not require external Python libraries, a Go compiler, or a virtual environment.

## Run it on your own local files

Once you have reviewed the file contents and permissions, run from the repository root:

```bash
python3 tools/glitchbyte_log_constellation.py \
  "$HOME/path-to-your-owned-logs/application.log" \
  --max-lines 100000 \
  --out "$HOME/PhantomLabsBuilds/my-private-log-reports"
```

Replace the quoted example path with a **real local log file you control**. The `--max-lines` flag accepts integers from 1 to 1,000,000 and applies per file. Multiple file paths are supported. No live website scan is performed.

## Find, open and read saved reports

```bash
find "$HOME/PhantomLabsBuilds" -type f \( -name '*.html' -o -name '*.json' -o -name '*.csv' \)
python3 -m json.tool "$HOME/PhantomLabsBuilds/log-constellation-reports/constellation.json" | less
xdg-open "$HOME/PhantomLabsBuilds/log-constellation-reports/constellation.html"
```

The HTML is a locally generated file. The dashboard displays up to 500 matching events at once; narrow the search to see additional matches. `xdg-open` requires a desktop session and may be unavailable on a headless Ubuntu server.

## Troubleshoot

| Symptom | Fix |
| --- | --- |
| `python3: command not found` | Install Python 3 using your distribution's package manager |
| `git: command not found` | Install Git or work from an already cloned repository |
| Repository directory already exists | Inspect that directory and use the shorter commands from within your verified clone; the recipe intentionally does not overwrite it |
| `No such file or directory` | Check the working folder using `pwd` and actual log filename |
| `Provide log file(s) or use --demo` | Supply `--demo` or at least one existing file |
| JSON/HTML did not appear | Check `--out` directory permissions, errors and filename |
| `xdg-open: command not found` | Read the JSON in terminal or transfer the HTML privately to a trusted local machine |
| Suspected sensitive data in output | Do **not share the report**; the script's redaction is only heuristic |

## Status and limits

**Source reviewed:** `tools/glitchbyte_log_constellation.py`, including `argparse`, `--demo`, `--out`, HTML/JSON outputs, redaction functions and source hashing. This documentation recipe has **not been end-to-end executed in your Ubuntu terminal**. Syntax checking is a recommended validation step, not a claim of live testing.

This tool uses offline data. It is not an X/Facebook scraper, external OSINT crawler, incident-response guarantee, authenticated log vault, or comprehensive secret scanner. Reports may still expose IP addresses, filenames and log contents. Never commit sensitive logs or reports.

Follow the repository's [license notice](../../LICENSE-NOTICE.md) and [security guidance](../../SECURITY.md).

[← PHANTOM TOOL VAULT](../TOOL_VAULT.md) · [← Homepage](../../README.md)
