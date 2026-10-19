# 🌹 HEXWRAITH Domain Atlas | Privacy Edition v1.1.1 RC2

**Status: locally verified, NOT yet published as a standalone HEXWRAITH repository or uploaded to Phantom Backup HQ.**

This record preserves the user's verified Ubuntu test results from October 19, 2026. It does not claim possession of the local ZIP, which exists only on the user's Ubuntu system until intentionally uploaded.

## Verified RC2 release identity

| Item | User-observed result |
| --- | --- |
| Local ZIP | `~/Downloads/hexwraith_privacy_edition_v1_1_1_rc2.zip` |
| SHA-256 | `b1728a0b480eae045ad289e59a69b3d20fd79e787d81bf4561c9f9428bb800a7` |
| Checksum sidecar | `~/Downloads/hexwraith_privacy_edition_v1_1_1_rc2.sha256` |
| Test suite | **14 tests, OK** for isolated copies of the patched implementation |
| User verification | `sha256sum -c` **OK**; `unzip -tq` **No errors detected** |
| Manifest | Per-file SHA-256 manifest validated successfully by local build |
| Original RC1 | Preserved unmodified, hash `c07edb3d12899b41b80052e82a3a7af70d3190ecbd6320bd1df51b91fe924782` |
| Private report files | Not listed among ZIP members |

## Eight exact ZIP members

1. `LICENSE-NOTICE.md`
2. `MANIFEST.json`
3. `README.md`
4. `hexwraith_domain_atlas.py`
5. `hexwraith_domain_atlas_private_2026.py`
6. `tests/test_429_guard.py`
7. `tests/test_hexwraith.py`
8. `tests/test_hexwraith_private_reports_2026.py`

All members reside under the top-level directory `hexwraith_privacy_edition_v1_1_1_rc2/`. User-side manifest validation, ZIP integrity, and explicit SHA-256 comparison succeeded. Both Python launchers in the RC2 ZIP are staged copies of the patched version; the previously installed original remains separate.

## What the current tests establish

The offline suite covered HTTP 429 and provider retry rules, rejection of unauthorized probing/crawling, domain and URL scoping/redaction, HTML escaping, and private-report generation under a permissive shell umask. In an earlier Ubuntu test the patched HEXWRAITH demo generated seven files of mode `0600` and owner-only report directories. Demo hostnames, HTTP results and source counts are clearly synthetic, not evidence of live discovery.

The main script import scan detected only Python standard-library modules. Optional external CLI tools such as Findomain/GAU are separate runtime dependencies when enabled in live modes.

## Licensing review and public release conditions

RC2 now contains the existing [GlitchByte Phantom Labs license notice](../../LICENSE-NOTICE.md), copied from a checksum-verified Headquarters archive. This is a **custom source-available license**, not an OSI-approved open-source license. It permits unmodified usage under conditions but restricts redistribution and modification without permission. Its notice links to the Headquarters issue tracker; verify that this is the intended permission-contact route for a separately published HEXWRAITH project. Only the rightful copyright holder can authorize the licensing of all included code, tests, assets, and third-party contributions.

The earlier RC1 pattern scan found no matches for four common credential-pattern categories; that screen is not a complete confidentiality review, and copying a notice into RC2 does not provide an exhaustive audit.

## 🔒 GitHub private repository confirmed (October 19, 2026)

GitHub reports that [`Hellfire13666/hexwraith-domain-atlas-privacy-2026`](https://github.com/Hellfire13666/hexwraith-domain-atlas-privacy-2026) now exists with visibility **private** and default branch `main`. The nine expected tracked file paths were found through the authenticated GitHub connection: `.gitignore`, `LICENSE-NOTICE.md`, `MANIFEST.json`, `README.md`, both Python entry points, and three test files. The user's Ubuntu-side clean-clone comparison/testing results have **not yet been supplied**, so do not mark the clean-clone verification as passed.

**Privacy boundary:** the existing `Hellfire13666/glitchbyte-phantom-labs-releases` Phantom Backup Vault is **public**, as is Headquarters. Do not add the private HEXWRAITH Git bundle, release ZIP, source files, or private reports to those public repositories without the owner's explicit decision to publish. A local private `git bundle` verified against the clean-cloned repository is the recommended next backup artifact. For independent cloud redundancy, create a *separate private* backup repo before uploading. A private repository may have had a prior public window; changing GitHub visibility does not revoke copies someone downloaded earlier.

## ✅ Private GitHub clean-clone and local Git bundle restore verified (October 19, 2026)

The authenticated GitHub connection verified commit `4225c48bcfb4175f58b4781cb00054cd40dc71e3` in the **private** [HEXWRAITH source repository](https://github.com/Hellfire13666/hexwraith-domain-atlas-privacy-2026). Commit title: `Release HEXWRAITH Privacy Edition v1.1.1 RC2`; the commit contains the nine expected tracked filenames.

The user's Ubuntu clean-clone/private-backup command reported:

- Clean clone and source-match gate completed before test execution.
- **14/14 tests passing** (`Ran 14 tests in 0.076s; OK`).
- `git bundle verify` reported **complete history**, including `main` and remote refs at commit `4225c48...`, and **bundle okay**.
- An independent `git clone` of the local bundle succeeded, and its restored HEAD matched the original source HEAD.
- `sha256sum -c` for the newly generated bundle returned **OK**.
- The private local backup artifact is `~/HexwraithPrivateVault.P1kzcM/hexwraith_private_git_backup.bundle`, with an adjacent `.sha256` file. The **actual bundle SHA-256 value was not pasted**, so do not invent it. The restore was performed locally and is not evidence of an encrypted or off-device backup.

**Status:** GitHub source verified and a recoverable **local** private Git bundle exists. An independent off-device/encrypted backup remains recommended. The existing Phantom Backup Vault is **public** and MUST NOT receive this private bundle/source unless the owner expressly decides to publish it. Git bundle files are not encrypted by default; private filesystem permissions are not a substitute for encryption. No further public-release decision has been made.

## Suggested safe staging checks before creating a public repository

```bash
cd "$HOME/Downloads"
sha256sum -c hexwraith_privacy_edition_v1_1_1_rc2.sha256
unzip -tq hexwraith_privacy_edition_v1_1_1_rc2.zip
unzip -Z -1 hexwraith_privacy_edition_v1_1_1_rc2.zip
```

Use a new, distinct, private staging directory rather than extracting over `~/PhantomLabsLaunchers/hexwraith_domain_atlas`. Audit source content and metadata for credentials/private information, confirm license ownership and terms, then test the staged package.

**Outstanding milestones:** explicit user choice of separate repository/visibility, repository publication of reviewed bytes, clean clone with passing offline tests, appropriate version/release tag, and a new checksum-verified Vault snapshot. The previous dated HQ snapshot contains source committed at that historical time, **not** the local-only RC2.
