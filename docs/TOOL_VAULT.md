# 🕷️ PHANTOM TOOL VAULT // PHASE 02

**The official GlitchByte Phantom Labs tool navigator.** Choose a project, read its documentation, test and run it locally. This page links to source code that exists in the repository, not hypothetical tools from design mockups.

![Official RosieGlitchbyte Phantom Labs](../artwork/labface2.png)

> **Vault inventory:** 16 Python scripts and one Go project checked against the GitHub `main` directory listing on 17 October 2026. All source links are relative, so they also work from a pull-request preview branch.

[🧪 Phase 20 documentation audit and verification guide](RECIPE_AUDIT.md). The automated test checks all 17 source-linked showcases, recipe coverage, and local Markdown links on PRs after the audit merges.

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

## 🕵️ Python Spotlight: Rosie Username Intel

**Eight public profile links · Offline-first mode · JSON reporting**

[💙 Rosie Username Intel showcase and build recipe](tool-showcases/USERNAME_INTEL.md) · [🐍 Python source](../tools/rosie_username_intel.py)

The first-run Bash recipe checks syntax, prints the actual help, and generates eight links without accessing any social websites. An optional live mode checks only four platforms and distinguishes uncertain or rate-limited results.

## 🌹 Python Spotlight: Rose Crawler

**Twelve platform link destinations · Respectful optional public fetch · HTML, JSON and CSV**

[🌹 Rose Crawler showcase and complete Bash build recipe](tool-showcases/ROSE_CRAWLER.md) · [🐍 Original Python source](../tools/rose_crawler.py)

The first-run recipe generates candidate public profile links **offline**. An optional fetch mode checks robots.txt, applies a minimum delay and labels unverified and uncertain outcomes.

## 🌱 Python Spotlight: Rosie Signal Garden

**Offline note analysis · Source fingerprints · Searchable HTML, JSON and CSV**

[🌱 Rosie Signal Garden showcase and full Bash recipe](tool-showcases/SIGNAL_GARDEN.md) · [🐍 Actual Python source](../tools/rosie_signal_garden.py)

The first-run recipe uses harmless demo notes with no external website scans. The tool extracts links and date-looking entries from your own local files.

## 👻 Python Spotlight: Domain Phantom

**Eight modules · Public domain signals · Offline RDAP-link first run · JSON reports**

[👻 Domain Phantom showcase and copy-paste Bash recipe](tool-showcases/DOMAIN_PHANTOM.md) · [🐍 Python source](../tools/rosieglitchbyte_domain_phantom.py)

Start safely with mode 7, which constructs a public RDAP research link without connecting to a target. Other modes cover DNS, metadata, links, TLS and headers, with documented authorization and safety restrictions.

## 📡 Python Spotlight: IP Specter

**Offline IP classification · Optional public network research · JSON reports**

[📡 IP Specter showcase and complete Bash recipe](tool-showcases/IP_SPECTER.md) · [🐍 Python source](../tools/rosieglitchbyte_ip_specter.py)

The first run classifies a reserved documentation IP entirely offline. Additional public networking modes are documented separately, with authorization required for connectivity checks.

## 🌘 Python Spotlight: IP Shadow Scraper

**Nine modes · Offline-first IP classification · Optional public research · JSON archives**

[🌘 IP Shadow Scraper showcase and build recipe](tool-showcases/IP_SHADOW_SCRAPER.md) · [🐍 Original Python source](../tools/rosie_ip_shadow_scraper.py)

Start with mode 1, which classifies a reserved documentation address without contacting a target. The showcase documents permissions for network options, certificate verification, and a known companion-art placement mismatch.

## 🛰️ Python Spotlight: X Intel Phantom (Official API)

**Python 3.9+ · X API v2 · Credential-aware public research · JSON + CSV**

[🛰️ Official X Intel Phantom showcase and build recipe](tool-showcases/X_INTEL_PHANTOM.md) · [🐍 Python source](../tools/glitchbyterosie_x_intel.py)

Start with offline syntax/help checks. Live API operations require your own permitted developer bearer token and endpoint access, with private input instructions on the showcase page.

## 🪞 Python Spotlight: X Shadow Intel (No API)

**Offline post analysis · Public research links · JSON and CSV · No API token**

[🪞 X Shadow No-API showcase and complete Bash recipe](tool-showcases/X_SHADOW_NO_API.md) · [🐍 Original Python source](../tools/glitchbyterosie_x_no_api.py)

The first run analyzes fictional sample CSV posts entirely offline; keyword-only research URLs do not contact X. Profile metadata checks are optional and distinct from the official X API tool.

## 🦋 Python Spotlight: HackGirl Intel Workstation

**No X API token · Local CSV/JSON analysis · HTML dashboard · Public research links**

[🦋 HackGirl Intel showcase and complete Bash recipe](tool-showcases/HACKGIRL_INTEL.md) · [🐍 Original Python source](../tools/rosieglitchbyte_hackgirl.py)

