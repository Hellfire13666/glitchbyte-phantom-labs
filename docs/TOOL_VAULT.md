# 🕷️ PHANTOM TOOL VAULT // PHASE 02

**The official GlitchByte Phantom Labs tool navigator.** Choose a project, read its documentation, test and run it locally. This page links to source code that exists in the repository, not hypothetical tools from design mockups.

![Rosie Phantom Tool Vault](../artwork/vaultlab.png)

<!-- PHANTOM-DOOR-INDEX:START -->
## 🚪 All tool doors: find any project in two clicks

**24 independent tools**. Pick **Open source** for the real Python file or Go project, or **Setup guide** for exact Ubuntu commands, tests and output locations. GitHub shows code; it does not run programs in your browser.

**For every new tool:** create its unique source and setup guide, add one row here, and run `python3 -m unittest discover -s tests -v`. The `test_tool_vault_doors.py` guard checks that every published top-level/nested Python entry point and Go module is indexed.

### 🔎 Domain, network and public-intelligence doors

| Tool | Purpose | GitHub door | Start here |
| --- | --- | --- | --- |
| SUBDOMINATRIX | Passive subdomain discovery | [Open source](../tools/subdominatrix.py) | [Setup guide](tool-showcases/SUBDOMINATRIX.md) |
| Rosie Phantom Scan V2 | DNS, TLS and public-domain observations | [Open source](../tools/rosie_phantom_scan_v2.py) | [Setup guide](tool-showcases/ROSIE_PHANTOM_SCAN_V2.md) |
| GlitchByte Domain Intel | Public domain research | [Open source](../tools/glitchbyte_domain_intel.py) | [Setup guide](tool-showcases/DOMAIN_INTEL.md) |
| Domain Phantom | Domain investigation modes | [Open source](../tools/rosieglitchbyte_domain_phantom.py) | [Setup guide](tool-showcases/DOMAIN_PHANTOM.md) |
| Neon Rose Phantom 3.0 | Multi-mode domain research | [Open source](../tools/rosieglitchbyte_neon_rose_phantom_3.py) | [Setup guide](tool-showcases/NEON_ROSE_PHANTOM_3.md) |
| IP Specter | IP address classification | [Open source](../tools/rosieglitchbyte_ip_specter.py) | [Setup guide](tool-showcases/IP_SPECTER.md) |
| IP Shadow Scraper | IP signals and local reports | [Open source](../tools/rosie_ip_shadow_scraper.py) | [Setup guide](tool-showcases/IP_SHADOW_SCRAPER.md) |
| VOIDLANTERN (Go) | Authorized HTTP/TLS diagnostics | [Open project](../tools/go/voidlantern-go/) | [Setup guide](tool-showcases/VOIDLANTERN.md) |
| Rosie Username Intel | Public username research links | [Open source](../tools/rosie_username_intel.py) | [Setup guide](tool-showcases/USERNAME_INTEL.md) |
| VELVETECHO Persona Observatory | Colorful public username intelligence and offline masked phone-format scanning | [Open source](../tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py) | [Setup guide](tool-showcases/VELVETECHO.md) |
| Rose Crawler | Public-profile links and metadata | [Open source](../tools/rose_crawler.py) | [Setup guide](tool-showcases/ROSE_CRAWLER.md) |
| X Intel Phantom | Official X API research | [Open source](../tools/glitchbyterosie_x_intel.py) | [Setup guide](tool-showcases/X_INTEL_PHANTOM.md) |
| X Shadow Intel | Local X post analysis | [Open source](../tools/glitchbyterosie_x_no_api.py) | [Setup guide](tool-showcases/X_SHADOW_NO_API.md) |
| HackGirl Intel | Offline CSV/JSON investigations | [Open source](../tools/rosieglitchbyte_hackgirl.py) | [Setup guide](tool-showcases/HACKGIRL_INTEL.md) |

### 🧬 Local analysis and evidence doors

| Tool | Purpose | GitHub door | Start here |
| --- | --- | --- | --- |
| SCREAMFRAME Pixel Autopsy | Screenshot metadata and visual matches | [Open source](../tools/screamframe-pixel-autopsy/screamframe_pixel_autopsy.py) | [Setup guide](tool-showcases/SCREAMFRAME.md) |
| GHOSTMARK Integrity Atlas | Read-only file hashes and duplicates | [Open source](../tools/ghostmark_integrity_atlas.py) | [Setup guide](tool-showcases/GHOSTMARK.md) |
| Log Constellation | Offline local log analysis | [Open source](../tools/glitchbyte_log_constellation.py) | [Setup guide](tool-showcases/LOG_CONSTELLATION.md) |
| Rosie Signal Garden | Offline notes and source fingerprints | [Open source](../tools/rosie_signal_garden.py) | [Setup guide](tool-showcases/SIGNAL_GARDEN.md) |

### 💗 Creative code and puzzle doors

