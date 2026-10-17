<div align="center">

# 🌹 GLITCHBYTE PHANTOM LABS

### 👻 ROSIEGLITCHBYTE // CYBER TOOL FORGE

<!--
OFFICIAL ROSIE HERO:
When the approved banner is uploaded to artwork/glitchbyte-phantom-labs-official-hero.png,
uncomment the following line to display it at the very top of the repository.
The official artwork must show brown eyes, black hair with electric-blue highlights.
Do not substitute an unfamiliar face.
<img src="artwork/glitchbyte-phantom-labs-official-hero.png" alt="Official RosieGlitchbyte Phantom Labs cyber workshop banner" width="100%" />
-->


**Public OSINT · Python 3 · Go · Ubuntu/Linux · Creative Coding**

![Python](https://img.shields.io/badge/Python-3.x-00D6F5?style=for-the-badge&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-1.21%2B-FF1493?style=for-the-badge&logo=go&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Terminal-9F5EFF?style=for-the-badge&logo=linux&logoColor=white)

> **Built in the shadows. Preserved in the code.**

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  GLITCHBYTE // PHANTOM LABS                            ┃
┃  [✓] PYTHON WORKSHOP      [✓] GO TOOL FORGE             ┃
┃  [✓] PUBLIC INTELLIGENCE [✓] CREATIVE EXPERIMENTS      ┃
┃                                                        ┃
┃  > Every project has its own identity.                  ┃
┃  > Build. Test. Run. Explore. █                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

[**🏠 Ecosystem**](#-whats-inside-the-lab) · [**🕷️ Tool gallery**](docs/TOOL_SHOWCASE.md) · [**📚 Start here**](docs/TOOL_STARTER_GUIDE.md) · [**📊 Results**](#-locate-your-html-json-and-csv-reports) · [**🛡️ Security**](SECURITY.md) · [**🌹 Artwork**](artwork/)

</div>

---

## 🕸️ The Phantom command ecosystem

```text
╔════════════════════════════════════════════════════════╗
║  ROSIE@PHANTOM-LABS:~$ ecosystem --open                ║
╠════════════════════════════════════════════════════════╣
║  01  START HERE    → setup, examples and documentation ║
║  02  PYTHON        → research tools and creative code  ║
║  03  GO            → compiled diagnostic utilities     ║
║  04  INTELLIGENCE  → public data, logs and link maps   ║
║  05  RESULTS       → HTML / JSON / CSV report reading   ║
║                                                        ║
║  > One tool. One identity. No accidental overwrites. █ ║
╚════════════════════════════════════════════════════════╝
```

| Launch pad | Destination |
| --- | --- |
| 🧭 **NEW HERE?** | [Open the installation and starter guide](docs/TOOL_STARTER_GUIDE.md) |
| 🕷️ **TOOLS** | [Browse our verified tool gallery](docs/TOOL_SHOWCASE.md) |
| 🐍 **PYTHON** | [Explore the Python projects](tools/) |
| ⚙️ **GO** | [Build and run VOIDLANTERN](tools/go/voidlantern-go/) |
| 🗃️ **RESULTS** | [Find and understand saved reports](docs/TOOL_STARTER_GUIDE.md#2-find-reports-and-clickable-links) |
| 🎨 **ARTWORK** | [View available artwork](artwork/) |

## ⚡ What's inside the lab?

A workshop of independent research utilities, Linux command-line experiments, and themed programming projects. Each creation has its own purpose and identity. **No project gets replaced unless a remake or upgrade is specifically requested.**

| 🧪 Lab station | Explore | What you'll find |
| --- | --- | --- |
| 🕷️ Web & domain intelligence | [Python tools](tools/) | Crawlers, domain and network-oriented utilities |
| 👻 Log & signal analysis | [Log Constellation](tools/glitchbyte_log_constellation.py) | Local log analysis |
| 🌹 Public username research | [Username Intel](tools/rosie_username_intel.py) | Username research utility |
| 💻 Go experiments | [VOIDLANTERN](tools/go/voidlantern-go/) | HTTP status, TLS, redirects and response-header diagnostics |
| 💗 Creative coding | [Python tools](tools/) | Games, puzzles and expressive experiments |
| 🎨 Rosie art corner | [Artwork](artwork/) | Companion original art |

[**Explore the detailed tool gallery →**](docs/TOOL_SHOWCASE.md)

## 🚀 Your first 60 seconds

```bash
git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
cd glitchbyte-phantom-labs

# Discover Python tools and Go projects:
find tools -type f \( -name '*.py' -o -name 'go.mod' \) | sort

# Check an individual Python script's supported arguments:
python3 tools/rose_crawler.py --help
```

Arguments differ by project. If a script does not support `--help`, consult its documentation or source before executing.

**Want to run Go?** VOIDLANTERN lives in [`tools/go/voidlantern-go/`](tools/go/voidlantern-go/). It has its own build steps, tests and README.

### 🔍 Locate your HTML, JSON and CSV reports

From the directory where you ran a tool:

```bash
find . -type f \( -name "*.html" -o -name "*.json" -o -name "*.csv" \)
```

That finds **files on your own computer**, not websites on the internet. Open HTML results in your browser and use JSON or CSV in your preferred analysis software. [Learn how to read your reports →](docs/TOOL_STARTER_GUIDE.md)

## ✨ The Phantom Labs development code

- **Originality:** unique names, source files, folders and report paths. Remakes/upgrades only when requested.
- **Live visibility:** network tools should show progress as checks finish wherever practical, with meaningful `FOUND`, `POSSIBLE`, `UNKNOWN` and error states.
- **Free-first public research:** prioritize permitted public information; respect limits, privacy and authorization.
- **Quality gate:** document how to install, build/test, run, and interpret outputs before release.
- **No false certainty:** a public username match is not proof that two accounts belong to the same person.
- **Protect the workshop:** use separate branches and pull requests; preserve existing creations.

[**Read the workshop's build and publishing checklist →**](docs/TOOL_STARTER_GUIDE.md)

## 🧰 Development checks

For the legacy Python collection, run from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q tools
```

For VOIDLANTERN, run from its individual Go module:

```bash
cd tools/go/voidlantern-go
go test ./...
go vet ./...
go build -o voidlantern .
```

Some tools require network access, optional dependencies or user-supplied API credentials. Syntax and unit tests do **not** constitute a complete integration or security audit.

## 🌹 Official Rosie artwork

Our approved creative direction uses **Rosie's brown eyes, dark hair with electric-blue highlights, and established reference variants**. The finalized hero illustration is being prepared for repository upload. The artwork slot above is intentionally disabled until the **approved image** exists in the repository. This keeps the real GitHub README from displaying a broken image or an unrelated replacement.

See the [official Rosie visual kit](docs/OFFICIAL_VISUAL_KIT.md) for the exact upload path, image requirements and publish instructions.

For a working public website with searchable cards, galleries and interactive controls, GitHub Pages would be a **separate future build**. This README is a real, navigable GitHub homepage, not an interactive web application.

## 🔐 Ownership, safety and release status

**Project publisher and attribution:** RosieGlitchByte.

Copyright © 2026 RosieGlitchByte, to the extent applicable. The workshop's custom source-available [license notice](LICENSE-NOTICE.md) permits downloading and running unmodified tools; modifications and redistribution require prior written permission. AI-assisted material may not qualify for copyright protection in all jurisdictions.

This repository is publicly accessible, but much of the original collection remains **preservation/release-candidate code**, not audited production software. Review [SECURITY.md](SECURITY.md) and [the release checklist](docs/RELEASE_CHECKLIST.md) before distributing a specific tool. Never commit passwords, session cookies, tokens, sensitive research reports, or private personal data.

---

<div align="center">

**🌹 GLITCHBYTE PHANTOM LABS · ROSIEGLITCHBYTE**

*One tool. One identity. Infinite creative directions.*

[Back to top ↑](#-glitchbyte-phantom-labs)

</div>
