# 🕷️ PHANTOM TOOL VAULT // PHASE 02

**The official GlitchByte Phantom Labs tool navigator.** Choose a project, read its documentation, test and run it locally. This page links to source code that exists in the repository, not hypothetical tools from design mockups.

![Official RosieGlitchbyte Phantom Labs](../artwork/labface2.png)

> **Vault inventory:** 16 Python scripts and one Go project checked against the GitHub `main` directory listing on 17 October 2026. All source links are relative, so they also work from a pull-request preview branch.

## 📋 The Phantom Build Recipe standard

**Every tool gets copy-and-paste terminal instructions right on its own page.** Each recipe covers **Install → Build → Test → Run → Find Results → Troubleshoot**. The steps must match that tool's real flags, requirements and report formats, with honest test status and permission checks for network research.

[👻 VOIDLANTERN's complete build recipe](tool-showcases/VOIDLANTERN.md#-copy--paste-build-recipe--ubuntu-or-linux-bash) · [🧪 Official showcase template](tool-showcases/SHOWCASE_TEMPLATE.md)

## ⚡ Spotlight: VOIDLANTERN

**Go • Website diagnostics • Local JSON output**

[👻 Read the illustrated-by-commands VOIDLANTERN showcase](tool-showcases/VOIDLANTERN.md) · [📁 Source + tests](../tools/go/voidlantern-go/) · [🧪 GitHub Go workflow](../.github/workflows/voidlantern-go-checks.yml)

Check HTTP status, elapsed time, up to five redirects, TLS certificate issuer/expiry and six HTTP security headers of a site you own or are authorized to assess. **This is not a penetration test, vulnerability confirmation, or bulk website crawler.**

## ✨ Python Spotlight: Log Constellation

**Offline log analysis · Python 3 · HTML + JSON reports**

[🌌 Read the Log Constellation showcase and complete build recipe](tool-showcases/LOG_CONSTELLATION.md) · [🐍 Actual Python source](../tools/glitchbyte_log_constellation.py)

The first-run recipe generates **safe sample logs without network requests**, performs Python syntax validation, creates an HTML dashboard and JSON report, and explains where to find the files.

## 🌐 Python Spotlight: Domain Intel

**Public domain research · Python 3 · DNS, website, links, TLS and RDAP**

[🌐 Complete Domain Intel showcase and copy-paste build recipe](tool-showcases/DOMAIN_INTEL.md) · [🐍 Python source](../tools/glitchbyte_domain_intel.py)

The initial Bash recipe checks requirements and syntax, then requests an authorized domain before performing a DNS lookup. It saves timestamped JSON reports outside the source tree.

## 🔎 Research and analysis

| Tool | Language | Source |
| --- | --- | --- |
| GlitchByte Domain Intel | Python | [Source](../tools/glitchbyte_domain_intel.py) · [Build recipe](tool-showcases/DOMAIN_INTEL.md) |
| GlitchByte Log Constellation | Python | [Source](../tools/glitchbyte_log_constellation.py) · [Build recipe](tool-showcases/LOG_CONSTELLATION.md) |
| GlitchByteRosie X Intel | Python | [glitchbyterosie_x_intel.py](../tools/glitchbyterosie_x_intel.py) |
| GlitchByteRosie X No API | Python | [glitchbyterosie_x_no_api.py](../tools/glitchbyterosie_x_no_api.py) |
| Rose Crawler | Python | [rose_crawler.py](../tools/rose_crawler.py) |
| Rosie IP Shadow Scraper | Python | [rosie_ip_shadow_scraper.py](../tools/rosie_ip_shadow_scraper.py) |
| Rosie Signal Garden | Python | [rosie_signal_garden.py](../tools/rosie_signal_garden.py) |
| Rosie Username Intel | Python | [rosie_username_intel.py](../tools/rosie_username_intel.py) |
| RosieGlitchbyte Domain Phantom | Python | [rosieglitchbyte_domain_phantom.py](../tools/rosieglitchbyte_domain_phantom.py) |
| RosieGlitchbyte IP Specter | Python | [rosieglitchbyte_ip_specter.py](../tools/rosieglitchbyte_ip_specter.py) |
| VOIDLANTERN | Go | [Project directory](../tools/go/voidlantern-go/) · [Showcase](tool-showcases/VOIDLANTERN.md) |

## 💗 Creative code and experiments

| Tool | Language | Source |
| --- | --- | --- |
| Rosie Catch Me Chaos | Python | [rosie_catch_me_chaos.py](../tools/rosie_catch_me_chaos.py) |
| Rosie Dark Desire | Python | [rosie_dark_desire.py](../tools/rosie_dark_desire.py) |
| Rosie Ghost Heart | Python | [rosie_ghost_heart.py](../tools/rosie_ghost_heart.py) |
| Rosie Hide Seek | Python | [rosie_hide_seek.py](../tools/rosie_hide_seek.py) |
| RosieGlitchbyte Hackgirl | Python | [rosieglitchbyte_hackgirl.py](../tools/rosieglitchbyte_hackgirl.py) |
| RosieGlitchbyte Neon Rose Phantom 3 | Python | [rosieglitchbyte_neon_rose_phantom_3.py](../tools/rosieglitchbyte_neon_rose_phantom_3.py) |

## 🧭 Start here

Clone the repo:

```bash
git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
cd glitchbyte-phantom-labs
```

List existing Python and Go modules:

```bash
find tools -type f \( -name '*.py' -o -name 'go.mod' \) | sort
```

Find any generated HTML, JSON and CSV files from the right working directory:

```bash
find . -type f \( -name '*.html' -o -name '*.json' -o -name '*.csv' \)
```

Read the [starter guide](TOOL_STARTER_GUIDE.md) for Python setup, Go compilation, local outputs and caveats.

## 🧪 Tool spotlight standard

Use the [tool showcase template](tool-showcases/SHOWCASE_TEMPLATE.md) when introducing another independent tool. The showcase must link to an existing source path, document the actual CLI rather than invent flags, list prerequisites and tests, show **clearly marked illustrative output**, cover limitations and public-data safety, and explain how to find generated reports.

A **source link is not a passing integration test**. Historic tools may need review before production use. In particular, read [SECURITY.md](../SECURITY.md) for the known unauthenticated TLS fingerprint issue in one Python tool. Do not interpret a username match as a confirmed identity.

**Source-available, not unrestricted open source:** consult [LICENSE-NOTICE.md](../LICENSE-NOTICE.md) before modification or redistribution.

[← Official homepage](../README.md) · [Full ecosystem](ECOSYSTEM.md) · [Official Rosie identity](ROSIE_VISUAL_STANDARD.md)
