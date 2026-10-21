# 🌹 GlitchByte Master Hub | New-tool registration standard

**One paste to install. One click to open. One front door for every independently released tool.**

This applies to **future GlitchByte Phantom Labs tools**. It does not claim that older projects have already been updated.

## Primary Start mode for real research

For each **network OSINT / OPSEC research tool** newly built or upgraded, the hub card should open with a genuine live-source Start command, actual tested public-domain examples, and real-time observations showing source URLs and provider status. Label synthetic/offline tests as **Tests**, never as the main research workflow. Every tool's start commands must be real, compatible with the installed executable version, simple to paste, and non-destructive. See [LIVE OPSEC / OSINT release requirements](LIVE_OSINT_REAL_OUTPUT_STANDARD.md).

For a local-only tool such as RIFTSEAL, the main command should do **real local-file hashing**, not fictitious network activity.

## Every future independent tool ships with

1. **Unique identity:** distinct project, package, Python/Go source filename, output/report names, artwork, GitHub repository and tool page. Never overwrite a working tool or the installed Master Hub.
2. **One-square beginner installer:** one tested terminal block with a real downloadable official release, pinned SHA-256 / manifest checks when packaged, no surprises or destructive overwrites, clear dependency failures, and an optional launch. Do not publish a download command before its release artifact is live. Users should be able to inspect script source before running it.
3. **Desktop launch:** a separately named menu/desktop shortcut when the tool supports a UI. Avoid editing older pinned icons. Provide XFCE help when icons are hidden.
4. **Easy / Medium / Savage recipe pages:** actual supported commands and prerequisites, meaning of output, timeouts and partial results, and truthful save/no-save and Firefox behavior. Copy controls copy text only, never execute shell commands through HTML.
5. **A home in the Master Hub:** dedicated logo/button and project identity for significant published tools, reliable recipes/manual links, status on installed pages, and clear missing-tool behavior.
6. **Publication and recovery:** checked links from HQ, Tool Vault and corresponding project page; version-specific install and verification evidence; private output excluded from public GitHub; verified snapshot/backups where part of the build standard.

## PHANTOM SPINE adapter version status

**Current guidance:** [PHANTOM SPINE exact adapter compatibility](PHANTOM_SPINE_ADAPTER_STATUS.md). The Live Signal **v0.2.0-rc2 local candidate** uses the real HEXBAZAAR **v0.1.2-rc1 Rosie Savage** script and real public-source requests. Its `shop` command detects files but does not verify successful live provider data. The **RC2 → HEXBAZAAR v0.1.2** end-to-end Debian public-source field run now passes (113 actual observations from 4 providers on October 21, 2026); **native DNS also passed (6 real records / 6 usable queries) and RIFTSEAL passed (two matching SHA-256 calculations on an 8,826-byte file)**. See [field test](PHANTOM_SPINE_RC2_DEBIAN_FIELD_TEST.md). The historical PHANTOM SPINE v0.1.0 and Master Hub v0.2.0 built-in recipe may reference older paths; do not silently overwrite released Hub files to change them. Updated RC2 pages appear through Installed Page Finder as a **separate** new installation.

## PHANTOM SPINE v0.2.0 public package status

The [v0.2.0 publication checkpoint](PHANTOM_SPINE_V020_PUBLICATION_CHECKPOINT.md) records the user's approved **Rosie and mechanical-spine** public artwork, a new standalone source-available landing page, 17 passing automated tests, an isolated versioned Linux install and the separately SHA-256-verified ZIP. The actual [PHANTOM SPINE v0.2.0 public GitHub Release](https://github.com/Hellfire13666/phantom-spine-live-signal-2026/releases/tag/v0.2.0) and separate [verified PHANTOM SPINE v0.2.0 Installer Vault copy](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/tree/main/installers/phantom-spine-live-signal/v0.2.0) have now both been verified. **Only the new permanent Master Hub switch card remains pending**; publish it in a separate, tested versioned Master Hub upgrade, not by modifying v0.2.0 in place.



The current v0.2.0 `Installed Page Finder` discovers **HTML** pages directly inside sibling project folders under `~/PhantomLabsLaunchers/`, plus one `docs/*.html` level when the hub is launched via `START_HUB.sh`. It **does not** discover executable Python scripts as clickable HTML pages, install dependencies, run shell commands, or recursively search private directories.

A **new custom branded switch card** is added by building and publishing a new version of the Master Hub with real asset/link tests. It is **not automatically created** just because a new tool was installed. Until the hub is upgraded, the installed-page finder and the tool's GitHub guide provide discovery.

## Master Hub v0.3.0 candidate: permanent PHANTOM SPINE switch

The [v0.3.0 checkpoint](MASTER_HUB_V030_RELEASE_CHECKPOINT.md) records a separately versioned Hub package featuring the **already published** PHANTOM SPINE Live Signal v0.2.0, approved Rosie art, real live-domain recipes, and a unique Desktop v3 launcher. The candidate ZIP and checksum passed local testing, but the **Hub v0.3.0 GitHub Release and Installer Vault mirror remain pending** until the owner publishes the package and the real public copies are verified. Older Master Hub v0.2.0 files and pinned launchers stay unchanged.

## Required installer Vault registration

Before marking a **publicly released** tool complete, register its exact released ZIP and SHA-256 file under [Phantom Backup HQ approved installers](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/docs/INSTALLER_VAULT_REGISTRY.json), verify the workflow and actual new versioned archive, and confirm its [checksum entry](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/installers/SHA256SUMS.txt). A link alone is not a backup. Locally installed and unreleased tools do **not** get silently uploaded to GitHub.

## Release acceptance recipe

```text
BUILD -> TEST -> DOCUMENT -> BRAND -> PUBLISH TOOL -> VERIFY DOWNLOAD
      -> REGISTER IN MASTER HUB -> VERIFY NAVIGATION -> BACK UP
```

Review [one-paste Master Hub install](MASTER_HUB_PUBLIC_INSTALL.md), [v0.2.0 release evidence](MASTER_HUB_PUBLIC_RELEASE.md) and the [full publication standard](BUILD_PUBLICATION_STANDARD.md). Debian Trixie tests and Ubuntu tests must always be labeled separately.
