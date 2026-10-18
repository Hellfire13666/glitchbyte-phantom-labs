<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌐 GLITCHBYTE DOMAIN INTEL // PHANTOM TOOL SPOTLIGHT

**Python 3 · Public domain research · Six modes · Timestamped JSON results**

[🔗 Source code](../../tools/glitchbyte_domain_intel.py) · [🕷️ Phantom Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> **A domain's public signals, presented as a readable terminal investigation.** Use only sites and domain names you own or have appropriate permission to assess, and respect their terms and rate limits.

## 🔎 What it does

The existing source provides six selectable modes, using the *actual* `--mode` flag:

| Mode | Feature | What the current code retrieves |
| --- | --- | --- |
| `1` | DNS | IP addresses via Python sockets, and optional A/AAAA/MX/NS/TXT/CAA records using `dnspython` |
| `2` | Website | Homepage HTML title, meta description, HTTP status and response headers |
| `3` | Links | HTTP(S) links found in the homepage response, including external hostnames |
| `4` | TLS and headers | Leaf certificate details and six HTTP security-header observations |
| `5` | RDAP | Public domain registration metadata from `rdap.org`, often redacted |
| `6` | Combined | All of the above |

**Limits:** HTTP requests have a 9-second fetch timeout; the homepage response is capped at about 600 KB, with up to 150 unique links retained in the link report. It does **not** recursively crawl websites, verify ownership or identity, or demonstrate a vulnerability. Standard DNS resolution and direct certificate lookup may have different timeout behavior.

The optional `dnspython` package adds DNS record types; without it, base IP resolution still works and the report explains the limitation. The script prints individual mode results as they complete, but does **not** show a site-by-site progress counter because it scans one chosen domain.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu or Linux Bash

**Install → Build → Test → Run → Find Results → Troubleshoot.** Copy this block into Bash. The code only starts a network request **after** you type a domain you are permitted to assess.

```bash
# PHANTOM LABS // DOMAIN INTEL build-and-run recipe
set -e

# 1. INSTALL: Python 3 and Git are the only required tools.
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }

# Keep releases outside the working repository, without overwriting files.
WORKSPACE="$HOME/PhantomLabsBuilds/domain-intel-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f "glitchbyte-phantom-labs/tools/glitchbyte_domain_intel.py" ]; then
  if [ -e "glitchbyte-phantom-labs" ]; then
    echo "Existing directory is not a verified clone. Inspect it manually."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
cd glitchbyte-phantom-labs

# 2. BUILD: this is a standalone Python 3 script; no compilation is needed.
python3 --version

# 3. TEST: syntax validation and CLI help. These do not contact a target.
python3 -m py_compile tools/glitchbyte_domain_intel.py
python3 tools/glitchbyte_domain_intel.py --help

# 4. RUN: only proceed for an authorized domain, entered by you.
echo "Enter a domain you own or are authorized to assess (e.g. your-own-site.org)."
read -r -p "Authorized domain (blank skips network access): " DOMAIN
if [ -z "$DOMAIN" ]; then
  echo "No domain entered. Build and syntax check are complete."
else
  mkdir -p "$WORKSPACE/reports"
  cd "$WORKSPACE/reports"
  # Mode 1 checks public DNS; choose mode 2-6 for additional lookups.
  python3 "$WORKSPACE/glitchbyte-phantom-labs/tools/glitchbyte_domain_intel.py" \
    "$DOMAIN" --mode 1 --no-color
  echo "JSON reports in $PWD:"
  find . -maxdepth 1 -type f -name 'glitchbyte_*.json' -print
fi

# 5. FIND RESULTS even if you chose not to run a lookup.
echo "Results directory: $WORKSPACE/reports"
echo "To inspect a saved report, run:"
echo 'python3 -m json.tool /path/to/glitchbyte_DOMAIN_TIMESTAMP.json | less'
```

**Optional extended DNS records:** If your system has `python3-venv` installed, you can create a private virtual environment inside `$HOME/PhantomLabsBuilds/domain-intel-station` and install `dnspython`. This is optional and not required for the recipe above:

```bash
cd "$HOME/PhantomLabsBuilds/domain-intel-station"
python3 -m venv .venv
.venv/bin/python -m pip install 'dnspython>=2.6,<3'
.venv/bin/python glitchbyte-phantom-labs/tools/glitchbyte_domain_intel.py --help
```

If `venv` is unavailable, install your distribution's `python3-venv` package first. External DNS and website results vary depending on the target and network.

### Run other modes from the report directory

Replace `your-authorized-domain.org` with a real domain you control or have permission to assess:

```bash
cd "$HOME/PhantomLabsBuilds/domain-intel-station/reports"
python3 ../glitchbyte-phantom-labs/tools/glitchbyte_domain_intel.py \
  your-authorized-domain.org --mode 6 --no-color
```

**Important:** Mode `6` sends several kinds of requests, including a request to an external RDAP service; use it only when those inquiries are appropriate. Mode `1` is the gentlest starting point.

## 📊 Reports: what gets saved?

A successful invocation writes **one JSON report** with a filename of this form, under the **current working directory**:

```text
glitchbyte_your-authorized-domain.org_YYYYMMDD_HHMMSS.json
```

The fields include `tool`, `domain`, `timestamp_utc`, `mode`, and `results`. The inner `results` depend on your selected mode. The existing script does **not** have a `--out` parameter or an HTML export.

To find and read your real report:

```bash
find "$HOME/PhantomLabsBuilds/domain-intel-station/reports" -type f -name 'glitchbyte_*.json'
python3 -m json.tool "/full/path/to/your-actual-report.json" | less
```

The example JSON filename above is a *pattern*, not proof that any real domain was queried here. Avoid putting private findings into public repositories.

## 🛠️ Troubleshooting

| Problem | Remedy |
| --- | --- |
| `python3` or `git` not found | Install through your distribution's package manager and reopen your terminal |
| `cd` fails | Verify your working directory with `pwd`; the recipe uses `~/PhantomLabsBuilds/domain-intel-station` |
| `No module named dns` / limited DNS output | Extended records are optional; use the isolated `dnspython` steps above |
| Timeout, certificate or HTTP error | Confirm connectivity, permission and target availability; check the `error` field in saved results |
| No JSON appears | Ensure a valid domain was entered; look in the directory from which the script was invoked |
| Redacted registration fields | RDAP services may hide registration data; don't infer absent private details |
| Results appear incomplete | Homepage fetch is bounded and follows only available links from that page, not every website page |
| Accidentally assessed the wrong domain | Stop and verify authorization before repeating checks |

## 🧪 Evidence and release status

The command line flags and output location above were confirmed from [the current Python source](../../tools/glitchbyte_domain_intel.py). Source inspection is **not** an end-to-end Ubuntu test, a successful live domain lookup, or verification of a vulnerability. The copy-and-paste recipe has not been executed against a live domain during this documentation build.

**Safety:** Use public information responsibly, follow [SECURITY.md](../../SECURITY.md), and respect the repository's [custom source-available license](../../LICENSE-NOTICE.md). Do not upload identifying private data, access credentials, session tokens or sensitive results.

[← PHANTOM TOOL VAULT](../TOOL_VAULT.md) · [← Official homepage](../../README.md)
