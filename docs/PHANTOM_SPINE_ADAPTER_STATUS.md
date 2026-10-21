# 👻 PHANTOM SPINE | Adapter Compatibility and Live Status

**Lab reference: October 21, 2026.** This is the current version guide. The **Live Signal v0.2.0-rc2 HEXBAZAAR adapter has now passed a real owner-side Debian field run** (113 actual unique observations, 4 usable providers, 0 notices). Its independent native DNS and RIFTSEAL adapter field checks are still pending. This candidate has **not** been published to GitHub Releases or Installer Vault. See the [field evidence notes](PHANTOM_SPINE_RC2_DEBIAN_FIELD_TEST.md).

## Which version is which?

| Component | Actual role | Integration status |
| --- | --- | --- |
| Original PHANTOM SPINE v0.1.0 | Local workshop/orchestration, legacy HEXBAZAAR references | Historical, **not** confirmed compatible with later HEXBAZAAR |
| PHANTOM SPINE Quickstart/Visual Portal | HTML instructions, copy buttons and launchers | Does not by itself create live research |
| **PHANTOM SPINE Live Signal v0.2.0-rc2** | Genuine HTTPS DNS public data lookups; optional real v0.1.2 HEXBAZAAR subprocess; real local file hashing | Offline logic checks pass; **Debian HEXBAZAAR integration field PASS**, independent native DNS and RIFTSEAL field checks pending |
| HEXBAZAAR v0.1.2-rc1 Rosie Savage | Separate real public-provider engine | **PHANTOM SPINE RC2 end-to-end Debian live output confirmed** (4 usable providers, 113 unique observations, October 21, 2026) |
| RIFTSEAL Evidence Forge | Local read-only file SHA-256 | Standalone local hashing is real. PHANTOM SPINE `--via riftseal` bridge needs owner-side execution check |

## Exact verified HEXBAZAAR path

```text
~/PhantomLabsLaunchers/hexbazaar-savage-intel-shop-v0_1_2_rc1_rosie_savage/hexbazaar_savage_intel_shop_v0_1_2_rc1.py
```

Actual checked HEXBAZAAR v0.1.2 CLI supports:

```text
hexbazaar [--color {auto,always,never}] domain <public-domain> --live
  --providers dns,ripe,certspotter,urlscan
  --view full --timeout 4 --limit 100 --delay 1
```

PHANTOM SPINE RC2 starts that **real installed Python program** with these supported flags. Public providers can return no records, partial records, HTTP 429, 502, or timeouts; none of those are synthetic findings.

The original PHANTOM SPINE v0.1.0 expects obsolete v0.1.0 adapter locations. Older pages are historical references and must not be read as proof that the legacy connection passed. **RC2's v0.1.2 bridge did pass the owner-side Debian live test on October 21, 2026.**

## Real-domain field acceptance commands (after RC2 is installed)

Check installed adapter *files only*, offline:

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" shop
```

Real Google and Cloudflare public DNS-over-HTTPS lookup (Google: A, AAAA, MX, NS; Cloudflare: A, AAAA):

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" hunt example.com --engine native --providers dns --timeout 5
```

Real HEXBAZAAR public-provider subprocess test, using public domain `facebook.com`:

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" hunt facebook.com --engine hexbazaar --providers dns,ripe,certspotter,urlscan --timeout 4 --limit 100
```

Real independent local SHA-256 using an existing Master Hub file:

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" evidence --file "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/index.html" --via local
```

Optional real RIFTSEAL adapter check (requires separately installed Evidence Forge):

```bash
"$HOME/.local/bin/phantom-spine-live-rc2" evidence --file "$HOME/PhantomLabsLaunchers/glitchbyte-phantom-labs-master-hub-v0_2_0/index.html" --via riftseal
```

**What to report back for acceptance:** tool version, provider status, live source URL(s), true observation count, nonzero process exit/timeout if applicable; for RIFTSEAL, a matching real SHA-256 and byte count. Do not include private reports, tokens, emails, or sensitive identifiers. A tool being found by `shop` means file presence, **not** a verified real provider result.

## Which pages are current?

Use **PHANTOM SPINE Live Signal RC2's five local pages**: `index.html`, `examples.html`, `connections.html`, `adapter-guide.html`, `troubleshooting.html`. They contain 18 copyable commands and versioned compatibility notes. The installed RC2 page files predate the new owner-side HEXBAZAAR field confirmation; use this updated GitHub guide for the latest verification status. Its version-specific short alias `phantom-spine-live-rc2` preserves the original `phantom-spine-live` alias. Master Hub v0.2.0 currently discovers sibling `index.html` pages but its built-in historical PHANTOM SPINE card has **not** been rebuilt or republished; updating that fixed card requires another tested, versioned Master Hub release.

**Security and release gate:** Public-source passive lookups only, no credentials or account bypass. Local evidence uses files the operator selects. No provider data is faked; no reports are automatically saved. Do not publish the RC2 ZIP as a completed release or register it in the [Installer Vault](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/docs/INSTALLER_VAULT.md) until the **remaining native DNS and RIFTSEAL owner-side checks**, distribution review and release verification pass.

Related: [Live OSINT release standard](LIVE_OSINT_REAL_OUTPUT_STANDARD.md) · [Master Hub tool registration](MASTER_HUB_TOOL_REGISTRATION.md).
