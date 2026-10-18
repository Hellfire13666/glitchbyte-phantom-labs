# 🌹 PHASE 22 // CLEAN UBUNTU COPY-AND-PASTE RECIPE VERIFICATION

**Result: PASS, all 17 documented first-run Bash recipes.**

[Successful Ubuntu CI execution](https://github.com/Hellfire13666/glitchbyte-phantom-labs/actions/runs/39085535226) · [Source of the verification test](../tests/test_published_copy_paste_recipes.py) · [Phase 21 offline verification](OFFLINE_VERIFICATION.md)

## What was executed

On a GitHub Actions Ubuntu runner, the Python unittest suite extracts the **first fenced Bash block** from each published showcase page and invokes that block using `bash -c` in a separate freshly created temporary `HOME`.

The execution covers **all 16 Python scripts and VOIDLANTERN Go**, in the following showcase order:

| Workstation | First-run coverage |
| --- | --- |
| Log Constellation | Offline demo, generated HTML/JSON |
| Domain Intel | Syntax/help and authorized-domain prompt; blank input intentionally skips live DNS |
| Username Intel | Fictional handle, offline public profile-link report |
| Rose Crawler | Fictional handle, offline candidate links and reports |
| Signal Garden | Offline demo note and reports |
| Domain Phantom | Offline mode 7 RDAP research-link report |
| IP Specter | Offline documentation-IP classification |
| IP Shadow Scraper | Offline documentation-IP classification |
| X Intel Phantom | Syntax/help and safe setup-only first run; no API token supplied |
| X Shadow No-API | Fictional CSV analysis |
| Ghost In My Heart | All five puzzle gates and letter display |
| Dark Desire | Hex-decoded letter saved by recipe |
| Find Me If You Love Me | Three puzzles, finale and text transcript |
| Catch Me in the Chaos | Three puzzles, finale and ANSI-safe transcript assertion |
| HackGirl Intel | Fictional CSV analysis with JSON/HTML reports |
| Neon Rose Phantom 3.0 | Offline RDAP URL generation and JSON check |
| VOIDLANTERN Go | `go test`, `go vet`, build; blank URL prompt intentionally skips contacting a website |

The first Bash blocks were **not rewritten** for the test, and the actual tool and documentation files are the published repository files.

## Exact testing boundary

To avoid needing a live remote clone 17 times and accidentally picking up an unrelated future `main` commit, the test temporarily maps:

```text
https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
```

to the **currently checked-out repository** using Git's `url.<base>.insteadOf` environment configuration. Therefore, the real `git clone` commands run and create Git checkouts, but the data comes from a local `file://` source rather than GitHub over the internet.

A fresh temporary `HOME` is created for **each recipe**, and the test deletes it afterward. Inputs are fictional or blank; no X API bearer token, login cookie, production IP or authorized remote website is needed. The repository remains unchanged.

**This proves:** All published first blocks complete successfully in the tested Ubuntu CI environment, including the local setup, actual available command-line options, offline examples and required artifact checks.

**It does not prove:** Public internet cloning under every network configuration, live-site permissions, every optional example after the first Bash block, support on every Ubuntu version, security certification, or successful X API/real-world data access.

## Run the suite yourself

From an existing checkout on Python 3.11 with Git and Go available:

```bash
python3 -m unittest discover -s tests -p 'test_published_copy_paste_recipes.py' -v
```

This particular suite is Linux/Bash-oriented and uses GNU/Linux utility behaviors. It uses no external application credentials.

The original source tools, licensing, security policies, artwork, and Go code were **not modified** in Phase 22.

[← Tool Vault](TOOL_VAULT.md) · [← GitHub homepage](../README.md)
