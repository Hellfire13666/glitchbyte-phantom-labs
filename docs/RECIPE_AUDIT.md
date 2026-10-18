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
3. **IP Shadow Scraper artwork placement.** The source expects `rosie_ip_shadow_art.png` alongside its script, while repository artwork is kept in `artwork/`. The optional art viewer may not find it. Any source fix should be a separate reviewed change.
4. **Rose Crawler output filename behavior.** The source uses `Path.with_suffix()` on a username-based stem; handles with periods may result in unexpected file names. See the dedicated tool page. Fix source separately if approved.
5. **Report overwrites and privacy.** Multiple tools use fixed report filenames or second-resolution timestamps. Preserve older reports in unique directories and never commit unreviewed research output.

## Future-tool rule

Every new `tools/*.py` source must have a corresponding `docs/tool-showcases/*.md` recipe, a Tool Vault table link, actual working terminal commands, clearly stated permissions, real report paths, troubleshooting, and honest execution status. The audit tests will help catch omissions in future PRs.

[← Phantom Tool Vault](TOOL_VAULT.md) · [← Official homepage](../README.md) · [← Source-level starter guide](TOOL_STARTER_GUIDE.md)
