# 🌹 HEXWRAITH Domain Atlas | Privacy Edition v1.1.1 RC2

**Status: verified source committed and tagged in a PRIVATE standalone HEXWRAITH GitHub repository; local RC2 ZIP and private Git bundle are validated. No public GitHub Release or off-device private backup yet.**

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

GitHub reports that [`Hellfire13666/hexwraith-domain-atlas-privacy-2026`](https://github.com/Hellfire13666/hexwraith-domain-atlas-privacy-2026) now exists with visibility **private** and default branch `main`. The nine expected tracked file paths were found through the authenticated GitHub connection: `.gitignore`, `LICENSE-NOTICE.md`, `MANIFEST.json`, `README.md`, both Python entry points, and three test files. The user subsequently supplied clean-clone verification and restore results: **14/14 tests passed**, eight release members matched and a Git bundle restored successfully (see below).

**Privacy boundary:** the existing `Hellfire13666/glitchbyte-phantom-labs-releases` Phantom Backup Vault is **public**, as is Headquarters. Do not add the private HEXWRAITH Git bundle, release ZIP, source files, or private reports to those public repositories without the owner's explicit decision to publish. A local private `git bundle` has now been created and restore-tested. For independent cloud redundancy, create a *separate private* backup repo before uploading. A private repository may have had a prior public window; changing GitHub visibility does not revoke copies someone downloaded earlier.

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

## ✅ Verified private RC2 Git tag (October 19, 2026)

The user ran `git push origin v1.1.1-rc2` and Ubuntu reported `[new tag] v1.1.1-rc2 -> v1.1.1-rc2`, `[PASS] Private release tag published`, and commit `4225c48bcfb4175f58b4781cb00054cd40dc71e3`. Using the authenticated GitHub connection, the repository visibility was rechecked as **private** and files `MANIFEST.json` and `README.md` were successfully fetched from ref `v1.1.1-rc2`, confirming GitHub resolves this tag to the expected RC2 source. The tag labels the existing nine-file Git commit. It is **not** a separate GitHub Release or an uploaded RC2 ZIP asset. [Private release tag](https://github.com/Hellfire13666/hexwraith-domain-atlas-privacy-2026/tree/v1.1.1-rc2) (accessible to authorized users only).

## ✅ GPG encrypted local backup created and decrypted (October 19, 2026)

The user ran an owner-only local GPG symmetric encryption command for the restore-tested HEXWRAITH Git bundle. Ubuntu showed `gpg: AES256.CFB encrypted data`, `gpg: encrypted with 1 passphrase`, and `[PASS] Encrypted backup created and decrypted successfully`. The resulting encrypted file is `~/HexwraithPrivateVault.P1kzcM/hexwraith_private_git_backup.bundle.gpg`. The original unencrypted bundle is preserved. The command created a separate adjacent SHA-256 checksum for the encrypted file.

**Remaining verification:** the user has not yet reported the command that compares the decrypted encrypted bundle's SHA-256 to the original plain Git bundle. No independent off-device copy has been confirmed. Until then, distinguish successful GPG encryption/decryption from byte-for-byte recovery verification and disaster-recovery redundancy. Never put the encrypted bundle or recovery passphrase in the public Headquarters/Phantom Vault repositories. The user's GPG passphrase must never be entered into a chat or public source file.

## ✅ Encrypted Git bundle integrity and byte-for-byte recovery verified (October 19, 2026)

The user reran checks locally against `~/HexwraithPrivateVault.P1kzcM/hexwraith_private_git_backup.bundle` and its GPG-encrypted counterpart. Both `sha256sum -c` checks returned **OK**; `gpg --decrypt` succeeded with AES256.CFB and a passphrase; the SHA-256 of decrypted output matched the SHA-256 of the original Git bundle. The command was streamed through `sha256sum` and did not save decrypted output as a separate file. This completes the **local encrypted backup integrity** milestone, in addition to the prior full Git bundle restore check.

The accompanying `lsblk` showed a single internal `nvme0n1` 953.9 GiB disk with partitions and no separately listed USB/removable storage. Therefore, **no external/off-device backup has been confirmed**. The recommended next step is attach an external storage device or choose a secure second destination, verify its mount location, copy only the `.gpg` file and its `.sha256` file, and validate the copied checksum. Do not copy the plaintext Git bundle to an untrusted destination or publish private source/bundles in the public Headquarters or Vault repositories.

## Suggested RC2 local release checks

```bash
cd "$HOME/Downloads"
sha256sum -c hexwraith_privacy_edition_v1_1_1_rc2.sha256
unzip -tq hexwraith_privacy_edition_v1_1_1_rc2.zip
unzip -Z -1 hexwraith_privacy_edition_v1_1_1_rc2.zip
```

Use a new, distinct, private staging directory rather than extracting over `~/PhantomLabsLaunchers/hexwraith_domain_atlas`. Audit source content and metadata for credentials/private information, confirm license ownership and terms, then test the staged package.

**Outstanding milestones:** review license terms/rights and full security implications before any public release, retain an encrypted off-device copy or separate private backup, and optionally create a formal private GitHub Release (a Git tag by itself is not a GitHub Release). Do **not** place private HEXWRAITH source/bundles in the existing public Vault. The local RC2 ZIP is not a GitHub Release asset.
