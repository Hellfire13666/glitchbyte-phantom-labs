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

## 🛡️ Output Safety Audit: first Ubuntu inventory (October 19, 2026)

The user's read-only Python AST inventory of `~/PhantomLabsLaunchers` parsed **15 Python files** and identified **9 file paths with potential write operations**. This is **not** nine confirmed vulnerabilities. The returned candidate list was: `hexwraith_domain_atlas/hexwraith_domain_atlas_private_2026.py` (7 candidate writes), `hexwraith_domain_atlas/hexwraith_domain_atlas.py` (7), `subdominatrix_live_signal_2026/subdominatrix_live_signal_2026.py` (5), `subdominatrix_live_signal_2026/subdominatrix_updated_2026.py` (5), `rosieriot_overdrive_2026/rosieriot_overdrive.py` (4), `code/subdominatrix.py` (4), `velvetecho/velvetecho_persona_observatory.py` (4), `triad_signal_companion_2026/triad_signal_2026.py` (1), and `code/hexwake_palette_foundry.py` (1). Duplicate variants count separately in this output. The inventory inspects `.write_text()`, `.write_bytes()` and explicit write-mode `open()` calls and is not comprehensive for `subprocess`, other methods or shell scripts.

**First targeted review: VelvetEcho Persona Observatory** because its user/persona research reports deserve conservative private file permissions. Check its four write operations around source lines 319–328, directory creation, output naming and any existing report file permissions. **No patch or leak has been established** from this inventory alone. Conduct the next step read-only, and avoid printing private report contents or copying source into a public repository. The source for HEXWRAITH's *patched* version already has offline 0600/0700 regression coverage, while the original unpatched launcher remains separate. The next audit should also distinguish SUBDOMINATRIX and Triad Signal original/updated variants rather than treating them identically.

## ⚠️ VelvetEcho report-permissions finding: confirmed on Ubuntu (October 19, 2026)

The user's read-only inspection of `~/PhantomLabsLaunchers/velvetecho/velvetecho_persona_observatory.py` exposed `write_reports` at lines **311–329**. It uses `directory.mkdir(parents=True, exist_ok=True)`, two `Path.write_text()` calls and 2–3 `open('w')` file outputs (JSON, profile CSV, optional phone CSV, HTML), without an explicit restrictive umask or file mode; output basenames do use UTC microseconds plus a 3-byte random suffix. The user's `~/VelvetEchoReports` filesystem audit found **17 files with mode `0664` and one report directory with mode `0775`**. On normal Unix permission interpretation, `0664` permits group write and *other-user read* of file contents; `0775` permits traversal/read by other users and group directory write, making this a confirmed **local confidentiality/privacy exposure**, not just an audit candidate.

**Remediation pending user execution:** adjust the existing dedicated VelvetEcho report tree files to `0600`, directories to `0700` (without touching report contents), and verify. Separately create a new uniquely named patched copy of the VelvetEcho launcher implementing owner-only exclusive file creation for new reports and rejecting non-private/symlink output directories; preserve the known-good original and test a synthetic offline demo under permissive `umask 022` or `000`. Do not publish original persona/phone reports or claims of live identity attribution. The report basenames are already low-collision but `'w'` mode does not provide exclusive creation, so patch if appropriate. No code patch is claimed installed as of this checkpoint. Existing disclosures, if any, cannot be undone by later permission changes.

## ✅ VelvetEcho existing reports secured; patched offline demo passed (October 19, 2026)

The user executed the targeted Ubuntu permission repair in `~/VelvetEchoReports`, then verified **17 regular report files now mode `0600`**, **1 directory mode `0700`**, **0 identified symlinks** and `[PASS] Regular report files and directories are private`. The command changed local filesystem permission bits only; it did not delete or rewrite report contents. These changes cannot revoke previous access/copies, if any.

The separate launcher `~/PhantomLabsLaunchers/velvetecho/velvetecho_private_reports_2026.py` exists, and the user ran the synthetic offline demo twice: each reported `[PASS] Synthetic offline demo`, `[PASS] JSON, CSV and HTML reports generated`, **4 test report files with `0600`**, and **report directories with `0700`**, under a deliberately permissive process umask of `022`. This is a local test of that copy, not a claim that the original launcher was patched or that all unauthorized inputs/lifecycle paths were reviewed. The original program uses microsecond timestamps plus random suffixes; the patched copy changes creation/validation of outputs.

