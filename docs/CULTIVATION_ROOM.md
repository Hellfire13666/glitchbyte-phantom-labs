<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-A5D600?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌱 Cultivation Room | Foundation & Building Lab

**Phantom Labs HQ** · Tool blueprints · Python 3 / Go · Ubuntu/Linux · Testing · Patches

> *Plant the concept. Build the engine. Test the roots.*

The Cultivation Room is **one of the three established laboratories**, not a fourth repository or a replacement for individual tool pages. Prototypes, installers, test recipes, docs and unique artwork begin here. Publish each finished tool to its own repository, then archive a checksum-verified version in Phantom Backup HQ.

<!-- GLITCHBYTE LAB NAV START -->
## 🧭 GLITCHBYTE LAB DOORS

| Destination | Enter the lab | Add files |
| --- | --- | --- |
| 👻 **Phantom Labs HQ** | [Main headquarters](https://github.com/Hellfire13666/glitchbyte-phantom-labs) | [📤 HQ file door](https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main) |
| 🌱 **Cultivation Room** | [Build and cultivation room](https://github.com/Hellfire13666/glitchbyte-phantom-labs/blob/main/docs/CULTIVATION_ROOM.md) | [📤 Build lab file door](https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main) |
| ⚡ **RosieRiot Overdrive** | [Overdrive tool repository](https://github.com/Hellfire13666/rosieriot-overdrive-2026) · [Lab room](https://github.com/Hellfire13666/glitchbyte-phantom-labs/blob/main/docs/ROSIERIOT_OVERDRIVE_LAB.md) | [📤 Overdrive file door](https://github.com/Hellfire13666/rosieriot-overdrive-2026/upload/main) |
| 🔐 **Phantom Backup HQ** | [Release and backup archive](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases) · [Tool Vault index](https://github.com/Hellfire13666/glitchbyte-phantom-labs/blob/main/docs/TOOL_VAULT.md) | [📤 Vault file door](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/upload/main) |

> **Vault rule:** Keep versioned archives and SHA-256 manifests. GitHub files are not a substitute for an independent offline backup. Never upload credentials or private reconnaissance reports to public repositories.

<!-- GLITCHBYTE LAB NAV END -->

## 🌈 Workshop-wide publishing rules

Use the [Build → Run → Publish → Vault standard](BUILD_PUBLICATION_STANDARD.md) for **every new project or requested upgrade**, whether Python, Go, local creative code, public intelligence, or Firefox tooling. Each build gets its own three [beginner runtime recipes](BEGINNER_RUNTIME_RECIPES.md), honest real-time output, optional saving where supported, distinct artwork, an individual setup page, and cross-links to HQ, Tool Vault, and the *verified* Backup HQ snapshot. Old working tools and past backup archives stay intact.

## 🧪 SUBDOMINATRIX current build stage

**Integration fix published:** independent 60-second Findomain timeout, partial hostname preservation, direct feedback for CLI failures and heartbeat output were added after the 51-name partial run. GitHub tests and the real Ubuntu run passed: 151 unique candidates, including 102 from Findomain in 40.45 seconds. [Full recipe](tool-showcases/SUBDOMINATRIX.md).



The [CI-reviewed terminal-only live signal upgrade](tool-showcases/SUBDOMINATRIX.md) has merged to HQ main. Its new `--terminal-only --color always` option prints public-source findings and skips report files/Firefox. Existing saved HTML/Firefox mode remains supported. Offline tests passed; the user's real Ubuntu public-source smoke test then succeeded with 151 unique hostname candidates, 102 Findomain records, and one explicitly saved TXT. The original legacy Firefox mode remains separately tested offline. Do not mark live field testing complete until results are observed.

## ⚡ Current workstation verification

**Findomain (external tool) passed its live public-source check** in 23 seconds. Its [diagnostic and Simple / Medium / Extra run recipes](integrations/FINDOMAIN_LIVE_CHECK.md) are published as a workshop integration guide. The user-local executable works; an older `/usr/bin/findomain` placeholder remains optional cleanup. No tool source or release archive was modified by that check.

## 💾 Universal easy-save implementation

[Easy Save for Every Tool](EASY_SAVE_ALL_TOOLS.md) is the source of truth for the native `-o name.txt` / `--o name.txt` future-build standard and the shared wrapper for existing command-line utilities. Every one of our 24 tool pages now explains how to use the save runner or the native option. This preserves existing source, built-in reports and Firefox workflows; interactive tools need their own exporter rather than assuming a pipe can capture state.

## 💾 New workshop save option

**Every future tool build or explicitly requested upgrade should offer simple output saving where practical:** `-o name.txt` writes human-readable results only if requested. Live terminal results should still appear. Document exact filename/path, TXT contents, non-overwrite behavior and exceptions. SUBDOMINATRIX has a tested implementation under review; older tools are not silently rewritten. [Publishing standard](BUILD_PUBLICATION_STANDARD.md) · [Subdominatrix](tool-showcases/SUBDOMINATRIX.md).


## Build path

1. Reserve a unique project name, Python filename, launcher name and report folder.
2. Build with offline demo and visible error handling.
3. Verify on Ubuntu/Linux without disturbing installed tools.
4. Create unique art, README, installation steps and a versioned ZIP.
5. Publish the tool to its own repository; archive its release in the Vault.

[🔍 Browse existing tools](../docs/ECOSYSTEM.md) · [🔐 Tool Vault](TOOL_VAULT.md)
