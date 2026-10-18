# 🌹⚡ COPY, PASTE & OPEN // PHANTOM LABS QUICK LAUNCHERS

**No ChatGPT file attachments. No Git pull. No merge or rebase. No code typed in nano. No shell exit.**

Open a terminal on Ubuntu/Linux, copy **one complete block** below, and your chosen tool generates a real local HTML gallery. Firefox opens automatically when installed on your desktop. Scripts and reports are saved only under `~/PhantomLabsLaunchers/`, so an existing `~/glitchbyte-phantom-labs` checkout is never touched.

Each block downloads just the [first-party launcher source](../scripts/phantom_quickopen.py) from the official repository, then the launcher downloads the selected, [published Python tool](../tools/) from GitHub if it is not already cached. Internet is needed to download uncached code. HEXWAKE, CIPHERBOX and GHOSTMARK processing is offline after download; ROSIE SCAN has an explicitly opted-in network mode. **Review downloaded source before execution** if you do not trust it.

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

Makes a three-stage fictional codebreaking puzzle, HTML page and separate `.answer.txt` solution. **Never share the answer file.** Cipherbox is educational encoding, not secure encryption. For custom text without putting the message in terminal history, add `--message-file "$HOME/my_message.txt"`.

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

The default uses **three temporary synthetic files** so no personal documents are read. To inspect a local folder you choose, add `--folder "$HOME/Documents"`. Reports include file paths and SHA-256 values; keep them private. GHOSTMARK never changes, deletes, or uploads originals.

[Source](../tools/ghostmark_integrity_atlas.py) · [Full integrity guide](tool-showcases/GHOSTMARK.md)

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

Every tool caches its code in `~/PhantomLabsLaunchers/code/` and stores a fresh unique HTML/JSON report under `~/PhantomLabsLaunchers/reports/<tool>/`. The underlying original tools retain their own report formats and individual [build recipes](TOOL_VAULT.md). The shared [Python Quick Open launcher](../scripts/phantom_quickopen.py) is tested in Ubuntu CI against all four real programs without network, validating the HTML/JSON outputs, folder scan, file preservation and failure paths.

**This page covers our four newer tools with verified local HTML exports.** Other original tools have their own [full individual recipes](TOOL_VAULT.md) and will receive a Quick Open command when their browser-launch path can be tested. Do not assume a CLI-only tool opens Firefox.

[← Homepage](../README.md) · [Tool Vault](TOOL_VAULT.md) · [Source-available license](../LICENSE-NOTICE.md)
