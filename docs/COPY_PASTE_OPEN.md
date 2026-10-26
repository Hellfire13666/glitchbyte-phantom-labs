<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF1493?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹⚡ COPY, PASTE & OPEN // PHANTOM LABS QUICK LAUNCHERS

**💾 Optional TXT from a terminal run:** [Easy Save for Every Tool](EASY_SAVE_ALL_TOOLS.md) supports both `-o name.txt` and `--o name.txt` using the shared transcript saver. That tool saves the terminal's printed output, not a Firefox dashboard's underlying evidence, and Quick Open's original HTML/JSON files are still created as before. Only new/upgraded tools with native flags (currently SUBDOMINATRIX) can claim to save clean result-only TXT themselves.

**No ChatGPT file attachments. No Git pull. No merge or rebase. No code typed in nano. No shell exit.**

Open a terminal on Linux, copy **one complete block** below, and your chosen tool generates a real local HTML gallery. Firefox opens automatically when installed on your desktop. Scripts and reports are saved only under `~/PhantomLabsLaunchers/`, so an existing `~/glitchbyte-phantom-labs` checkout is never touched.

Each block downloads just the [first-party launcher source](../scripts/phantom_quickopen.py) from the official repository, then the launcher downloads the selected, [published Python tool](../tools/) from GitHub if it is not already cached. Internet is needed to download uncached code. HEXWAKE, CIPHERBOX and GHOSTMARK processing is offline after download; ROSIE SCAN has an explicitly opted-in network mode. **Review downloaded source before execution** if you do not trust it.

**Future tool release standard:** [Build → Run → Publish → Vault](BUILD_PUBLICATION_STANDARD.md) and [Simple/Medium/Extra beginner recipes](BEGINNER_RUNTIME_RECIPES.md). Existing one-paste Firefox launchers here **currently create local HTML reports automatically**; new terminal-first tools should save only when requested. Each individual guide must disclose its real behavior rather than invent flags.

## 🖥️ How visitors actually trigger a tool

**GitHub shows source code and instructions; clicking a filename, image or documentation link does not execute Python on your computer.** These are **Linux terminal launchers**, not buttons that run inside GitHub or the browser. They also do not create a terminal command named `hexwake` or `cipherbox`.

1. On an Linux desktop, open **Terminal** (often **Ctrl+Alt+T**).
2. On this page, choose the tool below. **Copy the entire Bash code block** under that heading (not the raw Python source URL).
3. **Paste** it into Terminal, then press **Enter**. Wait for `[REPORT]` and, when Firefox is available, `[OPEN] Firefox launched with the new gallery.`
4. The launcher downloads the official Python files if needed, runs a sample, and creates a real local `.html` report. Firefox opens it on a graphical desktop. **This does not launch a live website or a program inside GitHub.**
5. If Firefox doesn't open, find the terminal line beginning **`[REPORT] Open this HTML file:`**. Paste that full path into Firefox's address bar, or open it with `firefox '/full/path/from/report/line.html'`.

**Check Firefox itself first** if necessary (this only opens a public test webpage):

```bash
firefox https://example.com
```

If you see `curl: (22) ... 404`, check that this launcher file exists on the repository's **main** branch: [scripts/phantom_quickopen.py](../scripts/phantom_quickopen.py). A branch-only file cannot be downloaded using a `/main/` URL until its pull request is merged. If `curl` fails, the `&&` chain stops so Python won't run. **No `exit`, `git reset`, `git merge`, or `git pull` is required.**

If Terminal says `cipherbox: command not found`, that is expected: the correct trigger is the complete **CIPHERBOX Bash code block below**, not the word `cipherbox` alone. Running Python source without the launcher also won't automatically launch Firefox unless that particular tool implements browser opening.

## ⚡ HEXWAKE // real Firefox color palettes

```bash
mkdir -p "$HOME/PhantomLabsLaunchers" && curl -fL --retry 2 "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/phantom_quickopen.py" -o "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" && python3 "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" hexwake
```

Creates six rotating Glitch HEX palettes with seed 7831 and hot pink base `#FF1493`. To change the palette, add `--seed 9999 --count 4 --base '#B6FF00'` to the end.

[Source](../tools/hexwake_palette_foundry.py) · [Complete HEXWAKE guide](tool-showcases/HEXWAKE.md)

## 🗝️ CIPHERBOX // real reversible code puzzle

```bash
mkdir -p "$HOME/PhantomLabsLaunchers" && curl -fL --retry 2 "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/phantom_quickopen.py" -o "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" && python3 "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" cipherbox
```

Makes a three-stage fictional codebreaking puzzle, HTML page and separate `.answer.txt` solution. **Never share the answer file.** Cipherbox is educational encoding, not secure encryption. For custom text without putting the message in terminal history, add `--message-file ./my_message.txt`.

