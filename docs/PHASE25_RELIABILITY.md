# 🌹 PHASE 25 // ARTWORK AND REPORT RELIABILITY

**Scope:** two narrowly targeted Python tool fixes, offline regression tests, and documentation reconciliation.

## Fixes in this pull request

| Tool | Prior behavior | Phase 25 behavior |
| --- | --- | --- |
| Rosie IP Shadow Scraper | The optional `--art` command looked for a PNG beside the script; preserved art lives in `artwork/` | Finds **the original artwork file** in the repository `artwork/` folder; no image moves, edits or duplicates |
| Rosie IP Shadow Scraper | Reports used second-resolution filenames and could overwrite a prior same-second run | Adds a microsecond timestamp and a short random UUID suffix |
| Rose Crawler | `Path.with_suffix()` could mistake a dotted username for a file extension | Builds each report path with its explicit `.json`, `.csv` or `.html` extension, keeping the username intact |
| Rose Crawler | Second-resolution filenames could collide during quick reruns | Adds a microsecond timestamp and a short random UUID suffix |

The files remain in each tool's existing output directory. The scripts' CLI flags, offline/public research behavior, normal report contents and the repository's approved art are unchanged. Report filenames now have a longer, unpredictable suffix.

## Actual tests

The new [reliability regression tests](../tests/test_phase25_source_reliability.py) check that the artwork path exists, that dotted usernames produce all three expected formats, and that repeated IP reports produce two distinct JSON files with their respective payloads. Existing Ubuntu CI also executes the 17 published first-run Bash recipes.

```bash
python3 -m unittest discover -s tests -p 'test_phase25_source_reliability.py' -v
python3 -m unittest discover -s tests -v
```

The live artwork viewer still depends on a graphical Linux desktop with `xdg-open`. Regression tests verify the original image path, not a graphical window opening.

## CI public clone comparison

The Phase 23 workflow originally required proposed Python/Go source files to match the public `main` checkout exactly. That protected earlier documentation-only changes, but would **wrongly fail legitimate fixes** in a new PR. The workflow now:

- Performs a real HTTPS clone of public `main` without credentials.
- Lists the hashes and reports tool files that differ from proposed changes.
- Tests the public clone separately with its offline Python suite and Go tests/build.
- Leaves verification of proposed changed files to the main branch/PR Python CI, which executes all published recipes and the Phase 25 regression tests.

**A changed source file is not silently treated as passing the old source-integrity check.** The new comparison displays the differences; reviewers should review the actual PR diff.

## Still not resolved

These targeted fixes do not eliminate every fixed-name report elsewhere in the collection, certify real X API/web integrations, or complete a full privacy, licensing or security audit. See the [release checklist](RELEASE_CHECKLIST.md) for remaining gates.

[← Tool Vault](TOOL_VAULT.md) · [← Homepage](../README.md)
