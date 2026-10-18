<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 📡 ROSIEGLITCHBYTE IP SPECTER // TOOL SHOWCASE

**Python 3 · IP classification and public network data · JSON archive · Standard library only**

[🐍 Verified source](../../tools/rosieglitchbyte_ip_specter.py) · [🕷️ Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> **The radar starts with local facts.** IP Specter is a separate project from IP Shadow Scraper and Domain Phantom. Network features are optional and must be used only where permitted.

## Actual functionality

| Mode | Action | Network traffic? |
| --- | --- | --- |
| `1` | Classify IPv4/IPv6 address (global, private, loopback, link-local, reserved, etc.) | **No** |
| `2` | Reverse DNS hostname lookup | Yes, DNS |
| `3` | RDAP public network metadata via rdap.org for global IPs | Yes for global IPs |
| `4` | TLS certificate on TCP port 443, requiring `--hostname` for certificate validation | Yes |
| `5` | TCP connectivity on ports **22, 80, 443** | **Yes; explicit `--authorized` or interactive confirmation required** |
| `6` | Combined *public* report: classification, reverse DNS and RDAP | DNS/RDAP for applicable inputs; **does not include ports or TLS** |

Mode 5 reports `open` versus `closed_or_filtered`; it cannot reliably distinguish a closed port from packet filtering. The tool does not perform stealth scanning, credentials tests, exploit checks or private content access.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

**Install → Build → Test → Run → Find Results → Troubleshoot.** The first run only classifies the reserved documentation address `192.0.2.1`. **It does not contact the address**, perform port checks, or require any API key. The optional initial Git clone contacts GitHub.

```bash
# PHANTOM LABS // IP SPECTER FIRST RUN
set -e

# 1. INSTALL: Python 3 and Git; no external Python packages required.
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/ip-specter-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

if [ ! -f glitchbyte-phantom-labs/tools/rosieglitchbyte_ip_specter.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Unexpected existing folder: inspect it; refusing to overwrite."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: standalone Python; no compiler needed.
python3 --version

# 3. TEST: syntax validation and actual CLI help (offline).
python3 -m py_compile glitchbyte-phantom-labs/tools/rosieglitchbyte_ip_specter.py
python3 glitchbyte-phantom-labs/tools/rosieglitchbyte_ip_specter.py --help

# 4. RUN: purely local classification, using a documentation-only IPv4 address.
python3 glitchbyte-phantom-labs/tools/rosieglitchbyte_ip_specter.py \
  192.0.2.1 --mode 1

# 5. FIND RESULTS: fixed output directory set by the source.
REPORT_DIR="$HOME/RosieGlitchByte_IP_Reports"
echo "Saved reports:"
find "$REPORT_DIR" -maxdepth 1 -type f \
  -name 'ip_specter_192.0.2.1_1_*.json' -print
echo "Inspect your real file with: python3 -m json.tool /actual/path/report.json"
```

The original script prints the archived file's exact location. Reports use `~/RosieGlitchByte_IP_Reports/ip_specter_<IP>_<mode>_<UTC timestamp>.json`, and there is **no `--out` flag**. An IPv6 filename replaces colons with hyphens. Runs in the same second with the same IP/mode may replace one another.

### Optional permitted public lookups

**Only for an IP you own or have a legitimate reason to check**, use the actual mode flags below. Replace the placeholder with a valid IP:

```bash
cd "$HOME/PhantomLabsBuilds/ip-specter-station"
# Reverse DNS / public RDAP only when appropriate
python3 glitchbyte-phantom-labs/tools/rosieglitchbyte_ip_specter.py \
  YOUR_PUBLIC_IP --mode 6

# TLS certificate with a real matching hostname (mode 4)
python3 glitchbyte-phantom-labs/tools/rosieglitchbyte_ip_specter.py \
  YOUR_PUBLIC_IP --mode 4 --hostname your-authorized-host.example
```

Mode `5` makes TCP connections to ports 22, 80 and 443. It should only be selected when you **explicitly** have authorization for that host. The `--authorized` option records your assertion of permission; it does not itself grant permission.

### Find and read the report

```bash
find "$HOME/RosieGlitchByte_IP_Reports" -type f -name '*.json'
python3 -m json.tool "/full/path/to/your-actual-report.json" | less
```

The JSON contains `tool`, `timestamp_utc`, `target`, `mode` and `results`. The current implementation does **not** generate HTML or CSV.

## 🛠️ Troubleshooting

| Issue | Check |
| --- | --- |
| Python or Git not found | Install from your Linux distribution's package manager |
| Invalid IPv4 / IPv6 input | Use a valid IP address, without a port number |
| Report missing | Inspect `~/RosieGlitchByte_IP_Reports`, the console's `[ARCHIVED]` message, and filesystem permissions |
| RDAP skipped | Non-global addresses are intentionally skipped |
| Reverse DNS returns an error | Many IP addresses have no reverse DNS; this does not prove anything about identity |
| TLS returns an error | Verify hostname, public address, port access and certificate trust; don't disable verification |
| Port checks blocked | A correct authorization confirmation is required; do not try to bypass restrictions |
| `closed_or_filtered` | This means the TCP connection failed; the tool does not distinguish the reasons |
| Report overwritten | Copy previous JSON to a distinct filename or run at another time |

## 🧪 Evidence, privacy and limitations

The supported flags, six modes and report path were confirmed by inspecting [the existing source](../../tools/rosieglitchbyte_ip_specter.py). This **documentation update is not an executed Ubuntu end-to-end test**, and no external IP address was queried here. Mode 1 is offline, but modes 2–6 have different networking and authorization requirements.

Network metadata does not identify an individual; IP addresses may be shared or dynamically assigned. Review [SECURITY.md](../../SECURITY.md) and the repository's [custom source-available license](../../LICENSE-NOTICE.md). Never commit private scan output, credentials or personal information.

[← PHANTOM TOOL VAULT](../TOOL_VAULT.md) · [← Official homepage](../../README.md)
