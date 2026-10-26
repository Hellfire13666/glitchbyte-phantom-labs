# 🌐 Master Hub v0.2.0 | Public release and verification record

**Status: public GitHub release published.** [Official release](https://github.com/Hellfire13666/glitchbyte-phantom-labs/releases/tag/master-hub-v0.2.0) with tag `master-hub-v0.2.0`.

The published GitHub asset metadata confirms these exact files:

| File | GitHub status |
| --- | --- |
| `glitchbyte-phantom-labs-master-hub-v0.2.0.zip` | Uploaded · 981,915 bytes |
| `glitchbyte-phantom-labs-master-hub-v0.2.0.sha256` | Uploaded · 112 bytes |

ZIP SHA-256 confirmed both in the local package and in the GitHub release asset digest:

```text
e5b1ef241ab8e3058fae593ecb1ea4fe26d95cdfb9eca1a0e84c656a1025fac7  glitchbyte-phantom-labs-master-hub-v0.2.0.zip
```

## Checks completed

- GitHub PR [#51](https://github.com/Hellfire13666/glitchbyte-phantom-labs/pull/51) merged; public installer, guide and README are on `main`. Four CI checks on its head commit reported success (two `verify`, two `public-clone`).
- Original release ZIP SHA-256, ZIP integrity, and packaged manifest: pass.
- Hub verification script: 28 original release files, ten HTML pages and six SVG switch badges verified.
- Internal HTML link/asset references after regenerating the installed-page catalog: **232 checked, 0 missing**.
- JavaScript interface simulation in Chromium using real `index.html` and `assets/hub.js`: discovered pages populate HEXBAZAAR/PHANTOM SPINE/RIFTSEAL cards; search filters; command-copy button gives feedback; empty installation disables missing destinations.
- Installer `bash -n`, fresh temporary Linux-home install, menu shortcut, desktop shortcut, re-install preserving files, and corrupt-ZIP rejection: pass.
- Source in GitHub `scripts/install_glitchbyte_master_hub_v020.sh` was fetched and matched the previously tested source text.

## Debian Trixie field result: public-download smoke test PASSED

**October 20, 2026, Linux desktop validation:** A documented test ran the documented public GitHub ZIP download check on the already installed local v0.2.0 hub. Their terminal showed:

- Release ZIP downloaded over HTTPS (curl completed; approximately 958 KiB as displayed).
- `sha256sum -c` returned success against the exact pinned release SHA-256.
- `unzip -tq` returned no ZIP-content errors.
- `python3 -B "$HUB/scripts/verify_hub.py"` returned **28 release files verified**, all static HTML pages/local links verified, and all six branded SVG badges verified.
- `START_HUB.sh` refreshed the installed-page catalog, reporting **six HTML pages discovered**, without changing sibling tool folders.
- The terminal printed **`[PASS] PUBLIC DOWNLOAD AND HUB VERIFIED`**; a browser window displayed a **PHANTOM SPINE Connection Recipes** page.

This verifies an external release download and an existing local hub's re-open/render path on a Linux desktop. It **does not** establish a clean first-time public installer run, successful interaction with every navigation/copy button, verified desktop-shortcut v2 behavior, full accessibility, or compatibility across Linux distributions. The screenshot has not been uploaded to public GitHub because it contains device/user details.

## Remaining real-world validation and rights checks

- **Public download:** **Linux desktop test passed**, including ZIP checksum and integrity, as recorded above. This container could not repeat the external download because outbound DNS for github.com is blocked.
- **Real desktop GUI:** one hub-associated HTML recipe page was visible in a Linux desktop browser capture. **Individual links, copy actions, menu/desktop launcher activation, and a clean first-install are still unconfirmed**. Chromium in this test environment blocked direct `file://` navigation; simulation tests are separate evidence.
- **Additional Linux distributions:** not yet verified.
- **Distribution review:** confirm artwork redistribution rights and packaged contents against the repository's [custom source-available license](../LICENSE-NOTICE.md). No blanket open-source or security-certification claim is made.

## Final personal Debian XFCE check

1. Review and run [the one-square public installer](MASTER_HUB_PUBLIC_INSTALL.md) on a clean Linux user account, or reopen an existing local hub with `bash "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/START_HUB.sh"` (the installer will not overwrite it).
2. Confirm the Rosie homepage is visible, recipes/manual/gallery buttons open, the Installed Page Finder matches installed sibling tools, and each Copy button copies its displayed command.
3. Confirm the separate **GlitchByte Phantom Labs Switchboard v2** application-menu/desktop shortcut opens the correct hub. If needed in XFCE: right-click wallpaper → Desktop Settings → Icons → File/launcher icons.
4. Record results, any missing paths, and Firefox version. Do not expose private reports or the generated `catalog.js` on GitHub.

The hub is **published** and its offline build / installer have been verified. Real-world GUI acceptance and the above distribution review remain explicit, separate checks. Future tool entries follow the [tool registration standard](MASTER_HUB_TOOL_REGISTRATION.md).
