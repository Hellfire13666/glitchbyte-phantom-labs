# 🌹👻 ROSIE PHANTOM SCAN V2 | PUBLIC DOMAIN INTEL STUDIO

**⚡ NO-DOWNLOAD-ATTACHMENT QUICK START:** [Copy one terminal command, generate HTML and open Firefox](../COPY_PASTE_OPEN.md). No Git pull, merge or rebase. The command is hosted in our GitHub lab and uses its own safe home folder.

**⚡ HOW TO TRIGGER THIS TOOL:** Clicking GitHub's source link only displays code. To **run the program and open Firefox**, [open the one-paste launcher instructions](../COPY_PASTE_OPEN.md#-how-visitors-actually-trigger-a-tool), copy the complete Bash command for this tool, paste it into an **Ubuntu/Linux Terminal**, and press **Enter**. Wait for the local `[REPORT]` HTML path. Firefox opens automatically if installed; otherwise open that saved HTML path manually. These are not one-click GitHub apps, and typing a tool name alone is not a shell command.


**Independent Python 3 tool · Responsive Rosie-branded HTML dashboard · JSON evidence · 11 report panels · Optional Findomain + WHOIS**

[🐍 Source](../../tools/rosie_phantom_scan_v2.py) · [🧪 Automated tests](../../tests/test_rosie_phantom_scan_v2.py) · [🕷️ Tool Vault](../TOOL_VAULT.md)

Research a public domain with a small, bounded set of conventional lookups. Reports distinguish missing observations from confirmed facts. This is **not** a port scanner, identity attribution service, vulnerability scanner or unlimited crawler.

### Modules

| Panel | What it reports |
| --- | --- |
| 01 Target/IP | Domain, resolved IPs and collection timestamp |
| 02 DNS | A, AAAA, MX, NS, SOA, CAA, TXT via Google DNS-over-HTTPS |
| 03 HTTPS certificate | Protocol, issuer, subject, expiration, subject-alternative names |
| 04 Website | Status, title, description, canonical, OpenGraph, up to 30 page link paths |
| 05 Headers | Selected HTTPS security-header observations |
| 06 WHOIS/RDAP | Domain events, nameservers, registrar/registration roles if available |
| 07 crt.sh | Optional public certificate-transparency subdomain names |
| 08 Findomain | Optional installed `findomain` command; not required |
| 09 WHOIS CLI | Optional installed `whois` command; not required |
| 10 Portals | Clickable public research service links |
| 11 Notes | Errors, incompleteness, and safety boundaries |

An offline run exercises the **real rendering and export pipeline** but deliberately performs no remote lookups. Use a public domain you own or are authorized to examine for live checks. DNS, RDAP and certificate transparency are external services, so live results may be stale or unavailable. Missing security headers alone do **not** establish a vulnerability.

## 📋 COPY & PASTE BUILD RECIPE // UBUNTU / LINUX BASH

**Install → Build → Test → Run → Find Results → Troubleshoot**

The following block runs only the safe **offline preview** in CI, opens the generated HTML in Firefox when available on a graphical machine, and does not touch your existing Git checkout. It does not use `exit` or Git merges. The initial clone contacts GitHub; everything after checkout works offline.

```bash
# ROSIE PHANTOM SCAN V2 / SAFE FIRST RUN
command -v python3 >/dev/null 2>&1 && echo "PASS: Python 3 found"
command -v git >/dev/null 2>&1 && echo "PASS: Git found"

STATION="$HOME/PhantomLabsBuilds/rosie-scan-v2"
mkdir -p "$STATION"
cd "$STATION"

# Clone only if no prior checkout; do not overwrite or merge an existing tree.
if [ ! -d glitchbyte-phantom-labs ]; then
    git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

SCRIPT="$STATION/glitchbyte-phantom-labs/tools/rosie_phantom_scan_v2.py"
OUTPUT="$STATION/reports"

# BUILD: Validate the actual Python source.
python3 - "$SCRIPT" <<'PY'
from pathlib import Path
import sys
source = Path(sys.argv[1])
compile(source.read_bytes(), str(source), "exec")
print("PASS: Rosie V2 Python 3 syntax")
PY

# TEST: Confirm real CLI options.
python3 "$SCRIPT" --help

# RUN: Offline example, no DNS/API/WHOIS/Findomain connections.
python3 "$SCRIPT" example.com --offline --no-browser \
    --artwork "$STATION/glitchbyte-phantom-labs/artwork/labface2.png" \
    --out "$OUTPUT"

# FIND & READ: Confirm the real HTML and JSON were saved.
python3 - "$OUTPUT" <<'PY'
from pathlib import Path
import json
import sys
folder = Path(sys.argv[1])
html_files = sorted(folder.glob("rosie_v2_*.html"))
json_files = sorted(folder.glob("rosie_v2_*.json"))
assert html_files and json_files, "Missing report output files"
document = json.loads(json_files[-1].read_text(encoding="utf-8"))
assert document["domain"] == "example.com" and document["mode"] == "offline"
assert "ROSIE PHANTOM" in html_files[-1].read_text(encoding="utf-8")
print("PASS: HTML + JSON report generated")
print("HTML PREVIEW:", html_files[-1])
PY

# SHOW: Opens Firefox when it is installed, without closing the terminal.
if command -v firefox >/dev/null 2>&1; then
    LATEST=$(find "$OUTPUT" -maxdepth 1 -name 'rosie_v2_*.html' -type f -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)
    if [ -n "$LATEST" ]; then firefox "$LATEST" >/dev/null 2>&1 & fi
fi
```

### Run a live, public domain lookup

Once the first-run preview succeeds, use the same script for a domain you own or are authorized to research:

```bash
python3 "$HOME/PhantomLabsBuilds/rosie-scan-v2/glitchbyte-phantom-labs/tools/rosie_phantom_scan_v2.py" \
  example.com --passive-subdomains --findomain --whois-cli \
  --artwork "$HOME/PhantomLabsBuilds/rosie-scan-v2/glitchbyte-phantom-labs/artwork/labface2.png"
```

Without a domain argument, the script prompts you. By default, reports go to `~/ROSIE_PHANTOM_SCAN_V2`. The optional `findomain` and `whois` programs are **not installed by this script**; missing ones are recorded in the notes and do not stop RDAP/DNS research. The HTTPS request doesn't follow domain redirects. Results are bounded, and filenames are generated uniquely to preserve past reports.

### 🛠️ Troubleshooting

- **Git clone fails:** Verify Git and network connectivity. Do not reset or rebase your original repository.
- **Python missing:** Install Python 3 on Ubuntu before running the recipe.
- **Findomain or WHOIS not installed:** Optional stages are skipped. RDAP is part of the main script.
- **No results:** Public services may be unreachable, redacted or empty. Check the report Notes panel.
- **Firefox not installed / no graphical desktop:** Open the saved `.html` file manually using a browser.
- **Image missing:** The dashboard shows a rose fallback rather than failing.
- **Domain rejected:** Supply only a public hostname such as `example.com`, not a URL, IP address or path.
- **Need an offline demo:** Include `--offline`; this suppresses all network calls and optional commands.

### Testing and scope

[Offline tests](../../tests/test_rosie_phantom_scan_v2.py) cover file exports, domain filtering, Unicode/HTML escaping, placeholder/offline mode, options, and the saved report, without hitting internet services. GitHub Actions also executes this page's first Bash block in a clean temporary Linux home. **Live network lookups and Findomain versions are not certified by the offline tests.**

[Source-available license notice](../../LICENSE-NOTICE.md) · [Security policy](../../SECURITY.md)
