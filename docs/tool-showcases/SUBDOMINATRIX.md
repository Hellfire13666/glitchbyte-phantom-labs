<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹👻 SUBDOMINATRIX // ROSIE'S SUBDOMAIN INTELLIGENCE RIOT

**Same domains. Different perspective.** Multi-source public subdomain reconnaissance and reporting by GlitchByte Phantom Labs.

![SUBDOMINATRIX Main Artwork](../../artwork/subdom.png)

![SUBDOMINATRIX Second Artwork](../../artwork/Screenshot_2026-10-17_23-22-21.png)

**Official SUBDOMINATRIX artwork:** Both Rosie-themed pictures above are stored in this repository and displayed on this tool page. They are promotional illustrations, not live scanner screenshots. The statistics, maps, sample hostnames and command-like text depicted in the artwork are illustrative; use the verified commands below to run the actual tool. Real reports contain observed records or clearly labeled synthetic demo data.

[Python 3 source](../../tools/subdominatrix.py) · [Offline tests](../../tests/test_subdominatrix.py) · [One-paste launcher page](../COPY_PASTE_OPEN.md) · [Full Tool Vault](../TOOL_VAULT.md)

## What the actual tool does

- **Four public passive sources:** crt.sh certificate-transparency entries; AlienVault OTX passive DNS; HackerTarget hostsearch; and urlscan.io public observations. Their free endpoints can be rate-limited, empty, or unavailable, and the report says so.
- **Optional installed Subfinder and Findomain:** Use `--subfinder` and `--findomain` to run local executables; not bundled or installed. Missing tools do not stop the passive public-source scan.
- **Normalization and source attribution:** Keep only syntactically valid DNS names ending in the exact target domain; deduplicate across sources; indicate overlaps.
- **Opt-in DNS checking:** `--dns-check` checks at most `--max-verify` selected names with an 8-worker ceiling and records public vs reserved/private address observations.
- **Opt-in HTTPS headers:** `--http-check` together with `--dns-check` performs **one** bounded HEAD request over verified TLS per checked public hostname, using a validated public IP and hostname verification. It does not follow redirects or crawl links.
- **Technology clues:** A small set of hints inferred from HTTPS response headers only, not a comprehensive stack analysis and not a security-risk score.
- **Four saved outputs:** Neon HTML with client-side filtering, JSON, CSV, and TXT; unique output names preserve earlier reports.
- **Source-by-source feedback:** Name counts, status, elapsed seconds and error reasons so viewers can tell unavailable data from zero discoveries.
- **Offline demo:** Clearly marked synthetic names under `example.com`; **no external requests or optional CLI calls**.

**Not in this release:** global asset geolocation, screenshots, automatic technology fingerprints beyond selected headers, vulnerability scoring, login automation, unlimited crawling, brute-force enumeration, or automatic ownership attribution. These appear only as design directions in the concept picture, not as implemented features.

## 🧪 COPY & PASTE BUILD RECIPE // Ubuntu/Linux first run

**Install → Build → Test → Run → Find results → Troubleshoot.** The first Bash block is independently exercised in Linux CI under a disposable home folder. It generates an **offline synthetic preview**, not a live scan. It uses a dedicated checkout and does not alter a user's original Git clone.

```bash
# 🌹 SUBDOMINATRIX • GUARANTEED NO-LIVE-LOOKUP DEMO
command -v python3 >/dev/null 2>&1 && echo "Python 3 found"
command -v git >/dev/null 2>&1 && echo "Git found"

STATION="$HOME/PhantomLabsBuilds/subdominatrix"
mkdir -p "$STATION"
cd "$STATION"

# Install source in an independent folder, without git pull, merge, reset or exit.
if [ ! -d glitchbyte-phantom-labs ]; then
    git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

SCRIPT="$STATION/glitchbyte-phantom-labs/tools/subdominatrix.py"
OUTPUT="$STATION/reports"

# Verify Python source syntax before running anything.
python3 - "$SCRIPT" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
compile(path.read_bytes(), str(path), "exec")
print("PASS: SUBDOMINATRIX Python 3 source syntax")
PY

# Verify documented flags.
python3 "$SCRIPT" --help

# Create real JSON, CSV, TXT, and HTML from synthetic demonstration names.
python3 "$SCRIPT" example.com --offline-demo --no-open \
  --artwork "$STATION/glitchbyte-phantom-labs/artwork/labface2.png" \
  --out "$OUTPUT"

# Confirm all four output types really exist and demo state is explicit.
python3 - "$OUTPUT" <<'PY'
from pathlib import Path
import json
import sys
folder=Path(sys.argv[1])
files=list(folder.glob("subdominatrix_*.json"))
assert files, "No JSON report generated"
data=json.loads(files[-1].read_text(encoding="utf-8"))
assert data["mode"]=="SYNTHETIC OFFLINE DEMO"
assert data["stats"]["names"]>=10
for extension in (".html", ".csv", ".txt"):
    assert files[-1].with_suffix(extension).is_file(), "Missing " + extension
print("PASS: SUBDOMINATRIX offline intelligence preview")
print("HTML:",files[-1].with_suffix(".html"))
PY

# Open the newly generated HTML in Firefox if installed.
if command -v firefox >/dev/null 2>&1; then
    LATEST=$(find "$OUTPUT" -maxdepth 1 -name 'subdominatrix_*.html' -type f -printf '%T@ %p\n' | sort -nr | head -n 1 | cut -d' ' -f2-)
    if [ -n "$LATEST" ]; then firefox "$LATEST" >/dev/null 2>&1 & fi
fi
```

