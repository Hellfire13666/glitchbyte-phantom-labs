<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 💗 FIND ME IF YOU LOVE ME // PHANTOM TOOL SHOWCASE

<!-- GLITCHBYTE-ART-COVER:START -->

![Find Me If You Love Me | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/24_find_me_if_you_love_me.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · Offline terminal love puzzle · Three clues · UTF-8 hexadecimal letter**

[🐍 Original Python source](../../tools/rosie_hide_seek.py) · [🕷️ Phantom Tool Vault](../TOOL_VAULT.md) · [📚 Tool Starter Guide](../TOOL_STARTER_GUIDE.md)

> Follow a signal, decode a flower, choose a word. Three clues unlock a private-feeling, but *not cryptographically private*, love letter.

## What the existing game does

`tools/rosie_hide_seek.py` presents an original three-stage terminal romance puzzle. The gates are a six-letter signal riddle, a four-character flower decoded from the genuine hex bytes `726f7365`, and a three-letter closing declaration. Each puzzle allows **up to four attempts**, with hints after the second incorrect attempt. Finishing all three decodes `SEALED_LETTER` with `binascii.unhexlify(...).decode("utf-8")`, then prints the letter.

The program uses only Python standard-library modules and never contacts the network, reads private files, or writes files. It has **no implemented command-line flags** such as `--help`, `--fast`, or `--output`. Its typewriter animations intentionally pause between letters, and it catches interrupted input.

**Hex is an encoding, not encryption.** Anybody with the source can decode the letter.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu / Linux Bash

**Install → Build → Test → Run → Find & Read Output → Troubleshoot.**

The full block below checks local prerequisites, safely obtains the repository, verifies Python syntax, plays all three gates using the **real source** in a controlled test with animation delays disabled **only inside the temporary test process**, checks the ending, and saves a unique terminal transcript. The source file is never edited. Network access is needed only if Git must clone the repo.

```bash
# PHANTOM LABS // FIND ME IF YOU LOVE ME
set -e

# 1. INSTALL: Python 3 and Git; no pip packages needed.
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git required."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/hide-seek-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/rosie_hide_seek.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Existing directory lacks the expected script. Inspect it; nothing overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
GAME="$WORKSPACE/glitchbyte-phantom-labs/tools/rosie_hide_seek.py"

# 2. BUILD: Python is interpreted, so there is no compiler step.
python3 --version

# 3. TEST + 4. RUN: controlled offline playthrough of the existing game.
mkdir -p "$WORKSPACE/transcripts"
TRANSCRIPT=$(mktemp "$WORKSPACE/transcripts/find_me_XXXXXXXX.txt")
python3 - "$GAME" "$TRANSCRIPT" <<'PY'
import builtins
import contextlib
import importlib.util
import pathlib
import sys

source = pathlib.Path(sys.argv[1])
destination = pathlib.Path(sys.argv[2])
compile(source.read_bytes(), str(source), "exec")
print("PASS: original source parses.")

spec = importlib.util.spec_from_file_location("rosie_hide_seek", source)
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)

# Disable typewriter delays only in this in-memory test session.
game.time.sleep = lambda _seconds: None
answers = iter(("signal", "rose", "you"))
original_input = builtins.input
builtins.input = lambda _prompt="": next(answers)
try:
    with destination.open("w", encoding="utf-8") as output:
        with contextlib.redirect_stdout(output):
            game.main()
finally:
    builtins.input = original_input

story = destination.read_text(encoding="utf-8")
assert story.count("[ACCESS GRANTED]") == 3, "Not all three clues were solved."
assert "[ROSIE.EXE] You found me." in story, "Expected finale was not reached."
assert "RosieGlitchbyte <3" in story, "The final decoded letter was not printed."
print("PASS: three actual puzzle gates and decoded ending.")
print("Transcript:", destination)
PY

# 5. FIND / READ: output is captured by the recipe, not the original game.
echo "Saved: $TRANSCRIPT"
sed -n '1,18p' "$TRANSCRIPT"
find "$WORKSPACE/transcripts" -maxdepth 1 -type f -name 'find_me_*.txt' -print
```

The generated `find_me_XXXXXXXX.txt` transcript is made by the recipe's Python output redirection, **not** by a built-in export command. `mktemp` chooses a distinct filename so earlier transcripts aren't overwritten. The transcript may contain ANSI color-control sequences because the original game prints them.

### 🎮 Play the full animated game yourself

Use the unmodified game in a real interactive terminal:

```bash
python3 "$HOME/PhantomLabsBuilds/hide-seek-station/glitchbyte-phantom-labs/tools/rosie_hide_seek.py"
```

Answer prompts directly. The existing game has no fast-mode flag, so this command includes its original typewriter animation. For a quick check, use the automatic smoke test above rather than adding unimplemented flags.

## 🛠️ Troubleshooting

| Symptom | Action |
| --- | --- |
| `python3` or `git` missing | Install from your Linux distribution's package manager |
| Existing repository folder but source absent | Inspect the folder and path manually; the recipe refuses to overwrite it |
| `--help` or `--fast` doesn't work | Neither flag is implemented by the existing source |
| Story feels slow | Its per-character delays are intentional; the smoke test disables delays only in memory |
| Clue rejected | Each riddle expects one exact lowercase answer, ignoring surrounding whitespace |
| Game closes before the letter | All three gates must succeed, with no more than four guesses per gate |
| No report files appear after normal play | Expected: original game doesn't write reports; use recipe transcript capture |
| Strange characters in saved transcript | The tool writes ANSI terminal color codes |
| A prior transcript is missing | Use the exact path printed after the run; the recipe uses unique filenames |

## 🧪 Verification and safety

The source, its three gates, answer matching, timing and decoded finale were inspected directly in [`rosie_hide_seek.py`](../../tools/rosie_hide_seek.py). The smoke test above **checks the real game logic when run**, but the complete Bash recipe was **not executed end to end on your Ubuntu system** during this documentation update.

This is a fictional romance game, not malware or a secure method of storing secrets. Review the repository [security policy](../../SECURITY.md) and [custom source-available license](../../LICENSE-NOTICE.md).

[← PHANTOM TOOL VAULT](../TOOL_VAULT.md) · [← Homepage](../../README.md)
