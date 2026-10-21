# 👻 PHANTOM SPINE v0.2.0 | Public release preparation checkpoint

**Date:** October 21, 2026 · **Stage:** public package READY, repository and actual GitHub Release **NOT YET PUBLISHED**.

PHANTOM SPINE's owner selected `spine4.png`, the exact full-width Rosie, blue-highlighted hacker, cat and glowing mechanical spine artwork. That image was copied byte-for-byte into the future release package as `assets/rosie-phantom-spine-approved.png`, and is featured in the functional `index.html` homepage. It was not replaced with a generated mock-up, and the homepage has actual HTML copy buttons and tested command examples.

## Independently verified local artifacts

| Item | Verified property |
| --- | --- |
| Versioned archive | `phantom-spine-live-signal-v0.2.0.zip`, 3,758,458 bytes |
| Official package SHA-256 | `946262cad583f4a22d82091a805da089b6ef68c16815316772f45fb51e87a4f7` |
| Exact selected artwork SHA-256 | `5c903ba9d080a5ac1efc1f7fc49618832346b8e16e8fed0bc31421d6f1559541` |
| Package manifest | 24 sha256-verified files plus MANIFEST.json |
| Regression tests | 17/17 pass, including real-format provider handling and HTML art/link/copy checks |
| Isolated Linux install | PASS, verified new versioned folder, `phantom-spine-live-v020` start, real local hashing, application/desktop shortcuts, older shortcut preserved |
| Public packaging notice | `LICENSE-NOTICE.md`: source-available / rights reserved (not an OSI open-source license) |
| Distribution guidance | Separate `PHANTOM-SPINE-v0.2.0-PUBLICATION-KIT.zip` and reviewed `PHANTOM-SPINE-v0.2.0-PUBLISH.sh` for the owner's authenticated GitHub CLI session |

This checkpoint records local artifact verification but is **not** proof a public GitHub asset, live webpage or Installer Vault mirror exists. Do not provide or advertise a public binary URL until one has actually been uploaded and its SHA-256 re-verified.

## Real owner-side Debian field-test support

The existing [official field record](PHANTOM_SPINE_RC2_DEBIAN_FIELD_TEST.md) establishes all three RC2 engine workflows in October 2026:

- Live HEXBAZAAR bridge: 113 genuine public-source observations, four usable providers, no notices.
- Native live HTTPS DNS: six genuine `example.com` observations, six usable DNS requests, none failed. Two successful Cloudflare HTTP responses provided zero accepted findings.
- Real installed RIFTSEAL bridge: matching independent SHA-256 calculations on a local 8,826-byte HTML file.

The final v0.2.0 package is the RC2 engine versioned separately with updated code labels, exact user-approved art and current instructions. Its **offline regression and isolated install tests** pass; don't claim the new v0.2.0 binary has received a separate owner-side Debian internet rerun unless the owner performs it.

## Next official publication gate

1. The owner uses the prepared publication kit in their authenticated GitHub CLI session to create dedicated public source repository `Hellfire13666/phantom-spine-live-signal-2026` and upload BOTH original ZIP and its `.sha256` asset to a **v0.2.0 GitHub Release**. The helper refuses to overwrite an existing repo and stages only release package files (no local reports or private screenshots).
2. Independently download the public GitHub ZIP and confirm SHA-256 `946262cad583f4a22d82091a805da089b6ef68c16815316772f45fb51e87a4f7`; run the published installer.
3. Register that *actually published* public release in the [approved Installer Vault registry](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/docs/INSTALLER_VAULT_REGISTRY.json), run its workflow and confirm that the mirror ZIP, checksum and `SHA256SUMS.txt` appear under a unique versioned directory.
4. Build a **new** Master Hub release to provide its own permanent PHANTOM SPINE v0.2.0 card and updated official install recipe. The existing published Master Hub v0.2.0 must remain untouched.

The work is safe public-source passive research and read-only local file evidence, not credential access, account bypass or private account scraping. See [Live OSINT Standard](LIVE_OSINT_REAL_OUTPUT_STANDARD.md) for the mandatory user-facing claims and verification boundaries.
