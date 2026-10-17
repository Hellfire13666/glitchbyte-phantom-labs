# 🌹 GLITCHBYTE PHANTOM LABS

**RosieGlitchByte | Python • Linux • Terminal • Public OSINT • Creative Coding**

A collection of Python projects, experiments, and research utilities created for the Glitchbyte Phantom Labs workshop.

> Built in the shadows. Preserved in the code.

## Contents

- `tools/` Python 3 scripts and utilities
- `artwork/` companion original artwork
- `docs/` project inventory and publishing checklist

## 🕷️ Start here: Find • Build • Run • Read

**New to the lab?** Follow the [Phantom Labs Tool Starter Guide](docs/TOOL_STARTER_GUIDE.md) for discovering projects, running Python or Go tools, finding generated HTML/JSON/CSV reports, and our required new-tool testing checklist.

Find saved reports from your current folder:

```bash
find . -type f \( -name "*.html" -o -name "*.json" -o -name "*.csv" \)
```

**Every new creation:** unique project and report names, a documented build/test process, readable sample commands and output, and live site-by-site progress where technically practical. Upgrades and remakes happen only when specifically requested.

## Run a tool

```bash
python3 tools/rose_crawler.py --help
```

Some tools may need optional dependencies, an API key you supply, or network access. Read each script before running. Never commit passwords, session cookies, tokens, personal data, or sensitive research reports.

## Dependencies

Python 3 is required. DNS research features use dnspython.

On Ubuntu, install it with:

    sudo apt install python3-dnspython

Alternatively, install requirements.txt in a Python virtual environment.

## Ownership and reuse

**Project publisher and attribution:** RosieGlitchByte.

Copyright © 2026 RosieGlitchByte, to the extent applicable. The custom source-available license permits downloading and running the unmodified tools. Modifications and redistribution require prior written permission from RosieGlitchByte. See `LICENSE-NOTICE.md`. AI-assisted material may not qualify for copyright protection in all jurisdictions; attribution and a copyright notice do not establish exclusive ownership.

## Status

Initial preservation archive. Code has been syntax-checked; individual tools are not all integration-tested or security-audited. Review before public release.

## Release candidate status

This package is a **private release candidate**, not an approved public release. Review `SECURITY.md` and `docs/RELEASE_CHECKLIST.md` before changing repository visibility.

## Local checks

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q tools
```

The repository layout is intentionally flat: `README.md`, `tools/`, `artwork/`, and `docs/` sit at the repository root.
