<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF1493?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# RosieGlitchByte public release checklist

- [x] Preserve source and artwork in a downloadable archive
- [ ] Decide whether to remove the preserved nested workshop directory before public release
- [x] Verify Python source syntax and offline repository tests
- [x] Add `.gitignore`, security policy and CI workflow
- [x] Confirm the IP Shadow Scraper source requests certificate and IP-hostname verification, with offline mocked regression coverage (Phase 24)
- [ ] Validate IP-address TLS and certificate errors against an explicitly authorized live HTTPS endpoint
- [x] Run all 17 first-run Bash recipes in isolated Ubuntu CI workspaces (Phase 22; local Git remapping)
- [x] Confirm a real public HTTPS Git clone and offline Python/Go checks on Ubuntu (Phase 23)
- [ ] Future CLI tools: implement and test **both** native `-o name.txt` and `--o name.txt` when plain-text result export applies; default no TXT, preserve live output, no overwrite, and accurate content. Document exceptions for interactive/GUI workflows. All existing tool guides should reference the [universal transcript runner](EASY_SAVE_ALL_TOOLS.md) instead of inventing native support.
- [ ] Add a tested, beginner-friendly `-o name.txt` option on each **new or explicitly updated** terminal-first tool where meaningful; preserve screen output, avoid silent files/overwrites and document unsupported legacy flags. See [the standard](BUILD_PUBLICATION_STANDARD.md).
- [ ] For future releases follow the [Build → Run → Publish → Vault standard](BUILD_PUBLICATION_STANDARD.md): unique names/art, visible real feedback, real three-level recipes, accurate save/Firefox behavior, checked hub links, and **verified** new backup snapshots (never merely assumed)
- [ ] Perform tool-by-tool **live** functional, authorization, and platform compliance tests
- [ ] For each new or upgraded tool, include tested [SIMPLE / MEDIUM / EXTRA beginner recipes](BEGINNER_RUNTIME_RECIPES.md) with real commands, expected live feedback, runtime/timeout notes, optional save behavior, and Firefox instructions where supported (existing tools are not automatically retrofitted)
- [ ] Review all file contents and Git history for secrets and private data
- [x] Adopt a custom source-available license permitting unmodified use
- [ ] Confirm redistribution rights for all assets
- [x] Upload release candidate to private GitHub repository and verify GitHub Actions
- [x] Create and verify an independent local release backup

[🌹 Final workshop handoff and verification evidence](WORKSHOP_HANDOFF.md). The original workshop's offline setup milestone is complete, while live release and privacy gates remain open.

## 🛡️ Checklist #6: Runtime safety options confirmed, full audit still open

Ubuntu help-only checks confirmed that installed SUBDOMINATRIX offers an offline demo, terminal-only output, independent provider/tool timeouts, explicit DNS/HTTPS-check flags with a documented dependency, and native `-o` TXT saving. Triad Signal offers individual CLI timeouts, `--only` scopes and native `-o` / `--o`. The original installed SUBDOMINATRIX source lists only `-o` / `--output-txt`; a separate refreshed source was later downloaded, and its help confirmed native `--o`. **CLI flags are confirmed, but authorization enforcement, output privacy and production security readiness remain unverified.**

## 🔐 Checklist #7: TXT permission evidence

Actual Ubuntu `stat` detected a private Findomain transcript (`600`) and a less-private Triad Signal TXT (`664`). The user ran `chmod 600 ~/triad_check2.txt` and confirmed mode **0600** by `stat`. The updated [Triad Signal companion](integrations/TRIAD_SIGNAL_2026.md) uses explicit file mode `0600` on exclusively created `-o`/`--o` TXT output and includes an offline test under a permissive `umask 000`. Neither historical report permissions nor every other tool's saving logic have been retroactively changed. The overall audit remains open for token leaks, third-party data, dependency/source review, defaults, redirect handling and release archives.

## ✅ Ubuntu privacy milestone and next archive freshness gate

On October 19, 2026, the user ran `chmod 600 ~/triad_check2.txt` and confirmed the report became **0600**; `findomain_results.txt` was already **0600**. The separately downloaded patched `triad_signal_private_2026.py` exposed native `-o` / `--o`; the current HQ source passed its explicit-0600 permissive-umask regression tests. A separate updated SUBDOMINATRIX local file exposed `-o, --o, --output-txt`, and a real no-network, no-save synthetic terminal test reported **13 demo names, 5 overlapping**, no DNS/HTTP observations, no Firefox, no report files. This closes the *specific* output-permission finding, not the overall security audit. Full live authorization/security, old tool export audits, Git history and private-data gates remain open.

**Checklist #8 freshness note:** as inspected, Backup HQ's `snapshots/latest.json` points to the dated HQ `d6e4dc1fa836` archive and Overdrive `e26afde620b5` archive, which predate these later HQ source/documentation changes. A fresh, checksum-verified snapshot must exist before describing the latest privacy patch as backed up. [Latest index](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/snapshots/latest.json) · [Restore/verify guide](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/blob/main/docs/RESTORE_GUIDE.md).

## ✅ Checklist #8: Original local ZIP passed, updated HQ vault pending

User's Ubuntu read-only local backup test confirmed **Triad Forge original ZIP integrity PASS**, **8 of 8 installed files identical**, **0 differences**. Recorded local ZIP SHA-256: `c464d1809903749869a12fdde06af48bf76cc584c010fa9da415a63ab611b043`. This is a local identity fingerprint and comparison, not a separately retained offline backup. The GitHub Vault's `snapshots/latest.json` was separately checked and still identifies HQ backup source commit `d6e4dc1fa836`, earlier than the October 19 Triad Signal/security changes. **Do not check the current-source freshness gate until [Phantom Vault Versioned Backups](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases/actions/workflows/vault-backup.yml) has run and the newly indexed ZIP and SHA-256 sums have passed verification.**

## Additional unresolved release gates

- [x] Fix IP Shadow Scraper artwork lookup to use the existing repository `artwork/` file (Phase 25; no artwork bytes changed)
- [x] Prevent same-second filename reuse in Rose Crawler and IP Shadow Scraper with microsecond timestamps and randomized filename suffixes (Phase 25)
- [ ] Audit remaining tools for fixed-name outputs and timestamp collisions
- [x] Verify dotted-handle report names in Rose Crawler with regression tests (Phase 25)
- [ ] Review dependencies, automation permissions, network redirects and output privacy for production deployment

Offline tests do not establish live platform compliance, full security auditing, credential safety across Git history, or permission to scan a third-party target. See [Phase 24 readiness findings](RELEASE_READINESS_REVIEW.md).