| Tool | Purpose | GitHub door | Start here |
| --- | --- | --- | --- |
| HEXWAKE Palette Foundry | Offline Glitch HEX palettes | [Open source](../tools/hexwake_palette_foundry.py) | [Setup guide](tool-showcases/HEXWAKE.md) |
| PHANTOM CIPHERBOX | Reversible codebreaking puzzles | [Open source](../tools/phantom_cipherbox.py) | [Setup guide](tool-showcases/PHANTOM_CIPHERBOX.md) |
| Catch Me in the Chaos | Three-lock terminal puzzle | [Open source](../tools/rosie_catch_me_chaos.py) | [Setup guide](tool-showcases/CATCH_ME_IN_THE_CHAOS.md) |
| Dark Desire | Encoded love message script | [Open source](../tools/rosie_dark_desire.py) | [Setup guide](tool-showcases/DARK_DESIRE.md) |
| Ghost in My Heart | Interactive romance game | [Open source](../tools/rosie_ghost_heart.py) | [Setup guide](tool-showcases/GHOST_IN_MY_HEART.md) |
| Find Me If You Love Me | Three-clue romantic puzzle | [Open source](../tools/rosie_hide_seek.py) | [Setup guide](tool-showcases/FIND_ME_IF_YOU_LOVE_ME.md) |

<!-- PHANTOM-DOOR-INDEX:END -->

> **Vault inventory:** 16 preserved original Python scripts, seven additional standalone Python tools (HEXWAKE, PHANTOM CIPHERBOX, ROSIE PHANTOM SCAN V2, GHOSTMARK, SUBDOMINATRIX, SCREAMFRAME and VELVETECHO), and the preserved VOIDLANTERN Go project. New tools merge only after their review PRs; linked sources are present on this branch.

[🧪 Phase 20 documentation audit and verification guide](RECIPE_AUDIT.md). The automated test checks all 17 source-linked showcases, recipe coverage, and local Markdown links on PRs after the audit merges.

[💙 Phase 21: Actual offline Ubuntu execution report](OFFLINE_VERIFICATION.md). This verifies local Python runs and artifact creation, not every live network integration or full new-machine build.

[🌹 Phase 22: All 17 first-run recipes passed in clean Ubuntu CI workspaces](CLEAN_BUILD_VERIFICATION.md). Network cloning was mapped to a local Git checkout, and optional live target checks are excluded.

[🌹 Phase 23: Public HTTPS clone and source-preservation verification](PUBLIC_CLONE_VERIFICATION.md). Ubuntu CI confirms real public download, offline Python tests and Go build.

[🛡️ Phase 24 security and release-readiness review](RELEASE_READINESS_REVIEW.md). Corrected an obsolete TLS warning while keeping live security checks and report/artwork issues open.

[🌹 Phase 25 artwork and filename reliability fixes](PHASE25_RELIABILITY.md). Targeted source adjustments and offline regression tests preserve the original artwork and report contents.

[🌹 Final workshop handoff and remaining release gates](WORKSHOP_HANDOFF.md). The offline build foundation is verified, but live integrations are not certified.

## 🌹⚡ ONE-PASTE OPEN COMMANDS // NO ATTACHMENTS

[**Copy, Paste & Open: HEXWAKE, CIPHERBOX, ROSIE PHANTOM SCAN V2, GHOSTMARK and SUBDOMINATRIX**](COPY_PASTE_OPEN.md) · [Launcher source](../scripts/phantom_quickopen.py). One command per tool downloads the official launcher, caches the published script in a separate home folder, generates HTML, and opens Firefox when available. The default network-capable scanner preview performs no live lookups. Original tools' own recipe pages remain available below.

## 🌹 New: VELVETECHO Persona Observatory

**Color-coded outcomes · public username candidates · opt-in authorized checks · offline phone-format inspector · private HTML/JSON/CSV exports.** [Open the real Python source](../tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py) · [Full Ubuntu recipe](tool-showcases/VELVETECHO.md). Phone input is masked by default and does not enumerate accounts, carriers, or owners.

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
| HEXWAKE Palette Foundry | Python | [Source](../tools/hexwake_palette_foundry.py) · [Build recipe](tool-showcases/HEXWAKE.md) |
| PHANTOM CIPHERBOX | Python | [Source](../tools/phantom_cipherbox.py) · [Build recipe](tool-showcases/PHANTOM_CIPHERBOX.md) |
| ROSIE PHANTOM SCAN V2 | Python | [Source](../tools/rosie_phantom_scan_v2.py) · [Build recipe](tool-showcases/ROSIE_PHANTOM_SCAN_V2.md) |
| GHOSTMARK Integrity Atlas | Python | [Source](../tools/ghostmark_integrity_atlas.py) · [Build recipe](tool-showcases/GHOSTMARK.md) |
| SUBDOMINATRIX | Python | [Source](../tools/subdominatrix.py) · [Build recipe](tool-showcases/SUBDOMINATRIX.md) |

## ⚡ NEW WORKSTATION: HEXWAKE Palette Foundry

**Original offline Glitch HEX generator · Reproducible color families · JSON, CSS and HTML gallery**

[⚡ HEXWAKE showcase and complete Bash recipe](tool-showcases/HEXWAKE.md) · [🐍 Actual new Python source](../tools/hexwake_palette_foundry.py) · [🧪 Offline tests](../tests/test_hexwake_palette_foundry.py)

Unlike the preserved research tools, HEXWAKE is a new design tool. It uses rotating neon palettes and glitch-effect parameters, writes three real offline report formats, and does not contact external services.

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


## ✦ SCREAMFRAME Pixel Autopsy (offline screenshots)

**Image metadata · SHA-256 exact duplicates · 64-bit difference-hash visual echoes · local HTML/JSON.** [Ubuntu setup and tests](tool-showcases/SCREAMFRAME.md) · [Standalone Python project](../tools/screamframe-pixel-autopsy/). Screenshots stay local. Matching imagery, edited EXIF and filename mismatches are clues only, never proof of identity or tampering.
