# 🛡️ PHASE 24 // SECURITY AND RELEASE-READINESS REVIEW

**Scope: review of current preserved source and published release notes, not a complete security audit.**

[Security policy](../SECURITY.md) · [Release checklist](RELEASE_CHECKLIST.md) · [Offline TLS regression tests](../tests/test_ip_shadow_tls_policy.py) · [Tool Vault](TOOL_VAULT.md)

## Findings

| Area | Source-grounded finding | Action / status |
| --- | --- | --- |
| IP Shadow Scraper TLS | `tls()` uses `ssl.create_default_context()`, `check_hostname=True`, `verify_mode=ssl.CERT_REQUIRED`, and the target IP as `server_hostname` | **Corrected outdated security policy**; added mock-based regression tests |
| IP Shadow Scraper HTTPS HEAD | Uses Python's default verifying HTTPS context and collects response headers without storing Set-Cookie or authorization headers | Still requires explicit authorization, privacy review and permitted live validation |
| IP Shadow Scraper artwork | Optional viewer expects `tools/rosie_ip_shadow_art.png` while preserved art exists at `artwork/rosie_ip_shadow_art.png` | **Open**, separate source fix and owner review |
| Filename collisions | Some reports use second-resolution timestamps, and other demo options use fixed names | **Open**, avoid parallel/same-second runs or keep backups |
| Rose Crawler dotted handles | Uses `Path.with_suffix()` on a stem that can include periods | **Open**, source fix needed to avoid unintended filenames |
| Real-world integration | Live X API, public-page, authorized TLS, DNS and IP tests remain unverified | **Open**, do not claim production certification |
| Ownership and content | Custom source-available license and approved artwork are preserved | Redistribution and Git-history privacy review still required |

## Certificate behavior is not a blanket security guarantee

The original IP Shadow Scraper code requests an authenticated TLS context using the target **IP address** as the requested server name. Consequently, hostname-only certificates often **will not validate against an IP**. On a verification failure the tool records an error instead of a validated fingerprint. The new offline tests mock socket and TLS APIs to check that the correct parameters are requested and that certificate validation failure returns an error. **They do not establish that a real remote server has a trusted IP-address certificate.**

## Verification evidence and boundaries

- Phase 20 audited all 17 documentation pages and local links.
- Phase 21 executed safe offline Python test paths and artifacts on Ubuntu CI.
- Phase 22 executed the first published Bash block of all 17 tools in clean temporary Ubuntu workspaces with Git clones mapped to local checkout data.
- Phase 23 verified real public HTTPS cloning and offline Python/Go builds on GitHub-hosted Ubuntu.
- Phase 24 adds targeted TLS regression tests and corrects stale policy/checklist claims. A passing GitHub Actions run is required before marking these tests verified.

**Unresolved release work:** explicit authorization and platform-terms review for live operations, controlled real HTTPS/IP certificate checks, code/privacy security review, checking historical Git objects for secrets, artwork/redistribution rights, optional-art placement and report collision fixes.

## Safe commands for maintainers

From an existing repository checkout:

```bash
python3 -m unittest discover -s tests -p 'test_ip_shadow_tls_policy.py' -v
python3 -m unittest discover -s tests -v
```

No live website, personal identity, account or network target is contacted by these tests. Do not place tokens, cookies, private scans or raw personal records into public issues or build logs.

**Disposition:** Keep the collection labeled **release candidate with verified offline build paths**, not a comprehensively security-audited production suite.

[← Release checklist](RELEASE_CHECKLIST.md) · [← Homepage](../README.md)
