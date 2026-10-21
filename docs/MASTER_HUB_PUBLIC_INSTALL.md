# 🌹 GlitchByte Phantom Labs Master Hub v0.2.0

**One paste to install · One click to open · Independent tools stay intact**

This guide is for the downloadable Linux **offline** Master Hub. The hub provides Rosie-branded HTML tool navigation, manuals, recipe pages, a local installed-page finder, and desktop launchers. It is **not** a remote shell, it does not install other research tools, and clicking a **Copy** button does not execute the command.

> **Publication status:** The release ZIP is prepared and locally checked, but the GitHub release asset must be uploaded and checked before the single-paste public installer will work. See [Publication checklist](MASTER_HUB_PUBLIC_RELEASE.md). Do not announce the command as live until the release asset is actually downloadable.

## 🌱 One-square installer for your bros (after release publication)

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

Desktop Linux, `bash`, `python3`, `curl`, `unzip`, `sha256sum` and preferably `xdg-open` for launching in a browser. Debian 13 (Trixie) XFCE is the owner's field-tested desktop. Ubuntu **has not been personally verified** for this hub. The hub is local HTML and Python 3 standard-library code.

## ⚡ Open the hub again

```bash
bash "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/START_HUB.sh"
```

This refreshes the list of HTML pages from sibling tool directories and opens the index in your browser. Existing v0.1.0 folders and launcher entries are not overwritten. The installer also refuses to overwrite an existing v0.2.0 install or existing shortcut.

## 🖥️ Desktop shortcut instructions

After installation, look for **GlitchByte Phantom Labs Switchboard v2** in the application menu or for `GlitchByte-Phantom-Labs-Switchboard-v2.desktop` inside your Desktop folder. Right-click and select **Allow Launching** if your environment prompts for trust. Pin it to your desktop panel if desired.

**Debian XFCE special case:** If the file exists in Thunar's Desktop folder but you cannot see the icon on your wallpaper, right-click the wallpaper → **Desktop Settings** → **Icons** → choose **File/launcher icons**. Optionally run `xfdesktop --reload`. Enabling the setting affects visibility, not the actual installation.

## 🕷️ Using the tool switchboard

The hub has six logo cards: HEXBAZAAR, PHANTOM SPINE, RIFTSEAL, Report Vault, Recipe Library and Art Vault. Each card provides supported page links and tested recipes when available. **Open installed page** works only when a real local HTML file is discovered. A separate command-line tool may have no HTML page; use its documented command instead. Newly installed HTML-based tools appear in **Installed Page Finder** on the next launch; dedicated branded cards are added in later hub updates.

Never upload the locally generated `catalog.js`, private research reports, credentials, personal file paths, or machine-specific outputs to a public repository. `public-front-door.html` is a preview, not proof that a public web app is hosted.

## 🛡️ Verifiable scope

- Local v0.2.0 archive ZIP and its SHA-256 were verified; hub static file manifest, internal links and six logo SVGs passed checks.
- The standalone installer was checked in a clean isolated home directory, including desktop+menu shortcuts, repeat-install preservation and rejecting an invalid ZIP.
- A live Firefox/XFCE screen test of the new hub and a clean outside GitHub download remain for the owner or a volunteer. Container browser navigation was blocked by administrator policy, so we are **not** claiming a browser render pass.
- The repo's [custom source-available licensing notice](../LICENSE-NOTICE.md) allows use under its stated conditions; do not assume unrestricted open-source redistribution rights.

**GlitchByte Approved · Debian Trixie used · Ubuntu validation pending.**