## 🔧 Findomain slow-internet correction (Checklist #3)

The October 19, 2026 Ubuntu test returned **51 unique public-source hostname candidates** but reported `[OPTIONAL] findomain: failed | 0 records`. A separate direct `findomain -t facebook.com` run had previously completed successfully in 23 seconds. The tool was limiting Findomain to **24 seconds** because the public-provider `--timeout 8` was also used to derive a CLI deadline. The optional failure message hid the reason, and `subprocess.run` discarded partial output on timeout. A crt.sh HTTP 502 was a separate provider problem, not a failure of the overall collection.

**New behavior:**

- `--timeout 8` limits each public HTTP provider; `--cli-timeout 60` separately limits each installed Subfinder/Findomain command. Values for `--cli-timeout` are **10 to 120 seconds**.
- Candidate hostnames from an optional executable are printed as lines arrive. A timed-out or nonzero-exit process retains any candidates already collected and labels itself `partial`, `timeout` or `failed` accurately.
- `[OPTIONAL]` now prints **the reason and elapsed seconds**, not only `failed`. A `[WAIT]` heartbeat keeps the terminal alive during slow requests.
- The program runs no automatic provider retry on HTTP 429, respects the provider's rate limit, and continues other sources.
- `--terminal-only` still creates **no report files**; without it, the original four report formats and Firefox opening work as before.

**Recommended live public-source test (new source on main):**

```bash
export PATH="$HOME/.local/bin:$HOME/go/bin:$PATH"
SCRIPT="$HOME/PhantomLabsLaunchers/subdominatrix_live_signal_2026/subdominatrix_live_signal_2026.py"
python3 -u "$SCRIPT" facebook.com --terminal-only --color always \
  --findomain --timeout 8 --cli-timeout 60 --max-results 1000
```

The path shown above is the workshop's separately downloaded upgrade. If not installed there, use the build recipe below and substitute your actual source path. Download a fresh copy after the fix is merged. A successful public-source run can be **partial** when a remote provider returns HTTP 502 or 429; hostname candidates do not establish current active services.

---

## ⚡ Colorful terminal-only live signal (available on main)

**Want real intelligence scrolling by without saved files?** The upgraded source provides `--terminal-only` and `--color always` while keeping the original Firefox/HTML/JSON/CSV/TXT workflow unchanged. These options are now published on the `main` branch. Local older copies must be refreshed explicitly; the original Firefox/export mode continues working.

### Terminal-only, public-source research, no report files

```bash
SCRIPT="$HOME/PhantomLabsBuilds/subdominatrix/glitchbyte-phantom-labs/tools/subdominatrix.py"
python3 -u "$SCRIPT" example.com --terminal-only --color always --timeout 8
```

To add the separately installed passive Findomain and Subfinder, run `python3 -u "$SCRIPT" example.com --terminal-only --color always --timeout 10 --findomain --subfinder`.

**What appears:** `[MODE] LIVE PUBLIC-SOURCE COLLECTION`, `[START]`, `[SOURCE]`, `[FOUND]`, periodic `[WAIT]`, optional `[OPTIONAL]`, and a truthful `[SUMMARY]`. HTTP 429 errors are labeled `rate-limited` with any reported Retry-After hint, without immediately retrying a throttled provider. Each provider's findings appear when **that provider completes**; installed CLI tools still deliver their buffered findings after each tool finishes. Counts are candidate names, not verified live web services.

**Files OFF:** `--terminal-only` skips exporting reports and opening Firefox. **Firefox ON:** omit `--terminal-only` to keep the existing automatic HTML/JSON/CSV/TXT export and local Firefox launch. `--no-open` stops only browser launch, not export. This upgrade preserves the original default for legacy launchers and tests.

### 🌱 SIMPLE | Offline preview of terminal signal (no network)

```bash
python3 -u "$SCRIPT" example.com --offline-demo --terminal-only --color always
```

This displays a labeled **synthetic offline demo**, saves nothing, and does not contact the internet.

### ⚡ MEDIUM | Real passive hostname findings

```bash
python3 -u "$SCRIPT" example.com --terminal-only --color always --timeout 8
```

### 🔥 EXTRA | More passive sources, still no active probes

