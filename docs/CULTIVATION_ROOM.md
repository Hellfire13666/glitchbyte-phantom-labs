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


## 🔧 Checklist #4: Triad Forge integration

The original local archive/install scripts for Amass, GAU and Waybackurls were inspected and all three executables were reported installed. In the first live pass, Waybackurls completed and returned 20 URL lines while Amass and GAU timed out at 45 seconds. A separate [Triad Signal companion with independent bounded timeouts, parallel feedback and `-o`/`--o` TXT](integrations/TRIAD_SIGNAL_2026.md) is published and GitHub CI-tested. The existing local Forge folder and ZIP are not changed; the separate companion has now been tested on Ubuntu, with live module retrieval still limited as documented below.

## ✅ Triad Signal Ubuntu field-result update

The [published Triad Signal companion](integrations/TRIAD_SIGNAL_2026.md) has now been run on Ubuntu: Amass reached its 65-second cap with zero accepted candidates (nameserver graph relationship notices were observed), GAU reached its 50-second cap with zero URLs and a nonfatal config warning, and Waybackurls exited successfully in 0.87 seconds with zero results. It displayed per-module feedback and saved the **explicitly requested but empty** `~/triad_check2.txt`. Its standalone source passed the GitHub Python and public-clone checks; the original local Triad Forge ZIP remains untouched. **Checklist #4 status: installed/execution/output flow checked, external-provider retrieval partially verified only.** Advance to link/document consistency (checklist #5) without claiming these missing candidate sets passed.

## 🛡️ Checklist #6: Ubuntu safety-flag inspection (October 19, 2026)

The user verified the installed SUBDOMINATRIX `--help` exposes `--offline-demo`, `--terminal-only`, opt-in `--dns-check` / `--http-check` (HTTP requires DNS), `--max-verify`, `--timeout`, `--cli-timeout`, and local `-o` / `--output-txt` saving. The installed Triad Signal `--help` exposes `--only`, separately bounded Amass/GAU/Waybackurls seconds, `--max-show`, and `-o` / `--o` saving. A cross-check of HQ main found the current SUBDOMINATRIX source additionally supports `--o`, so the user's locally installed earlier copy should be refreshed to a **separate filename** instead of overwritten. 

**Verified:** presence of documented CLI controls, not a complete security audit. Remaining gates: review actual active-check authorization, privacy and credential handling, redirects/limits, dependencies, and safe file output across older tools. No active scans were performed by this help-only inspection. See [security policy](../SECURITY.md) and [release checklist](RELEASE_CHECKLIST.md).

## 🔐 Checklist #7: Privacy finding and remediation

User-side `stat` showed `findomain_results.txt` mode **0600** and Triad Signal's `triad_check2.txt` mode **0664**. That is an actionable local-report privacy gap, although actual readability by other users also depends on parent-directory permissions. The user subsequently ran `chmod 600 ~/triad_check2.txt`, and a follow-up `stat` confirmed mode **0600**. [Triad Signal](integrations/TRIAD_SIGNAL_2026.md) has an explicit 0600 / exclusive-create source fix with an automated permissive-`umask` regression check, covering future opted-in outputs after the local script is refreshed. Scope is **one output path**, not a claim that all old tools, reports, Git history, token handling or third-party APIs are security-audited.

## ✅ Checklist #7: Confirmed Ubuntu privacy fix and offline validation (October 19, 2026)

User-side Ubuntu evidence after the Triad Signal [0600 private-TXT patch](integrations/TRIAD_SIGNAL_2026.md): `findomain_results.txt` was already mode **0600**, and the earlier `triad_check2.txt` was mode **0664** until the user ran `chmod 600 ~/triad_check2.txt`; a follow-up `stat` confirmed **0600**. The new Triad Signal source was downloaded to a **separate local filename** `triad_signal_private_2026.py` and its `--help` displayed `-o, --o`. The updated SUBDOMINATRIX source was separately downloaded to `subdominatrix_updated_2026.py` and its help likewise displayed `-o, --o, --output-txt`. Its `example.com --offline-demo --terminal-only --color always` run completed with **13 synthetic names, 5 multi-source**, **zero** public DNS/HTTPS observations, and printed `[DONE] SAVE OFF: no report files created; Firefox not opened`. No live scan or extra report was requested in that demo.

**Verified milestone:** identified existing report permissions fixed; updated launchers available; offline demonstration and no-save feedback ran in real Ubuntu. The lab-wide security review (credentials, Git history, all legacy tools, external policy compliance) remains an open release gate. For checklist #8, verify the old local Triad ZIP and compare [Vault latest backup index](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/snapshots/latest.json) against the current HQ commit; the most recently indexed snapshot predates these privacy/report updates, so do **not** claim the newest source is already archived.

## ✅ Checklist #8: Original Triad Forge ZIP verified on Ubuntu (October 19, 2026)

