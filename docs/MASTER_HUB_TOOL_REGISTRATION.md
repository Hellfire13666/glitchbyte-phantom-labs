# 🌹 GlitchByte Master Hub | New-tool registration standard

**One paste to install. One click to open. One front door for every independently released tool.**

This applies to **future GlitchByte Phantom Labs tools**. It does not claim that older projects have already been updated.

## Every future independent tool ships with

1. **Unique identity:** distinct project, package, Python/Go source filename, output/report names, artwork, GitHub repository and tool page. Never overwrite a working tool or the installed Master Hub.
2. **One-square beginner installer:** one tested terminal block with a real downloadable official release, pinned SHA-256 / manifest checks when packaged, no surprises or destructive overwrites, clear dependency failures, and an optional launch. Do not publish a download command before its release artifact is live. Users should be able to inspect script source before running it.
3. **Desktop launch:** a separately named menu/desktop shortcut when the tool supports a UI. Avoid editing older pinned icons. Provide XFCE help when icons are hidden.
4. **Easy / Medium / Savage recipe pages:** actual supported commands and prerequisites, meaning of output, timeouts and partial results, and truthful save/no-save and Firefox behavior. Copy controls copy text only, never execute shell commands through HTML.
5. **A home in the Master Hub:** dedicated logo/button and project identity for significant published tools, reliable recipes/manual links, status on installed pages, and clear missing-tool behavior.
6. **Publication and recovery:** checked links from HQ, Tool Vault and corresponding project page; version-specific install and verification evidence; private output excluded from public GitHub; verified snapshot/backups where part of the build standard.

## How the hub finds tools

The current v0.2.0 `Installed Page Finder` discovers **HTML** pages directly inside sibling project folders under `~/PhantomLabsLaunchers/`, plus one `docs/*.html` level when the hub is launched via `START_HUB.sh`. It **does not** discover executable Python scripts as clickable HTML pages, install dependencies, run shell commands, or recursively search private directories.

A **new custom branded switch card** is added by building and publishing a new version of the Master Hub with real asset/link tests. It is **not automatically created** just because a new tool was installed. Until the hub is upgraded, the installed-page finder and the tool's GitHub guide provide discovery.

## Release acceptance recipe

```text
BUILD -> TEST -> DOCUMENT -> BRAND -> PUBLISH TOOL -> VERIFY DOWNLOAD
      -> REGISTER IN MASTER HUB -> VERIFY NAVIGATION -> BACK UP
```

Review [one-paste Master Hub install](MASTER_HUB_PUBLIC_INSTALL.md), [v0.2.0 release evidence](MASTER_HUB_PUBLIC_RELEASE.md) and the [full publication standard](BUILD_PUBLICATION_STANDARD.md). Debian Trixie tests and Ubuntu tests must always be labeled separately.
