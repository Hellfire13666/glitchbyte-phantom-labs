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

Ubuntu help-only checks confirmed that installed SUBDOMINATRIX offers an offline demo, terminal-only output, independent provider/tool timeouts, explicit DNS/HTTPS-check flags with a documented dependency, and native `-o` TXT saving. Triad Signal offers individual CLI timeouts, `--only` scopes and native `-o` / `--o`. The published SUBDOMINATRIX source supports `--o`, but the tested local copy is older and lists only `-o` / `--output-txt`. Keep that known-good local copy and download the updated source under a new name for a no-network `--help` check. **CLI flags are confirmed, but authorization enforcement, output privacy and production security readiness remain unverified.**

## 🔐 Checklist #7: TXT permission evidence

Actual Ubuntu `stat` detected a private Findomain transcript (`600`) and a less-private Triad Signal TXT (`664`). The user was instructed to run `chmod 600 ~/triad_check2.txt`; completion is not yet confirmed. The updated [Triad Signal companion](integrations/TRIAD_SIGNAL_2026.md) uses explicit file mode `0600` on exclusively created `-o`/`--o` TXT output and includes an offline test under a permissive `umask 000`. Neither historical report permissions nor every other tool's saving logic have been retroactively changed. The overall audit remains open for token leaks, third-party data, dependency/source review, defaults, redirect handling and release archives.

## Additional unresolved release gates

- [x] Fix IP Shadow Scraper artwork lookup to use the existing repository `artwork/` file (Phase 25; no artwork bytes changed)
- [x] Prevent same-second filename reuse in Rose Crawler and IP Shadow Scraper with microsecond timestamps and randomized filename suffixes (Phase 25)
- [ ] Audit remaining tools for fixed-name outputs and timestamp collisions
- [x] Verify dotted-handle report names in Rose Crawler with regression tests (Phase 25)
- [ ] Review dependencies, automation permissions, network redirects and output privacy for production deployment

Offline tests do not establish live platform compliance, full security auditing, credential safety across Git history, or permission to scan a third-party target. See [Phase 24 readiness findings](RELEASE_READINESS_REVIEW.md).