[Source](../tools/phantom_cipherbox.py) · [Full puzzle guide](tool-showcases/PHANTOM_CIPHERBOX.md)

## 🌹 ROSIE PHANTOM SCAN V2 // offline preview or authorized research

```bash
mkdir -p "$HOME/PhantomLabsLaunchers" && curl -fL --retry 2 "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/phantom_quickopen.py" -o "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" && python3 "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" rosie-scan
```

Default is a **zero-network demonstration** for `example.com`, so people can preview the 11-panel Rosie dashboard immediately. It also tries to download the existing approved lab header artwork. To perform **live public-domain research on a domain you own or are authorized to inspect**, add `--domain example.com --live --passive-subdomains --findomain --whois-cli`. Findomain and the WHOIS binary are optional, and absent tools are reported without aborting the basic scan.

[Source](../tools/rosie_phantom_scan_v2.py) · [Live-mode limitations and full guide](tool-showcases/ROSIE_PHANTOM_SCAN_V2.md)

## 👻 GHOSTMARK // duplicate file fingerprints

```bash
mkdir -p "$HOME/PhantomLabsLaunchers" && curl -fL --retry 2 "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/phantom_quickopen.py" -o "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" && python3 "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" ghostmark
```

The default uses **three temporary synthetic files** so no personal documents are read. To inspect a local folder you choose, add `--folder ./example-files` (after creating that folder). Reports include file paths and SHA-256 values; keep them private. GHOSTMARK never changes, deletes, or uploads originals.

[Source](../tools/ghostmark_integrity_atlas.py) · [Full integrity guide](tool-showcases/GHOSTMARK.md)

## 🌹👻 SUBDOMINATRIX // real subdomain intelligence feedback

**Default: fully offline demo, no target lookups.** This makes a real themed HTML, JSON, CSV and TXT report, with synthetic subdomain entries that are explicitly labeled. To launch, copy the entire terminal command and press **Enter**.

```bash
mkdir -p "$HOME/PhantomLabsLaunchers" && curl -fL --retry 2 "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/phantom_quickopen.py" -o "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" && python3 "$HOME/PhantomLabsLaunchers/phantom_quickopen.py" subdominatrix
```

To collect actual public passive information for a domain you own or are permitted to assess, add `--domain example.com --live`. To also use any separately installed enumeration executables, add `--subfinder --findomain`. For bounded live validation add `--dns-check --http-check --max-verify 40`, only for authorized targets. Neither Subfinder nor Findomain is installed automatically.

**What this genuinely implements:** four public passive sources, optional local CLI integrations, opt-in public-host DNS and HTTPS HEAD checks, header-based tech hints, feedback for unavailable/rate-limited sources, and four report formats. **Not in the current program:** vulnerability testing, global geolocation, screenshots or broad crawls. Decorative numbers in the promotional artwork are not real scan results.

[Python 3 source](../tools/subdominatrix.py) · [Complete Subdominatrix guide](tool-showcases/SUBDOMINATRIX.md)

## 🛠️ Troubleshooting

- **No Python 3 or curl:** Install `python3` and `curl` before running these commands.
- **Download fails:** Check GitHub access and the error printed by `curl`. With `&&`, the launcher won't run after a download error; it never calls `exit`.
- **Firefox unavailable:** The full local HTML file path is printed. Open it manually in your browser.
- **Your local repo has diverged:** These commands never issue `git pull` and never work inside your existing repository.
- **The code seems out of date:** Add `--refresh` to the launcher command to fetch a fresh copy of the tool; the launcher script itself is downloaded anew each paste.
- **Want to test without a browser:** Append `--no-browser`. Generated HTML and JSON still save locally.
- **Scan reports partial results:** WHOIS, RDAP, public DNS and crt.sh can be incomplete. Passive subdomain listings don't prove current ownership.
- **Security and privacy:** Read downloaded source first and don't submit secrets, sensitive paths, passwords or private evidence. CIPHERBOX is intentionally reversible.

### Files and validation

Every tool caches its code in `~/PhantomLabsLaunchers/code/` and stores a fresh unique HTML/JSON report under `~/PhantomLabsLaunchers/reports/<tool>/`. The underlying original tools retain their own report formats and individual [build recipes](TOOL_VAULT.md). The shared [Python Quick Open launcher](../scripts/phantom_quickopen.py) is tested in Linux CI against all five real programs without network, validating the HTML/JSON outputs, folder scan, file preservation and failure paths.

**This page covers our five newer tools with verified local HTML exports.** Other original tools have their own [full individual recipes](TOOL_VAULT.md) and will receive a Quick Open command when their browser-launch path can be tested. Do not assume a CLI-only tool opens Firefox.

[← Homepage](../README.md) · [Tool Vault](TOOL_VAULT.md) · [Source-available license](../LICENSE-NOTICE.md)