```bash
export PATH="$HOME/.local/bin:$HOME/go/bin:$PATH"
python3 -u "$SCRIPT" example.com --terminal-only --color always \
  --findomain --subfinder --timeout 10 --max-results 1200
```

The Extra command only queries public-domain sources and the installed public discovery tools, not direct DNS or HTTP verification. For explicitly authorized direct checks, add `--dns-check --http-check --max-verify 10`; this contacts listed hosts and should only be used on targets you own or are authorized to assess. Long-running/limited public sources may return partial results.

## 🌈 Three beginner run levels (after installing)

See also our [SIMPLE · MEDIUM · EXTRA runtime cookbook](../BEGINNER_RUNTIME_RECIPES.md) for the full explanation. These examples use **existing** documented options, not new `--simple`/`--medium`/`--extra` flags.

Set the script location once after completing the build instructions below:

```bash
SCRIPT="$HOME/PhantomLabsBuilds/subdominatrix/glitchbyte-phantom-labs/tools/subdominatrix.py"
```

**🌱 SIMPLE | Safe first-run preview, no network lookups**

```bash
python3 "$SCRIPT" example.com --offline-demo --no-open
```

Synthetic preview only, not live intelligence.

**⚡ MEDIUM | Real public passive sources**

```bash
python3 "$SCRIPT" example.com --no-open --max-results 300
```

Shows per-source public-data feedback and returns matching hostname candidates, subject to provider availability.

**🔥 EXTRA | Opt-in bounded DNS/HTTPS verification for authorized domains**

```bash
python3 "$SCRIPT" YOUR-AUTHORIZED-DOMAIN.example \
  --subfinder --dns-check --http-check \
  --max-verify 20 --max-results 300 --no-open
```

**Saving note:** This existing version always produces HTML/JSON/CSV/TXT; `--no-open` only stops Firefox from opening. A future terminal-first upgrade may add no-save as the default, but these instructions describe the actual published code. Names are candidate observations, not proof of service reachability or ownership. Limits and run times vary with network conditions.

---

### 🕷️ One-paste launcher, once the PR is merged

GitHub source links **do not execute Python**. Copy this *whole* block into the Ubuntu terminal, press Enter, and wait for the reported local HTML path. Firefox opens automatically if installed. This uses an isolated `~/PhantomLabsLaunchers` directory, not any old Git checkout.

```bash
mkdir -p "$HOME/PhantomLabsLaunchers" && curl -fL --retry 2 "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/phantom_quickopen.py" -o "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" && python3 "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" subdominatrix
```

**This exact launcher works on the GitHub main branch only after the release PR is merged.** An unmerged branch's URL cannot be downloaded from `/main/`. The standalone full recipe above also requires the release's source to be on main. Do not run pictured/mock installation commands from the promotional design.

### Real authorized research with Subfinder and Findomain

Only perform DNS and HTTP checks for domains you own or have permission to inspect. For public passive collection, supply a real public DNS domain:

```bash
SCRIPT="$HOME/PhantomLabsBuilds/subdominatrix/glitchbyte-phantom-labs/tools/subdominatrix.py"
python3 "$SCRIPT" example.com --subfinder --findomain \
  --dns-check --http-check --max-verify 40 --max-results 800
```

The `subfinder` and `findomain` binaries are optional; they must already be installed. The tool does **not** install them. Try `python3 "$SCRIPT" --help` for all verified flags.

### 🛠️ Troubleshooting

- **404 from curl:** The launcher PR has not merged to main, the link is wrong, or GitHub is unreachable. Don't delete or reset your existing checkout.
- **Firefox does not appear:** Test `firefox https://example.com`. Copy the printed absolute HTML report path into Firefox manually if needed.
- **Typing `subdominatrix` returns command not found:** This is a Python script, not an installed shell executable. Run the complete launcher block or `python3 "$SCRIPT" ...`.
- **No subdomains found:** Providers are rate-limited, unavailable, or don't have records; inspect the source feedback table.
- **Findomain/Subfinder missing:** Skip those flags or install the official programs separately. Passive services remain available.
- **HTTPS returns 'failed':** Certificate validation, site reachability, or HEAD support can fail; absence is not proof of weakness.
- **Demo looked too successful:** Demo results are fabricated **only for offline visualization**, never displayed as live findings.
- **Need screenshots or global map:** Not yet implemented; the poster is a concept, not tool output.

### Verification and limitations

[Tests](../../tests/test_subdominatrix.py) cover input scope, source parsers using mocked public services, demo rendering, saved formats, HTML injection escaping, limited DNS/HTTPS options, and rejecting reserved IPs. CI checks the full terminal recipe without hitting real third-party websites. **Live provider availability, data accuracy, and optional Subfinder/Findomain versions are not certified by offline tests.**

[Source-available license](../../LICENSE-NOTICE.md) · [Security guidelines](../../SECURITY.md)
