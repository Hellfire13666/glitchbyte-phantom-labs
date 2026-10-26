# 💾 GlitchByte Phantom Labs | Easy Save for Every Tool

[👻 Headquarters](../README.md) · [🕷️ Tool Vault](TOOL_VAULT.md) · [🌈 Beginner Recipes](BEGINNER_RUNTIME_RECIPES.md) · [🌱 Cultivation Room](CULTIVATION_ROOM.md) · [🔐 Backup HQ](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases)

**Our workshop's easy-save spellings:** `-o name.txt` and `--o name.txt`.

## ✅ Verified Ubuntu live test (October 19, 2026)

The shared easy-save runner was tested by the workshop user on Ubuntu with `python3 "$SAVER" --o findomain_results.txt -- findomain -t facebook.com`. Findomain printed real public-source candidate hostnames, encountered a crt.sh connection-limit error and tried its API fallback, then finished in **21 seconds**. The wrapper reported `[SAVED] Plain-text terminal output: findomain_results.txt`. This verifies that the common runner can display this Findomain output and save a requested TXT transcript in a real terminal. It does **not** establish accuracy or current reachability for every hostname, and it does not certify interactive or browser-only tools.

## Choose the right kind of save

### A. Native result export, where implemented

Native `-o` / `--o` writes the tool's actual clean result data. SUBDOMINATRIX writes deduplicated hostnames, one per line. Run the following inside the installed Subdominatrix project directory:

```bash
SCRIPT="./subdominatrix_live_signal_2026.py"
python3 -u "$SCRIPT" example.com --terminal-only --color always --o names.txt
```

Omit the output flag in terminal-only mode and SUBDOMINATRIX does not write any report files. Neither spelling overwrites existing output. Its original Firefox/HTML export mode remains available without terminal-only.

### B. Shared save runner, usable with most *existing noninteractive* CLI tools

[`phantom_easy_save.py`](../scripts/phantom_easy_save.py) runs an executable and copies whatever it **prints to the terminal** to one new TXT without ANSI color codes. Terminal colors remain on screen. This is a **transcript**, not the tool's own structured export.

**Install locally on Debian-based Linux:**

```bash
mkdir -p ./easy-save
curl -fL --retry 1 --connect-timeout 12 --max-time 60 \
  "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/phantom_easy_save.py" \
  -o ./easy-save/phantom_easy_save.py
python3 ./easy-save/phantom_easy_save.py --help
```

**Run from the directory where you installed `easy-save`:**

```bash
SAVER="./easy-save/phantom_easy_save.py"
python3 "$SAVER" -o results.txt -- python3 -u /path/to/the_real_tool.py ACTUAL_ARGUMENTS
```

Or use the *identical* long spelling:

```bash
python3 "$SAVER" --o results2.txt -- python3 -u /path/to/the_real_tool.py ACTUAL_ARGUMENTS
```

**Do not save a wrapper transcript:**

```bash
python3 "$SAVER" -- python3 -u /path/to/the_real_tool.py ACTUAL_ARGUMENTS
```

**Replace** `/path/to/the_real_tool.py ACTUAL_ARGUMENTS` with the actual working source path and flags shown in that tool's individual guide. The separator `--` is essential: options before it are for the save runner; everything after belongs to the child tool. Use `-u` with Python to reduce output buffering.

**Real harmless test, no scanning:**

```bash
SAVER="./easy-save/phantom_easy_save.py"
python3 "$SAVER" -o hello.txt -- python3 -u -c 'print("HELLO PHANTOM LABS")'
cat hello.txt
```

Run in your intended output directory. If `hello.txt` already exists, use a different new filename.

## 🧽 If less says a saved TXT "may be a binary file"

Press **y** to view the existing file; **q** exits less. This message can mean some non-printing terminal control bytes were captured, not that every finding is unusable. The latest Easy Save runner removes standard ANSI formatting, NUL/bell/backspace/form-feed and other problematic C0/DEL control bytes from *future* TXT saves. It preserves UTF-8 emoji and normalizes terminal CR/CRLF to text line breaks.