The user's read-only Python `zipfile.testzip()` and byte-for-byte installed-file comparison on `~/Downloads/glitchbyte_triad_forge_2026.zip` returned **`[PASS] ZIP integrity`**, **8/8 matching files**, and **0 differences** versus `~/PhantomLabsLaunchers/glitchbyte_triad_forge_2026/`. Local archive SHA-256: `c464d1809903749869a12fdde06af48bf76cc584c010fa9da415a63ab611b043`. This is a recorded fingerprint, not a signed third-party authenticity guarantee. The read-only test did not create a fresh backup or copy files elsewhere.

**Separate vault freshness gate remains open:** [Phantom Backup HQ's latest index](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/snapshots/latest.json) currently references HQ commit `d6e4dc1fa836`; later merged Triad Signal, permission fixes, and documentation changes are not in that indexed archive. The [Vault workflow](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/actions/workflows/vault-backup.yml) supports `workflow_dispatch` and rebuilds/checks hashes; verify a **new** indexed source commit, ZIP and `SHA256SUMS.txt` before marking latest HQ source as backed up. Historical local ZIP and public HQ source snapshots are different assets; the workflow only protects tracked, committed GitHub files.

## ✅ HEXWRAITH Privacy Edition v1.1.1 RC1: locally verified (October 19, 2026)

The user confirmed a separate locally packaged RC ZIP `~/Downloads/hexwraith_privacy_edition_v1_1_1_rc1.zip`, SHA-256 `c07edb3d12899b41b80052e82a3a7af70d3190ecbd6320bd1df51b91fe924782`. The `sha256sum -c` command returned **OK** and `unzip -tq` returned **No errors detected**. The local patched-source packaging process reported passing tests, valid ZIP, included manifest, no reports and unchanged working source. In prior Ubuntu tests, seven new report files were mode **0600** under permissive `umask 022`, all generated directories were private, and the complete local suite passed **14/14** tests. The RC packaging process additionally tested isolated copies of the patched implementation.

**Status:** locally verified release candidate; **not published to a HEXWRAITH GitHub repository or Phantom Backup HQ**. Preserve privacy of reports and do not mix local artifacts with public source archives. Full publication instructions, known limits and artifact fingerprint: [HEXWRAITH Privacy Edition RC1 release record](tool-showcases/HEXWRAITH_PRIVACY_EDITION_RC1.md). The previous Vault HQ backup predates this new documentation, and the local-only HEXWRAITH RC is not part of it.

## ✅ HEXWRAITH Privacy Edition v1.1.1 RC2: verified locally (October 19, 2026)

The user built a second ZIP while preserving RC1 and the working original HEXWRAITH installation. The RC2 local release archive `~/Downloads/hexwraith_privacy_edition_v1_1_1_rc2.zip` has SHA-256 `b1728a0b480eae045ad289e59a69b3d20fd79e787d81bf4561c9f9428bb800a7`. Ubuntu reported **14/14 patched-source tests passing**, **ZIP integrity PASS**, **per-file manifest hash PASS**, and `sha256sum -c` **OK**. The eight verified archive members are the license notice, README, manifest, two patched entry points, and three tests. No research report files appear in the ZIP listing. The custom Headquarters source-available license was included for copyright-holder review, not adopted as an OSI open-source license.

**RC2 is local only.** A standalone public HEXWRAITH repository has not yet been created and the RC2 ZIP has not been uploaded to Backup HQ. Next: stage reviewed source in a private directory, confirm publication rights/metadata, decide repository visibility, publish only approved files, validate clean clone and back up the newly published release. [RC2 release record](tool-showcases/HEXWRAITH_PRIVACY_EDITION_RC2.md).

## ✅ HEXWRAITH private RC2 tag verified (October 19, 2026)

The user published annotated Git tag `v1.1.1-rc2` on commit `4225c48bcfb4175f58b4781cb00054cd40dc71e3`. GitHub returned **private** visibility and confirmed `MANIFEST.json` and `README.md` accessible at that tag. The private repository clone already passed **14/14 tests**, its eight release files matched the verified RC2 ZIP, and the user successfully created/restored a local Git bundle with a passing checksum. This completes the private *tagged source* milestone, not a public release or independent encrypted backup. See [HEXWRAITH RC2 status](tool-showcases/HEXWRAITH_PRIVACY_EDITION_RC2.md). Next practical protection: encrypt and store a separate off-device copy without adding private source to the public Vault.

## Build path

1. Reserve a unique project name, Python filename, launcher name and report folder.
2. Build with offline demo and visible error handling.
3. Verify on Ubuntu/Linux without disturbing installed tools.
4. Create unique art, README, installation steps and a versioned ZIP.
5. Publish the tool to its own repository; archive its release in the Vault.

[🔍 Browse existing tools](../docs/ECOSYSTEM.md) · [🔐 Tool Vault](TOOL_VAULT.md)
