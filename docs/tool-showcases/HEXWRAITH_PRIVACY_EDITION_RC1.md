# 🌹 HEXWRAITH Domain Atlas: Privacy Edition v1.1.1 RC1

**Status: locally built, tested and checksum-verified on Ubuntu on October 19, 2026. NOT yet uploaded to GitHub.** This page is a release-candidate record, not a claim that GitHub Headquarters or Phantom Backup HQ contains the ZIP/source.

## Release identity

| Property | Verified local result |
| --- | --- |
| ZIP | `~/Downloads/hexwraith_privacy_edition_v1_1_1_rc1.zip` |
| SHA-256 | `c07edb3d12899b41b80052e82a3a7af70d3190ecbd6320bd1df51b91fe924782` |
| Checksum file | `~/Downloads/hexwraith_privacy_edition_v1_1_1_rc1.sha256` |
| ZIP verification | `sha256sum -c` returned `OK`; `unzip -tq` returned `No errors detected` |
| Prior source-only safety copy | `~/Downloads/hexwraith_private_source_20261019.zip`; SHA-256 `c350fff48f82b0dd7887556112e950d653c3e21f404fd5f543e5b8df345f583f` |
| Source under test | Patched local copy, `hexwraith_domain_atlas_private_2026.py` |
| Package behavior | Staged patched implementation under standard and private filenames; README, JSON hash manifest and tests, with research reports excluded by the packaging script |
| Publication | **Pending**; neither public source nor a release ZIP has been uploaded as a result of this local build |

## Field validation on Ubuntu

- Existing local HEXWRAITH `reports/` directory changed to mode `0700` via `chmod -R go-rwx`. A subsequent `find` reported **zero files with group/other permission bits**.
- Local patched script was created separately with mode `0600` and `--help` succeeded. Original launcher was preserved.
- Patched `--demo --tools none --out <isolated temporary directory>` was run from a process with permissive `umask 022`; the **seven** generated JSON/HTML/CSV/TXT outputs each had mode `0600`, and all generated directories passed the private-permission check.
- A new `test_hexwraith_private_reports_2026.py` regression test passed (1/1).
- The local complete suite including authorization rejection, rate-limit/HTTP 429 behavior, URL scoping/redaction, HTML escaping and privacy testing reported **14 tests, OK**. The test runner's deliberate `triad/HEXWRAITH: error`/429 notices are expected negative-path behavior.
- The RC1 packaging step **separately tested temporary copies of the patched source** and reported `[PASS] Patched-source tests`, `[PASS] ZIP integrity`, `[PASS] Manifest created`, `[PASS] Reports excluded` and `[PASS] Existing programs preserved`.
- **Offline/demo data are synthetic.** Passing tests do not establish provider reliability, permission for third-party scans or a complete production security audit.

## Verify the local candidate (Ubuntu)

```bash
cd "$HOME/Downloads"
sha256sum -c hexwraith_privacy_edition_v1_1_1_rc1.sha256
unzip -tq hexwraith_privacy_edition_v1_1_1_rc1.zip
unzip -Z -1 hexwraith_privacy_edition_v1_1_1_rc1.zip
```

Expected: checksum `OK`, no ZIP integrity errors. Review the complete file list **before public release** to confirm only the intended source/tests/README/manifest are present.

## Install in a separate folder and run the offline demo

Do not overwrite the known-good local `~/PhantomLabsLaunchers/hexwraith_domain_atlas/` installation while testing the candidate.

```bash
mkdir -p "$HOME/HexwraithRC1Review"
unzip -n "$HOME/Downloads/hexwraith_privacy_edition_v1_1_1_rc1.zip" -d "$HOME/HexwraithRC1Review"
cd "$HOME/HexwraithRC1Review/hexwraith_privacy_edition_v1_1_1_rc1"
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 -B hexwraith_domain_atlas.py --demo --tools none --out ./reports --color always
```

The demo uses illustrative host/URL data, not live website checks. For any future live use, consult `--help`, comply with provider terms and only enable site probing/crawling where specifically authorized. Keep private reports out of public Git.

## Security and maintenance limitations

This RC uses restrictive file creation defaults by setting process umask `077` before reporting, avoiding a symlink directly at the output directory and requesting a mode-`0700` directory. It prevents permissive *new file creation* in the tested paths, but is **not** a general security certification. The directory check is not a complete defense against parent-path/symlink races, previously existing output files with permissive permissions, unrelated tools, or modified permission masks elsewhere.

Before a public release: audit the staged ZIP file list/metadata for private research or credentials; review license and dependency requirements; decide on a unique HEXWRAITH repository; upload only approved source/release files; run a clean clone-and-test job; and publish a versioned archive in Phantom Backup HQ with its **new** verified checksum. The HQ archive created before HEXWRAITH publication does not contain this local-only RC.