**To safely clean an existing saved file without changing the original**:

```bash
python3 - <<'PY'
from pathlib import Path
import re
import unicodedata

source = Path.cwd() / "findomain_results.txt"
output = Path.cwd() / "findomain_results_clean.txt"

s = source.read_bytes().decode("utf-8", errors="replace")
s = re.sub(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)", "", s)
s = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", s)
s = s.replace("\r\n", "\n").replace("\r", "\n")
s = "".join(c for c in s if c in "\n\t" or unicodedata.category(c) not in ("Cc", "Cs"))

with output.open("x", encoding="utf-8") as handle:
    handle.write(s)
print("CLEAN TXT:", output)
PY
less ./findomain_results_clean.txt
```

The new filename must not already exist. **This sanitizes text; it does not remove headers and provider messages or turn a transcript into a clean hostname-only database.** To get *only hostnames*, use a tool's native export where supported.

---

## Exact behavior and limitations

| Feature | Shared runner behavior |
|---|---|
| `-o name.txt` or `--o name.txt` | Saves combined stdout/stderr to a new plain TXT transcript |
| Neither | Wrapper itself writes **no** TXT file |
| ANSI screen colors | Preserved as printed by the child |
| TXT file | Control color codes removed; readable text |
| Existing output | Refuses overwrite |
| Nonzero exit or partial run | Returns child exit code; keeps the partial saved transcript |
| Native JSON/CSV/HTML | **Not produced** by the wrapper |
| Legacy tool's own saved reports | **Still created if that tool already creates them** |
| Firefox/browser UIs | **Not** enabled, disabled, or captured by this wrapper |
| Interactive TUIs / prompts | May be affected by pipes; prefer native output for such tools |

A status line isn't proof of a real finding. A saved transcript isn't equivalent to a validated result database. The wrapper never uploads saved files to GitHub or outside services.

## Apply it across our Tool Vault

Open the [Tool Vault](TOOL_VAULT.md), choose a program and copy its **actual working launch command** from its individual setup page. Put that command after `--`. Here's a safe help-only example:

```bash
python3 "$SAVER" --o tool_help.txt -- python3 -u tools/subdominatrix.py --help
```

The above saves **help text**, not live intelligence. Replace the final `--help` with the tool's real run flags to save its terminal output. Go programs and other executables can also be used:

```bash
python3 "$SAVER" -o go_help.txt -- /path/to/your_built_go_binary --help
```

The shared runner is for printed output, not interactive browser-only workflows or a substitute for a native data export.

## Every new build: mandatory save specification

1. New terminal-first tools should implement **both native `-o name.txt` and `--o name.txt`**, with **no TXT saved by default** and live terminal feedback still enabled. Clearly label file content.
2. Saving should be explicit, use user-chosen filenames, and never overwrite existing reports without a separate user decision. Where supported, preserve separate JSON, CSV and HTML exports.
3. Include tested **Simple, Medium and Extra** how-to examples for saving/no-saving on the individual tool page, and link this guide through HQ, Tool Vault, Cultivation, Ecosystem, RosieRiot (where relevant), and Backup HQ.
4. For older tools still without native `-o`, document the shared wrapper instead of inventing native flags. Some older tools write reports automatically; the wrapper does not disable them.
5. Confirm working `--help`, correct result contents, no-save, non-overwrite, and failure behavior before declaring each native upgrade finished.

**Currently native:** SUBDOMINATRIX. **Shared wrapper:** supports most noninteractive CLI programs without modifying their executables. Existing legacy tools are not all automatically converted to native flags.

[← HQ](../README.md) · [Build Publication Standard](BUILD_PUBLICATION_STANDARD.md) · [SUBDOMINATRIX Guide](tool-showcases/SUBDOMINATRIX.md)
