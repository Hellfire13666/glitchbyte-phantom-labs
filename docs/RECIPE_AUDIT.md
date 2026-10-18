<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF1493?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🕷️ PHANTOM LABS // TOOL RECIPE AUDIT

**Scope:** repository `main` reviewed on 17 October 2026, with automated regression checks proposed in Phase 20.

## Inventory and coverage

| Item | Observed count | Coverage |
| --- | ---: | --- |
| Python scripts directly under `tools/` | 16 | Each has an individual source-linked showcase |
| Go modules under `tools/go/` | 1 | VOIDLANTERN has a dedicated showcase and Go tests |
| Individual tool showcases | 17 | Each contains a `COPY & PASTE BUILD RECIPE` section |
| Reusable template | 1 | Template only, not miscounted as a published tool |
| Official source repository | 1 | Original tools and custom license stay in place |

The auditor checks every Python script maps to **exactly one** recipe in the Tool Vault's tool tables, checks the Go spotlight, checks all 17 showcased recipe pages for essential documentation, and checks that Markdown links in the homepage and `docs/` resolve to real in-repository files/directories.

## Run the documentation checks

The new tests are part of the repository's existing Python `unittest` workflow:

```bash
git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
cd glitchbyte-phantom-labs
python3 -m unittest discover -s tests -v
```

On the Phase 20 branch (until merged), you can run just the audit:

```bash
python3 -m unittest discover -s tests -p 'test_tool_recipe_audit.py' -v
```

After merge, standard `python-checks.yml` runs these tests on pushes and pull requests. **The GitHub Actions result must be checked before claiming this new test suite passed.** The checks do not contact user-supplied research targets.

## What the audit tests prove, and what they don't

The checks can catch missing recipe pages, unlinked/mislinked tools, missing local Markdown links, and missing named recipe sections. They **cannot** prove that every Bash snippet has been executed successfully on Ubuntu, that a remote API supports a plan or endpoint, or that an external website is safe or accessible. Individual tool showcases identify any unperformed end-to-end tests.

No source changes to the Python tools or Go module are included in this audit phase. Existing Python syntax tests and Go tests remain in their original workflows.

## Findings to track separately

1. **Manual terminal verification still needed.** Run each full one-block recipe on a clean Ubuntu environment, verify the actual output, and record results before labeling all projects release-tested.
2. **IP Shadow Scraper TLS security-policy discrepancy resolved in Phase 24.** The preserved source uses a verifying context and checks the target IP hostname; the stale warning was corrected and mocked regression tests were added. Live certificate integration remains open.
3. **IP Shadow Scraper artwork placement (Phase 25 fixed).** The optional art viewer now locates the original file in the repository's `artwork/` folder without modifying the image.
4. **Rose Crawler dotted-handle filename behavior (Phase 25 fixed).** The reporter now preserves the username in all three output extensions; dedicated offline regression tests cover this.
5. **Report overwrites and privacy.** Phase 25 adds unique filenames to Rose Crawler and IP Shadow Scraper. Other tools may still use fixed names or second-resolution timestamps; preserve important reports and never commit unreviewed research output.

## Future-tool rule

Every new `tools/*.py` source or standalone `tools/<project>/*.py` entry point must have a corresponding `docs/tool-showcases/*.md` guide, a Tool Vault table link, actual working terminal commands, clearly stated permissions, real report paths, troubleshooting, and honest execution status. Go projects under `tools/go/<project>/go.mod` need the same Vault door and dedicated setup guide.

**Easy-find door guard:** The prominent **All Tool Doors** index near the top of `TOOL_VAULT.md` includes each tool's source/project link and setup guide. Run `python3 -m unittest discover -s tests -p 'test_tool_vault_doors.py' -v` before proposing a new tool. GitHub Actions also runs this check as part of `unittest discover -s tests`, failing when a new standalone tool is absent, a door is duplicated, or its source/guide link is broken. Tests check documentation completeness, not live external-network behavior.

[← Phantom Tool Vault](TOOL_VAULT.md) · [← Official homepage](../README.md) · [← Source-level starter guide](TOOL_STARTER_GUIDE.md)
