<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF1493?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹 GLITCHBYTE PHANTOM LABS // FINAL WORKSHOP HANDOFF

**Status: offline workshop foundation VERIFIED · public live-network integrations NOT CERTIFIED**

The preservation, branding, navigation, tool-showcase and offline build-verification project is at its planned handoff point. This is a **documentation and offline-readiness milestone**, not a claim of a fully security-audited software release.

## What exists on main

| Item | Verified repository state |
| --- | --- |
| Python scripts | **16** top-level `tools/*.py` |
| Go project | **1** VOIDLANTERN Go module |
| Individual showcases | **17**, each with a source link and first-run copy/paste recipe |
| Workshop identity | RosieGlitchByte homepage, approved preserved artwork and navigation |
| Tests | Python syntax/unit tests, recipe/link audit, safe offline tool execution, separate Go tests |
| Build recipes | All 17 published **first Bash blocks** executed under isolated Ubuntu CI homes |
| Distribution check | Real public GitHub HTTPS clone succeeded in Ubuntu CI |
| Recent targeted fixes | IP Shadow Scraper approved-artwork path, Rose Crawler dotted usernames, and collision-resistant filenames for these two tools |

## Latest confirmed evidence on main

At the final review on 17 October 2026, both GitHub Actions workflows were green at commit `ab30ac69402e6e4875e05042a2ad34dca5f55f2b`.

- [Python syntax and unit tests: passing](https://github.com/Hellfire13666/glitchbyte-phantom-labs/actions/runs/39086501654)
- [Public clone and offline Python/Go release check: passing](https://github.com/Hellfire13666/glitchbyte-phantom-labs/actions/runs/39086501666)

Prior evidence:

- [Phase 22: all 17 published first Bash blocks passed](CLEAN_BUILD_VERIFICATION.md)
- [Phase 23: real GitHub HTTPS clone validated](PUBLIC_CLONE_VERIFICATION.md)
- [Phase 24: source-grounded security review](RELEASE_READINESS_REVIEW.md)
- [Phase 25: artwork and report reliability fixes](PHASE25_RELIABILITY.md)

**CI scope matters:** Phase 22 rewrites the Git clone URL to a local checked-out repository to verify each first-run block reproducibly. Phase 23 separately confirms an actual HTTPS download. The public-clone workflow tests the downloaded public `main` copy; the Python PR workflow tests the proposed branch. Together they provide meaningful offline assurance, **not a comprehensive test of every live capability**.

## What is ready to use

The original offline games, local-file research tools, link generators and documented safe first-run operations can be used as a **tested educational/workshop baseline** in the supported Ubuntu CI environment. A maintainer can explore projects from the [Tool Vault](TOOL_VAULT.md), follow each dedicated recipe, and use the [starter guide](TOOL_STARTER_GUIDE.md) to troubleshoot.

The code is subject to the repository's [custom source-available license](../LICENSE-NOTICE.md). Public availability does **not** imply unrestricted redistribution rights.

## Open gates before a broader security-sensitive/public production release

1. **Credential and history audit:** Inspect all tracked files and reachable Git history for exposed secrets, identifiers, credentials and private research material. The CI tests do not perform this review. If any secrets are found, revoke/rotate them; removing a file alone does not protect old commits.
2. **Rights and distribution:** Confirm permissions for artwork, third-party assets, examples and code before making further redistribution claims. Retain the custom source-available license.
3. **Authorized live integration:** Test the applicable X API and public webpage modes only with permitted credentials, platform-policy review, and authorized targets. Confirm networking, redirects, TLS certificate behavior, rate limits, error handling and data retention.
4. **Other output filenames:** Audit remaining tools for fixed output names, same-second collisions and sensitive report handling. Phase 25 fixes only Rose Crawler and IP Shadow Scraper.
5. **Deployment decisions:** Resolve the archived nested-workshop question in the release checklist, document supported Linux/platform versions, and decide whether a release tag/archive is appropriate.

These gates remain **unchecked**, not quietly treated as completed.

## Maintenance instead of endless phases

For ordinary new features, create a separate branch and pull request. Preserve source, history, license, approved artwork and established tool identities unless a change is explicitly requested. New Python tools must include their own source-linked showcase, six-stage copy/paste recipe, offline tests where possible and a Tool Vault entry. The [automated audit](RECIPE_AUDIT.md) enforces existing showcase/link coverage.

### Short handoff checklist

- [x] Keep the original workshop and Rosie artwork intact.
- [x] Publish individual source-linked recipes for all 17 original tools.
- [x] Pass safe offline Python tests and Go test/build.
- [x] Pass all 17 safe first-run Bash blocks in isolated Ubuntu workspaces.
- [x] Verify an actual public GitHub HTTPS clone.
- [x] Fix targeted Phase 25 artwork and report naming issues.
- [ ] Complete independent source-history/privacy/asset-rights review.
- [ ] Complete permissioned live integration/security review before production claims.
- [ ] Choose any release tag and distribution scope after open checks are reviewed.

**Disposition:** Conclude the **original-workshop upgrade** as an offline-verified foundation when this handoff PR is approved. Keep the release checklist open for the work needed before security-sensitive deployment. Future projects can proceed independently without continually revisiting the foundational setup.

[← Homepage](../README.md) · [← Tool Vault](TOOL_VAULT.md) · [← Release checklist](RELEASE_CHECKLIST.md) · [← Security policy](../SECURITY.md)
