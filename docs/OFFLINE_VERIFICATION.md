# 💙 PHASE 21 // OFFLINE TERMINAL VERIFICATION

**Result: PASS on GitHub Actions Ubuntu runner.**

[Successful Ubuntu test run](https://github.com/Hellfire13666/glitchbyte-phantom-labs/actions/runs/39084340992) · [Python verification source](../tests/test_offline_terminal_verification.py) · [Phase 20 recipe audit](RECIPE_AUDIT.md)

## What actually ran

The existing `python-checks.yml` workflow uses a GitHub-hosted Ubuntu runner with Python 3.11 and `python -m unittest discover -s tests -v`. Phase 21 adds subprocess-based **real local execution** rather than just checking Markdown.

| Verification group | Actual operation |
| --- | --- |
| Source syntax | Parse all 16 top-level Python scripts |
| CLI sanity | Invoke `--help` on the 12 argparse-driven scripts |
| Offline local analysis | Run Log Constellation demo and Signal Garden demo; confirm JSON/HTML files |
| Public-link generation | Run Rose Crawler without `--fetch` and Username Intel `--links-only`; verify saved files |
| Safe domain report | Run Domain Phantom and Neon Rose Phantom in mode 7, which construct an RDAP research URL without querying the site |
| IP address classification | Run IP Specter and IP Shadow Scraper with `192.0.2.1 --mode 1`; verify JSON files |
| No-API imports | Run X Shadow No-API and HackGirl Intel against a fictional local CSV; verify JSON/CSV/HTML outputs where supported |
| No-API research links | Generate keyword links without fetching X/Google |
| Creative Python | Exercise Ghost In My Heart, Find Me If You Love Me, and Catch Me in the Chaos with real puzzle inputs; decode the Dark Desire letter |

All fixtures are fictional, and the subprocess tests run with isolated temporary `HOME` directories. **No real X account, production IP or third-party domain is used as a test target**. This phase makes no changes to existing research-tool source code.

## A bug the tests caught

The initial smoke-test suite failed its Catch Me in the Chaos **output assertion**, because the game embeds ANSI color sequences between *individual characters*. The displayed finale was there, but comparing its raw byte stream with the ordinary phrase `GAME COMPLETE` missed it. The test now strips ANSI escape sequences for comparison. We also corrected the same assertion issue in the **existing Phase 17 copy-and-paste build recipe**.

This was a **test and documentation bug**, not evidence that the underlying game failed. The original game source remains untouched.

## Important limits

A successful offline smoke test is a stronger statement than source inspection alone, but narrower than a complete release certification:

- **Not yet end-to-end checked:** The one-block `git clone` commands in every individual showcase have **not** all been pasted into distinct clean Ubuntu terminals.
- **Not included:** Paid X API authentication, live public-profile metadata, authorized domain/TLS/HTTP/port lookups, and external service reliability.
- **Not audited:** The tools' full security properties, privacy implications, correctness of real-world research data, or every possible input.
- **Go testing:** VOIDLANTERN retains its separate Go workflow. This Phase 21 Python workflow does not replace `go test` or `go vet`.

## How to run the verified suite yourself

From a repository checkout with Python 3.11:

```bash
python3 -m unittest discover -s tests -p 'test_offline_terminal_verification.py' -v
```

The existing CI will run the new tests automatically on subsequent pull requests after merging Phase 21.

**Release status:** Offline Python smoke tests passed. Live integration testing, whole-recipe fresh-machine verification, and security review remain future tasks.

[← Phantom Tool Vault](TOOL_VAULT.md) · [← Official homepage](../README.md)