The first-run recipe generates a uniquely named fictional CSV and analyzes it offline with a JSON report and HTML dashboard. Optional public profile metadata checks require a network request.

## 🌺 Python Spotlight: Neon Rose Phantom 3.0

**Eight domain modes · Safe offline RDAP-link first run · JSON archives**

[🌺 Neon Rose Phantom 3.0 showcase and complete Bash recipe](tool-showcases/NEON_ROSE_PHANTOM_3.md) · [🐍 Original source](../tools/rosieglitchbyte_neon_rose_phantom_3.py)

Its standalone recipe checks source syntax, produces a safe offline example report, validates the JSON, and explains optional authorized public-site checks.

## 🔎 Research and analysis

| Tool | Language | Source |
| --- | --- | --- |
| GlitchByte Domain Intel | Python | [Source](../tools/glitchbyte_domain_intel.py) · [Build recipe](tool-showcases/DOMAIN_INTEL.md) |
| GlitchByte Log Constellation | Python | [Source](../tools/glitchbyte_log_constellation.py) · [Build recipe](tool-showcases/LOG_CONSTELLATION.md) |
| GlitchByteRosie X Intel | Python | [Source](../tools/glitchbyterosie_x_intel.py) · [Build recipe](tool-showcases/X_INTEL_PHANTOM.md) |
| GlitchByteRosie X No API | Python | [Source](../tools/glitchbyterosie_x_no_api.py) · [Build recipe](tool-showcases/X_SHADOW_NO_API.md) |
| Rose Crawler | Python | [Source](../tools/rose_crawler.py) · [Build recipe](tool-showcases/ROSE_CRAWLER.md) |
| Rosie IP Shadow Scraper | Python | [Source](../tools/rosie_ip_shadow_scraper.py) · [Build recipe](tool-showcases/IP_SHADOW_SCRAPER.md) |
| Rosie Signal Garden | Python | [Source](../tools/rosie_signal_garden.py) · [Build recipe](tool-showcases/SIGNAL_GARDEN.md) |
| Rosie Username Intel | Python | [Source](../tools/rosie_username_intel.py) · [Build recipe](tool-showcases/USERNAME_INTEL.md) |
| RosieGlitchbyte Domain Phantom | Python | [Source](../tools/rosieglitchbyte_domain_phantom.py) · [Build recipe](tool-showcases/DOMAIN_PHANTOM.md) |
| RosieGlitchbyte IP Specter | Python | [Source](../tools/rosieglitchbyte_ip_specter.py) · [Build recipe](tool-showcases/IP_SPECTER.md) |
| VOIDLANTERN | Go | [Project directory](../tools/go/voidlantern-go/) · [Showcase](tool-showcases/VOIDLANTERN.md) |

## 💗 Creative Spotlight: Find Me If You Love Me

**Three-clue offline terminal romance puzzle · Real hex-encoded final letter · Unique transcript**

[💗 Find Me If You Love Me showcase and Bash build recipe](tool-showcases/FIND_ME_IF_YOU_LOVE_ME.md) · [🐍 Original Python source](../tools/rosie_hide_seek.py)

Its recipe checks the source and runs all three real puzzle gates in a controlled offline smoke test without modifying the game.

## ⚡ Creative Spotlight: Catch Me in the Chaos

**Three-lock offline terminal love puzzle · Hex-decoded letter · Unique transcript**

[⚡ Catch Me in the Chaos showcase and Bash build recipe](tool-showcases/CATCH_ME_IN_THE_CHAOS.md) · [🐍 Original Python source](../tools/rosie_catch_me_chaos.py)

The first-run recipe performs the real game logic in memory, checks the three gates and finale, and saves a unique transcript without altering the source.

## 💗 Creative code and experiments

| Tool | Language | Source |
| --- | --- | --- |
| Rosie Catch Me Chaos | Python | [Source](../tools/rosie_catch_me_chaos.py) · [Build recipe](tool-showcases/CATCH_ME_IN_THE_CHAOS.md) |
| Rosie Dark Desire | Python | [Source](../tools/rosie_dark_desire.py) · [Build recipe](tool-showcases/DARK_DESIRE.md) |
| Rosie Ghost Heart | Python | [Source](../tools/rosie_ghost_heart.py) · [Build recipe](tool-showcases/GHOST_IN_MY_HEART.md) |
| Rosie Hide Seek | Python | [Source](../tools/rosie_hide_seek.py) · [Build recipe](tool-showcases/FIND_ME_IF_YOU_LOVE_ME.md) |
| RosieGlitchbyte Hackgirl | Python | [Source](../tools/rosieglitchbyte_hackgirl.py) · [Build recipe](tool-showcases/HACKGIRL_INTEL.md) |
| RosieGlitchbyte Neon Rose Phantom 3 | Python | [Source](../tools/rosieglitchbyte_neon_rose_phantom_3.py) · [Build recipe](tool-showcases/NEON_ROSE_PHANTOM_3.md) |

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
