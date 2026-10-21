# 👻 PHANTOM SPINE Live Signal v0.2.0-rc2 | Debian field acceptance

**Date:** October 21, 2026 · **Platform:** User's Debian XFCE Linux machine · **Status:** one live engine accepted, two final checks pending.

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

This establishes genuine PHANTOM SPINE **HEXBAZAAR subprocess integration with live public-provider output on the owner's Debian machine**. The specific 113-observation total is a dated observation and **not** a promise of future provider results, identity attribution, or a claim all adapters are verified.

## ⏳ Still pending, before calling the full release accepted

1. **Independent native HTTPS DNS engine**. Run:
   ```bash
   "$HOME/.local/bin/phantom-spine-live-rc2" hunt example.com --engine native --providers dns --timeout 8
   ```
   Record the actual Google/Cloudflare source URLs and six-query summary; clear partial/failed provider status is also legitimate test feedback.
2. **Actual RIFTSEAL adapter round-trip and SHA-256 cross-check**. Run:
   ```bash
   "$HOME/.local/bin/phantom-spine-live-rc2" evidence --file "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/index.html" --via riftseal
   ```
   Expect two independently matching local digest and byte counts, or truthful adapter errors. Do **not** substitute a local-only hashing success for verification of the RIFTSEAL bridge.
3. Confirm remaining end-user page navigation, CLI launcher and packaging checks if the owner reports relevant problems; review public distribution terms and dependencies.

**Release gate:** This field pass does **not** mean the RC2 ZIP has been published to a GitHub Release or copied into Phantom Backup HQ Installer Vault. Preserve the original Master Hub v0.2.0 and PHANTOM SPINE installations; release only a tested, versioned package after the remaining acceptance checks.

Related: [Current adapter matrix](PHANTOM_SPINE_ADAPTER_STATUS.md) · [Live source standard](LIVE_OSINT_REAL_OUTPUT_STANDARD.md).
