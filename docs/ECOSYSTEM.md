<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF1493?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🕷️ GLITCHBYTE PHANTOM LABS // OFFICIAL ECOSYSTEM

**RosieGlitchbyte's original Linux, Python, Go, public-intelligence and creative-code workshop.**

This document is the live navigation hub for the repository. All linked tools below were checked against the paths that actually exist on the `main` branch on 17 October 2026. Prototypes discussed in chat are not treated as published until their source is committed here.

**Phase 2 is ready for review:** enter the [Phantom Tool Vault](TOOL_VAULT.md) for a categorized navigator, the dedicated [VOIDLANTERN showcase](tool-showcases/VOIDLANTERN.md) and a template for future spotlights.

## ⚡ One-paste launches

[Copy and paste commands that generate and open Firefox galleries](COPY_PASTE_OPEN.md) are now published for HEXWAKE, CIPHERBOX, ROSIE PHANTOM SCAN V2 and GHOSTMARK. [Launcher Python source](../scripts/phantom_quickopen.py). No Git pull, merge, or manual ChatGPT downloads required.

## 🧭 Five stations

| Station | What's here | Jump |
|---|---|---|
| 🐍 Python | Research, crawlers, experiments | [Python tools](../tools/) |
| ⚙️ Go | Independent compiled utilities | [VOIDLANTERN](../tools/go/voidlantern-go/) |
| 🔎 Public Intelligence | Domain, IP, username, web and local logs | [Research directory](#research-and-analysis) |
| 💗 Creative Coding | Games, love-coded ideas, interactive experiments | [Creative directory](#creative-code-and-experiments) |
| 📁 Output Reports | HTML, JSON, CSV discovery and reading | [Result guide](TOOL_STARTER_GUIDE.md#2-find-reports-and-clickable-links) |

## 🌹 New research workstation: SUBDOMINATRIX

[Real Python source](../tools/subdominatrix.py) · [Tool page and tested Ubuntu recipe](tool-showcases/SUBDOMINATRIX.md) · [Quick Open command](COPY_PASTE_OPEN.md). Multi-source public subdomain sightings with optional local Subfinder/Findomain, opt-in public-host DNS/HTTPS validation and HTML/CSV/JSON/TXT reporting. Decorative poster metrics are not scan results.

## 🔎 Research and analysis

| Tool | Source |
|---|---|
| GlitchByte Domain Intel | [glitchbyte_domain_intel.py](../tools/glitchbyte_domain_intel.py) |
| VELVETECHO Persona Observatory | [Python source](../tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py) · [Full setup and colorful outcome guide](tool-showcases/VELVETECHO.md) |
| ROSIE PHANTOM SCAN V2 | [Python source](../tools/rosie_phantom_scan_v2.py) · [Ubuntu showcase + WHOIS/Findomain](tool-showcases/ROSIE_PHANTOM_SCAN_V2.md) |
| GlitchByte Log Constellation | [glitchbyte_log_constellation.py](../tools/glitchbyte_log_constellation.py) |
| GHOSTMARK Integrity Atlas (offline local files) | [Python 3 source](../tools/ghostmark_integrity_atlas.py) · [Firefox dashboard + Ubuntu recipe](tool-showcases/GHOSTMARK.md) |
| GlitchByteRosie X Intel | [glitchbyterosie_x_intel.py](../tools/glitchbyterosie_x_intel.py) |
| GlitchByteRosie X No API | [glitchbyterosie_x_no_api.py](../tools/glitchbyterosie_x_no_api.py) |
| Rose Crawler | [rose_crawler.py](../tools/rose_crawler.py) |
| Rosie IP Shadow Scraper | [rosie_ip_shadow_scraper.py](../tools/rosie_ip_shadow_scraper.py) |
| Rosie Signal Garden | [rosie_signal_garden.py](../tools/rosie_signal_garden.py) |
| Rosie Username Intel | [rosie_username_intel.py](../tools/rosie_username_intel.py) |
| RosieGlitchbyte Domain Phantom | [rosieglitchbyte_domain_phantom.py](../tools/rosieglitchbyte_domain_phantom.py) |
| RosieGlitchbyte IP Specter | [rosieglitchbyte_ip_specter.py](../tools/rosieglitchbyte_ip_specter.py) |
| VOIDLANTERN (Go) | [tools/go/voidlantern-go](../tools/go/voidlantern-go/) |

## 💗 Creative code and experiments

| Tool | Source |
|---|---|
| Rosie Catch Me Chaos | [rosie_catch_me_chaos.py](../tools/rosie_catch_me_chaos.py) |
| Rosie Dark Desire | [rosie_dark_desire.py](../tools/rosie_dark_desire.py) |
| Rosie Ghost Heart | [rosie_ghost_heart.py](../tools/rosie_ghost_heart.py) |
| Rosie Hide Seek | [rosie_hide_seek.py](../tools/rosie_hide_seek.py) |
| RosieGlitchbyte Hackgirl | [rosieglitchbyte_hackgirl.py](../tools/rosieglitchbyte_hackgirl.py) |
| RosieGlitchbyte Neon Rose Phantom 3 | [rosieglitchbyte_neon_rose_phantom_3.py](../tools/rosieglitchbyte_neon_rose_phantom_3.py) |

## ⚡ New creative design workstation

| Tool | Source and recipe |
|---|---|
| HEXWAKE Palette Foundry | [Independent Python source](../tools/hexwake_palette_foundry.py) · [HTML, CSS and JSON recipe](tool-showcases/HEXWAKE.md) |

The original 17-tool collection remains preserved; HEXWAKE is an additional standalone creation.

## 🗝️ New offline codebreaking workstation

| Tool | Source and recipe |
|---|---|
| PHANTOM CIPHERBOX | [Independent Python source](../tools/phantom_cipherbox.py) · [Offline puzzle-maker and decoder recipe](tool-showcases/PHANTOM_CIPHERBOX.md) |

Separate from the original creative games, CIPHERBOX creates customizable real, reversible puzzles. Its answer keys intentionally contain the original plaintext and must not be shared.

## 🚀 Sample commands

### Python

```bash
git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
cd glitchbyte-phantom-labs
python3 tools/glitchbyte_log_constellation.py --help
```

Read each tool's supported flags or source; not all scripts expose identical options. To install shared optional dependencies, follow [Tool Starter Guide](TOOL_STARTER_GUIDE.md).

### Go

```bash
cd tools/go/voidlantern-go
go test ./...
go vet ./...
go build -o voidlantern .
./voidlantern -url https://example.com -out reports/example.json
```

### Locate saved reports

```bash
find . -type f \( -name "*.html" -o -name "*.json" -o -name "*.csv" \)
```

The command prints **local report paths**, not live profile links. Run from the correct folder. Some tools need a successful execution before any reports exist.

## 🧪 Creation standards

**All future tools and upgrades** should have:
1. Their own non-conflicting project names, filenames, folders, and report paths.
2. Real `--help` or documented usage, test commands, installation instructions and report examples.
3. Live per-site completion progress, when practical, and honest distinctions between matches, false positives, blocked requests and errors.
4. Preferably free, public, permitted sources while respecting authorization, privacy and service limits.
5. A new review branch/pull request, with no replacement of existing tools unless explicitly requested.
6. Clear test status; syntax validation is not proof that external websites were scanned successfully.

## 🔐 Existing protection

The repository's [license notice](../LICENSE-NOTICE.md), [security policy](../SECURITY.md) and [release checklist](RELEASE_CHECKLIST.md) remain authoritative. **Source-available is not necessarily open-source.** Do not assume third-party redistribution or modification is allowed.

> 🌹 One tool. One identity. Infinite creative directions.

[← Back to the homepage](../README.md)


## ✦ Newly built offline screenshot workshop: SCREAMFRAME

| New project | Source, recipe and tests |
|---|---|
| SCREAMFRAME Pixel Autopsy Studio | [Python tool](../tools/screamframe-pixel-autopsy/screamframe_pixel_autopsy.py) · [Ubuntu offline recipe](tool-showcases/SCREAMFRAME.md) · [8 offline tests](../tools/screamframe-pixel-autopsy/tests/test_screamframe_pixel_autopsy.py) |

This independent tool does not alter any previous Python or Go project. Local screenshot analysis is read-only; report filenames, digests and previews may be private.