**Next gate:** install a separate permanent regression test for VelvetEcho's private report modes and rejection of existing nonprivate/symlink destination folders. Run offline, preserving existing reports and source, then consider a source-only backup and broader compatibility tests. Publishing source or real persona/phone outputs to public GitHub is not part of this phase.

## ✅ VelvetEcho private-output regression suite passed (October 19, 2026)

The user added a separate test at `~/PhantomLabsLaunchers/velvetecho/tests/test_velvetecho_private_reports_2026.py` and ran it against the preserved separate patched launcher `velvetecho_private_reports_2026.py`. Ubuntu reported `test_private_output ... ok`, `test_reject_permissive_directory ... ok`, `test_reject_symlink_directory ... ok`, and **`Ran 3 tests in 0.187s; OK`**. The private-output test checks four synthetic reports at mode `0600` and a directory at `0700`; the other tests verify no output is created in a mode-`0775` or symlinked target directory. An earlier separate dry run also passed twice under simulated permissive umask. The original VelvetEcho source remains intact, and the existing 17 reports already have mode `0600` in a `0700` directory.

**Verification scope:** these three tests cover specific output-privacy guards, not comprehensive privacy or security assurance. The symlink rejection applies to the supplied final report directory, not a full multi-component race-proof path audit. **Next gate:** locally archive only the original source, patched source and regression tests with a private mode-`0600` archive and checksum; never include generated persona/phone reports. A public GitHub upload is not authorized by this test result.

## ✅ Scoping checkpoint: Four-family output audit completed; residual risks documented (October 19, 2026)

The user's combined **read-only local Ubuntu inventory** reported the following evidence:

| Tool family | Source behavior found | User's filesystem evidence | Disposition |
| --- | --- | --- | --- |
| SUBDOMINATRIX | Three source variants with 5, 5 and 4 exclusive-open calls; no evidence of explicit private creation mode in the scanned variants | Default `~/SUBDOMINATRIX_REPORTS` folder absent | Collisions mitigated by exclusive creation; **future exported reports may inherit permissive umask**, so privacy defaults remain an open improvement. Do not disrupt live discovery during this scoped audit. |
| Triad Signal | One exclusive open; simplistic AST `PRIVATE CREATE MARKERS` returned NOT DETECTED | User's saved TXT mode **0600** | Already earlier verified private output and no immediate issue identified. HQ source uses explicit `os.open(..., 0o600)`; false-negative private-marker text check is not authoritative for all installed variants. |
| RosieRiot Overdrive | Four `write_text()` calls, no exclusive open calls found by this scanner | Default output paths/modes were **not** inspected in this run | **Unresolved** potential overwrite or permission behavior; no confirmed incident. Review relevant writer implementations in a future targeted pass, not as an emergency patch. |
| HEXWAKE Palette Foundry | One exclusive-open call for palette exports and randomized stems in maintained HQ source | Default `~/HexwakePaletteReports` folder absent | Output collision defenses present; permissions may inherit umask. Lower privacy impact for synthetic palettes, not identity reports. |

`[PRIVATE CREATE MARKERS] NOT DETECTED` is a heuristic based on string matching in source, **not proof that files are public or unsafe**. The custom AST inventory also does not cover all writer APIs, imports, shell scripts, or external tool outputs. No live scans, modification of the four tools, or proof of global security certification occurred.

**Scoped Output Safety Audit: COMPLETED**, with bounded open issues above and the earlier VelvetEcho fix/HEXWRAITH tests verified. User previously requested to resume the **Cultivation Room new-tool build phase** rather than indefinite ZIP and permissions rounds. Don't mark overall privacy/security audit complete; retain output-hardening improvements as tracked technical debt.

## Additional unresolved release gates

- [x] Fix IP Shadow Scraper artwork lookup to use the existing repository `artwork/` file (Phase 25; no artwork bytes changed)
- [x] Prevent same-second filename reuse in Rose Crawler and IP Shadow Scraper with microsecond timestamps and randomized filename suffixes (Phase 25)
- [ ] Audit remaining tools for fixed-name outputs and timestamp collisions
- [x] Verify dotted-handle report names in Rose Crawler with regression tests (Phase 25)
- [ ] Review dependencies, automation permissions, network redirects and output privacy for production deployment

Offline tests do not establish live platform compliance, full security auditing, credential safety across Git history, or permission to scan a third-party target. See [Phase 24 readiness findings](RELEASE_READINESS_REVIEW.md).
