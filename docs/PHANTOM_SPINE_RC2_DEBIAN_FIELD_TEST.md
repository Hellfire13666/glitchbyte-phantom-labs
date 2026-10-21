# 👻 PHANTOM SPINE Live Signal v0.2.0-rc2 | Debian field acceptance

**Date:** October 21, 2026 · **Platform:** User's Debian XFCE Linux machine · **Status:** all three primary integration workflows have owner-side field evidence: HEXBAZAAR public research, native public DNS, and RIFTSEAL local verification. Public release packaging, licensing and Installer Vault archiving remain separate pending milestones.

## ✅ Actual PHANTOM SPINE → HEXBAZAAR v0.1.2 adapter: live field PASS

The owner supplied two screenshots of a local RC2 terminal run and recipe-page Copy feedback. The screenshots were reviewed privately and are **not posted to this public repository**; no account username, home-directory name, credentials, private reports or profile data are included here.

The running adapter identified itself as PHANTOM SPINE Live Signal Bridge v0.2.0-rc2 and launched the **installed real** HEXBAZAAR v0.1.2-rc1 Rosie Savage engine against the public domain `facebook.com`. Copying the browser recipe into the terminal was also shown working.

**Reproduction command** (runs passive public-source queries using the actual installed RC2 alias and HEXBAZAAR 0.1.2):

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" hunt facebook.com --engine hexbazaar --providers dns,ripe,certspotter,urlscan --timeout 4 --limit 100
```

**Observed run summary, from screenshots (not generated sample data):**

| Check | Screenshot evidence |
| --- | --- |
| Engine | PHANTOM SPINE v0.2.0-rc2 calling HEXBAZAAR v0.1.2-rc1 |
| Target | Public domain `facebook.com` |
| Source group | `dns,ripe,certspotter,urlscan` |
| Unique public-source observations | **113** |
| Usable providers | **4** |
| Provider notices | **0** |
| Progress/provenance | Actual finding lines and source URLs visible |
| Completion | `[DONE] HEXBAZAAR finished` |
| Output persistence | `[SAVE OFF]`; no report requested by PHANTOM SPINE |
| Browser recipe | Copy action returned `Copied real command` |

This establishes genuine PHANTOM SPINE **HEXBAZAAR subprocess integration with live public-provider output o

## ✅ Independent native HTTPS DNS: real Debian field PASS

**Owner-supplied terminal transcript** (not a mocked fixture): the installed PHANTOM SPINE RC2 native DNS engine made its own public HTTPS provider queries on October 21, 2026, at **16:26:28 UTC**, against the public domain `example.com`.

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" hunt example.com --engine native --providers dns --timeout 8
```

| Provider / query | Actual result | Transport status |
| --- | --- | --- |
| Google DNS / A | 2 actual public IPv4 addresses: `172.66.147.243`, `104.20.23.154` | HTTP 200, DNS 0 |
| Google DNS / AAAA | 2 actual public IPv6 addresses: `2606:4700:10::ac42:93f3`, `2606:4700:10::6814:179a` | HTTP 200, DNS 0 |
| Google DNS / MX | 0 accepted observations | HTTP 200, DNS 0 |
| Google DNS / NS | 2 records: `elliott.ns.cloudflare.com`, `hera.ns.cloudflare.com` | HTTP 200, DNS 0 |
| Cloudflare DNS / A | 0 accepted observations | HTTP 200, DNS 0 |
| Cloudflare DNS / AAAA | 0 accepted observations | HTTP 200, DNS 0 |

**Printed summary:** `UNIQUE PUBLIC OBSERVATIONS 6`; `PROVIDER QUERIES 6 usable / 0 failed | elapsed 11.0s`; `[SAVE OFF]`. Provider provenance was displayed as six exact URLs under `https://dns.google/resolve` and `https://cloudflare-dns.com/dns-query`, with matching `name=example.com&type=...` arguments.

**Important nuance:** `6 usable` means the six HTTPS DNS queries returned HTTP 200 and DNS 0, **not** that all six found records. Cloudflare's A and AAAA calls produced zero accepted observations in this run; the current transcript does not establish whether the provider's raw Answer arrays were empty or records were filtered by PHANTOM SPINE. Keep this explicitly visible rather than inferring matching results or claiming a source outage.

## ✅ Actual RIFTSEAL adapter: real Debian field PASS

The owner ran PHANTOM SPINE RC2's installed RIFTSEAL bridge against their Master Hub `index.html` (local file, no internet):

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" evidence \
  --file "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/index.html" \
  --via riftseal
```

The live terminal printed `ENGINE INSTALLED RIFTSEAL VERIFIED AGAINST LOCAL SHA256`, then:

- **SHA-256:** `b6dcac8c87d2f54cfc27c61a1ff12e5914789016985d428b89f4bd44a078ae4f`
- **BYTES:** `8826`
- **Result:** `[PASS] Two matching real calculations. No report or filename displayed.`

This confirms **the actual installed RIFTSEAL adapter round-trip and independent PHANTOM SPINE digest/byte-count comparison**, not merely successful local hashing. It does not establish an independent third-tool validation of the file contents, nor does it test every supported RIFTSEAL invocation.

## ✅ Release-candidate packaging QA, and what remains

An independent container-side verification of the original exact `phantom-spine-live-signal-v0.2.0-rc2.zip` confirmed on October 21, 2026:

- Pinned ZIP SHA-256 `17b1efb4bfc14896e9a4e44f24f24f047e6e0f926cf219e5b963f1c07b2a698a`; archive CRC/integrity check passed.
- Internal manifest verified **19 files** (20 ZIP members including the manifest itself).
- **13/13 Python offline regression tests passed**, plus shell launcher syntax checks.
- Earlier isolated installation/shortcut and HTML page/link checks are recorded in the corresponding RC2 QA report.
- All three primary engine modes have **real owner-side Debian field evidence** as of October 21, 2026. No need to run another fabricated demo to complete them.

**Outstanding release milestones:** review public package contents/rights/privacy and any necessary copyright/license notice; ensure dated acceptance results and correct instructions are included in the *new publicly distributed* artifact; publish a versioned official GitHub Release with a real ZIP and checksum; then archive the exact publicly approved ZIP/checksum via [Phantom Backup HQ Installer Vault](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/docs/INSTALLER_VAULT.md). The locally installed RC2 ZIP's README and HTML pages predate these field tests and still say pending; they are **historical unmodified RC2 files**, not an updated final published package. A future version should correct that without overwriting installed versions.

**Do not claim:** RC2 is already publicly released, that all public providers always find records, or that a Vault mirror exists before its actual checksum-verified copy is present.

Related: [Current adapter matrix](PHANTOM_SPINE_ADAPTER_STATUS.md) · [Live source standard](LIVE_OSINT_REAL_OUTPUT_STANDARD.md).
