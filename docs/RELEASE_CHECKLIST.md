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

## ✅ HEXWRAITH RC1: local release gate passed; GitHub publication pending

Local Ubuntu results show the source-only `hexwraith_privacy_edition_v1_1_1_rc1.zip` was created with passed patched-source test gate and a manifest; its SHA-256 is `c07edb3d12899b41b80052e82a3a7af70d3190ecbd6320bd1df51b91fe924782`. `sha256sum -c` returned **OK**, `unzip -tq` reported **no errors**, and the original launcher was preserved. Previously, a private-report check on `--demo` created seven mode-`0600` files; the local suite passed 14 tests. This means the **local RC1 integrity/privacy test milestone is done**, not that the archive was uploaded, that the release is security certified, or that all tests require no network in every context. [Release record](tool-showcases/HEXWRAITH_PRIVACY_EDITION_RC1.md).

- [x] Create and locally verify source-only HEXWRAITH RC1 with checksum and zipped-manifest structure.
- [x] Test private generated reports with permissive shell umask.
- [ ] Review full ZIP member list, file contents, licenses, dependencies and metadata for publication safety.
- [ ] Publish a distinct HEXWRAITH source repository/release and verify a clean clone.
- [ ] Archive the new published source/release in Backup HQ and verify SHA-256.

## ✅ HEXWRAITH RC2: locally validated; publication outstanding

October 19, 2026 Ubuntu evidence: **14 patched-source tests passed**, RC2 ZIP checksum `b1728a0b480eae045ad289e59a69b3d20fd79e787d81bf4561c9f9428bb800a7` returned **OK** under `sha256sum -c`; ZIP test and per-file manifest hash verification also passed. The user listed **eight expected members** including `LICENSE-NOTICE.md`, two launchers, three tests, README and manifest. The previously verified RC1 and original working launcher were preserved. [Full RC2 record](tool-showcases/HEXWRAITH_PRIVACY_EDITION_RC2.md).

- [x] Package RC2 with the existing Headquarters source-available licensing notice as a candidate.
- [x] Retest patched-source behavior and verify local ZIP checksum + manifest.
- [ ] Review third-party rights, full packaged source, README/metadata, and intended reuse/license restrictions before publishing.
- [ ] Create or select the final standalone HEXWRAITH GitHub repository with explicit owner-approved visibility.
- [ ] Upload vetted release bytes, verify clone and test, then create a checksum-verified Vault backup.

## 🔐 HEXWRAITH local backup closed; independent copy remains open

- [x] Private RC2 source/tag verified and clean-clone tests passed (14/14), commit `4225c48bcfb4175f58b4781cb00054cd40dc71e3`.
- [x] Git history bundle generated, clone-restored, and validated by SHA-256.
- [x] GPG-encrypted bundle created, decrypted, and verified byte-for-byte against the original with **both** checksum files reporting OK.
- [ ] Create and verify an **independent off-device** copy of the encrypted `.gpg` bundle plus checksum. The user's device inventory showed only a single NVMe disk; this remains pending by explicit choice.
- [ ] Conduct any additional security/rights review before making HEXWRAITH public or posting a GitHub Release. The standalone source repository is currently private; do **not** use the public Backup Vault for its private data.

**Next active lab gate: audit remaining tools for fixed-name report overwrites, timestamp collisions and default file permissions**, preserving code/report confidentiality and avoiding live network scans. [HEXWRAITH RC2 evidence](tool-showcases/HEXWRAITH_PRIVACY_EDITION_RC2.md).

## Additional unresolved release gates

- [x] Fix IP Shadow Scraper artwork lookup to use the existing repository `artwork/` file (Phase 25; no artwork bytes changed)
- [x] Prevent same-second filename reuse in Rose Crawler and IP Shadow Scraper with microsecond timestamps and randomized filename suffixes (Phase 25)
- [ ] Audit remaining tools for fixed-name outputs and timestamp collisions
- [x] Verify dotted-handle report names in Rose Crawler with regression tests (Phase 25)
- [ ] Review dependencies, automation permissions, network redirects and output privacy for production deployment

Offline tests do not establish live platform compliance, full security auditing, credential safety across Git history, or permission to scan a third-party target. See [Phase 24 readiness findings](RELEASE_READINESS_REVIEW.md).
