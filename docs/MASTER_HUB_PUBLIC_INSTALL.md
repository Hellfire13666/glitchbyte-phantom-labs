# 🌹 GlitchByte Phantom Labs Master Hub v0.2.0

**One paste to install · One click to open · Independent tools stay intact**

This guide is for the downloadable Linux **offline** Master Hub. The hub provides Rosie-branded HTML tool navigation, manuals, recipe pages, a local installed-page finder, and desktop launchers. It is **not** a remote shell, it does not install other research tools, and clicking a **Copy** button does not execute the command.

> **Release status: PUBLISHED.** [Official Master Hub v0.2.0 release](https://github.com/Hellfire13666/glitchbyte-phantom-labs/releases/tag/master-hub-v0.2.0) contains both the ZIP and checksum. GitHub's published ZIP digest matches the SHA-256 pinned by the installer. GitHub asset metadata and an owner-run Debian XFCE public-download smoke test both confirm the release archive integrity. A clean first-time installer run and full desktop/GUI interaction walkthrough remain to be verified. See the [release verification record](MASTER_HUB_PUBLIC_RELEASE.md).

## PHANTOM SPINE compatibility note (October 21, 2026)

The published Master Hub v0.2.0 remains unchanged and verified. Its built-in PHANTOM SPINE documentation is historical, and does **not** establish compatibility with newly installed HEXBAZAAR versions. For current HEXBAZAAR v0.1.2-rc1 adapter paths, see [PHANTOM SPINE adapter compatibility](PHANTOM_SPINE_ADAPTER_STATUS.md) and its [Debian field results](PHANTOM_SPINE_RC2_DEBIAN_FIELD_TEST.md). RC2's **HEXBAZAAR, native DNS, and RIFTSEAL** integrations now all have successful real Debian field evidence; **public packaging and release review are still pending**, so RC2 remains unpublished. After separately installing RC2, reopen Master Hub and select its new local HTML entry in Installed Page Finder; no new permanent Hub card is assumed. Only a tested and separately published Master Hub update may alter the built-in recipe.

## 🌱 One-square installer for your bros (public release)

Copy the *whole* block into a Linux terminal. It fetches the official installer script over HTTPS. The script downloads the pinned v0.2.0 ZIP from the official GitHub release, checks its SHA-256 and archive paths, safely installs to your home directory, adds an application menu entry and a desktop shortcut, then opens the hub.

```bash
tmp="$(mktemp)" &&
curl -fsSL --proto '=https' --tlsv1.2 \
  'https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/install_glitchbyte_master_hub_v020.sh' \
  -o "$tmp" &&
bash "$tmp"; result=$?; rm -f -- "$tmp"; test "$result" -eq 0
```

You can [review the installer source](../scripts/install_glitchbyte_master_hub_v020.sh) first. The script pins SHA-256 `e5b1ef241ab8e3058fae593ecb1ea4fe26d95cdfb9eca1a0e84c656a1025fac7` to reject altered ZIP downloads. Its expected official GitHub release tag is `master-hub-v0.2.0` in this HQ repository. No `sudo` or system-wide Python installation is used.

### Requirements

Desktop Linux, `bash`, `python3`, `curl`, `unzip`, `sha256sum` and preferably `xdg-open` for launching in a browser. The owner's desktop is Debian 13 (Trixie) XFCE; earlier hub launch and shortcut use was confirmed. The owner successfully downloaded and verified the public ZIP and reopened an existing v0.2.0 hub on Debian XFCE; fresh-account installation and all interactive buttons still need real-machine checks. Ubuntu **has not been personally verified** for this hub. The hub is local HTML and Python 3 standard-library code.

## ⚡ Open the hub again

```bash
bash "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/START_HUB.sh"
```

This refreshes the list of HTML pages from sibling tool directories and opens the index in your browser. Existing v0.1.0 folders and launcher entries are not overwritten. The installer also refuses to overwrite an existing v0.2.0 install or existing shortcut.

## 🖥️ Desktop shortcut instructions

After installation, look for **GlitchByte Phantom Labs Switchboard v2** in the application menu or for `GlitchByte-Phantom-Labs-Switchboard-v2.desktop` inside your Desktop folder. Right-click and select **Allow Launching** if your environment prompts for trust. Pin it to your desktop panel if desired.

**Debian XFCE special case:** If the file exists in Thunar's Desktop folder but you cannot see the icon on your wallpaper, right-click the wallpaper → **Desktop Settings** → **Icons** → choose **File/launcher icons**. Optionally run `xfdesktop --reload`. Enabling the setting affects visibility, not the actual installation.

## 🕷️ Using the tool switchboard

The hub has six logo cards: HEXBAZAAR, PHANTOM SPINE, RIFTSEAL, Report Vault, Recipe Library and Art Vault. Each card provides supported page links and tested recipes when available. **Open installed page** works only when a real local HTML file is discovered. A separate command-line tool may have no HTML page; use its documented command instead. Newly installed HTML-based tools appear in **Installed Page Finder** on the next launch; dedicated branded cards are added in later hub updates. The [future tool registration standard](MASTER_HUB_TOOL_REGISTRATION.md) explains the one-square installer, tool pages, and branded hub integration expected of each new release.

Never upload the locally generated `catalog.js`, private research reports, credentials, personal file paths, or machine-specific outputs to a public repository. `public-front-door.html` is a preview, not proof that a public web app is hosted.

## 🛡️ Verifiable scope

- Local v0.2.0 archive ZIP and its SHA-256 were verified; hub static file manifest, internal links and six logo SVGs passed checks.
- The standalone installer was checked in a clean isolated home directory, including desktop+menu shortcuts, repeat-install preservation and rejecting an invalid ZIP.
- Published GitHub release **metadata** confirms the exact tag, ZIP asset (981,915 bytes), checksum asset and matching ZIP SHA-256. A direct external release-file download could not be performed in the container because DNS was unavailable.
- The owner's Debian XFCE screenshot shows the public ZIP download/checksum and hub verify script passing, and an actual PHANTOM SPINE recipe page visible in a browser. This is a public-download and existing-install browser-open smoke test, not a clean install or full UI acceptance test.
- The hub's card discovery, search, copy feedback, and no-installed-pages states passed Chromium DOM/JavaScript simulation; direct browser navigation was blocked by administrator policy here. Desktop v2 shortcut use and clicking every hub control have not yet been field-confirmed.
- The repo's [custom source-available licensing notice](../LICENSE-NOTICE.md) allows use under its stated conditions; do not assume unrestricted open-source redistribution rights.

**GlitchByte Approved · Debian Trixie used · Ubuntu validation pending.**