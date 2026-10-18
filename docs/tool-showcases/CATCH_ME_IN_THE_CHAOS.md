# ⚡ CATCH ME IN THE CHAOS // PHANTOM TOOL SHOWCASE

**Python 3 · Offline terminal love puzzle · Three locks · Real UTF-8 hex letter · No dependencies**

[🐍 Original Python source](../../tools/rosie_catch_me_chaos.py) · [🕷️ Phantom Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> Neon static, three locks, and a love letter waiting at the other end. This is a fictional romance game, not an account cracker or network tool.

## What the original game actually does

`tools/rosie_catch_me_chaos.py` runs a colorful terminal adventure. Solve a flower riddle, decode an ASCII hex word (`737461746963`), and answer a keyboard riddle to unlock a genuine UTF-8 hex-encoded letter. Animated rainbow glitch lines, a heartbeat effect and a romantic finale are built into the original game.

**Source-grounded details:**
- The three locks accept exact answers after `strip().lower()`, with hints after two wrong guesses. There is **no fixed attempt limit**.
- The game uses Python's standard library only, with **no network requests**.
- The existing `ANIMATE = True` variable controls pauses. There is **no implemented `--fast`, `--help`, `--output` or `--mode` CLI flag**.
- `reveal()` decodes hexadecimal into a letter. Hex is reversible encoding, **not encryption**.
- It does **not write its own report files**. The recipe below saves a transcript without changing the game.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu / Linux Bash

**Install → Build → Test → Run → Find / Read Output → Troubleshoot.**

This first run checks the exact original Python source, performs all three genuine locks in a controlled **in-memory fast test**, verifies the actual finale, and saves a unique text transcript. It **does not modify the source or query websites**; an initial `git clone` contacts GitHub only if necessary.

```bash
# PHANTOM LABS // CATCH ME IN THE CHAOS first-run recipe
set -e

# 1. INSTALL: Python 3 + Git; no pip dependencies.
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git is required."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/catch-me-chaos-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

if [ ! -f glitchbyte-phantom-labs/tools/rosie_catch_me_chaos.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Existing checkout folder has no expected source file; inspect it. Nothing overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
GAME="$WORKSPACE/glitchbyte-phantom-labs/tools/rosie_catch_me_chaos.py"

# 2. BUILD: standalone Python. No compilation or third-party packages.
python3 --version

# 3. TEST + 4. RUN: play through real game logic in memory.
mkdir -p "$WORKSPACE/transcripts"
TRANSCRIPT=$(mktemp "$WORKSPACE/transcripts/catch_me_XXXXXXXX.txt")
python3 - "$GAME" "$TRANSCRIPT" <<'PY'
import builtins
import contextlib
import importlib.util
import pathlib
import re
import sys

source = pathlib.Path(sys.argv[1])
destination = pathlib.Path(sys.argv[2])
compile(source.read_bytes(), str(source), "exec")
print("PASS: original Python syntax")

spec = importlib.util.spec_from_file_location("rosie_catch_me_chaos", source)
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)

# Turn off pauses in this test process, not in the repository's source.
game.ANIMATE = False
answers = iter(("rose", "static", "keyboard"))
original_input = builtins.input
builtins.input = lambda _prompt="": next(answers)
try:
    with destination.open("w", encoding="utf-8") as out:
        with contextlib.redirect_stdout(out):
            game.main()
finally:
    builtins.input = original_input

result = destination.read_text(encoding="utf-8")
plain = re.sub(r"\\x1b\\[[0-9;]*m", "", result)
assert plain.count("[ACCESS GRANTED]") == 3, "A lock was not completed."
assert "GAME COMPLETE" in plain, "Final chapter not reached."
assert "RosieGlitchbyte <3" in plain, "Hex-decoded letter missing."
print("PASS: three locks, full ending and decoded letter")
print("Transcript:", destination)
PY

# 5. FIND AND READ: this recipe created a uniquely named text file.
echo "Saved transcript: $TRANSCRIPT"
sed -n '1,16p' "$TRANSCRIPT"
find "$WORKSPACE/transcripts" -maxdepth 1 -type f -name 'catch_me_*.txt' -print
```

The transcript is saved by the **recipe's output capture**, not by a built-in export feature. The filename is chosen using `mktemp` to avoid overwriting a prior transcript. Since the original game emits ANSI terminal colors, some editors display escape codes in the saved text.

## 🎮 Run the original animated game yourself

```bash
python3 "$HOME/PhantomLabsBuilds/catch-me-chaos-station/glitchbyte-phantom-labs/tools/rosie_catch_me_chaos.py"
```

Answer each riddle at `YOUR ANSWER >`. The game accepts retries and shows hints after two wrong answers. To skip animation for an automated test, use the separate recipe above. **Do not try `--fast`**; that flag doesn't exist in this script.

## 🛠️ Troubleshooting

| Issue | Fix |
| --- | --- |
| Python 3 or Git not found | Install through your Linux distribution's package manager |
| Existing repository folder missing tool | Inspect the checkout path rather than overwrite existing files |
| Full game types very slowly | That's intentional animation; the smoke test sets `ANIMATE=False` only in memory |
| A lock doesn't open | Input is case-insensitive but expects the exact puzzle answer; hints follow two mistakes |
| `--help` or `--fast` doesn't show expected behavior | Neither flag is implemented |
| No JSON/HTML/CSV report | The original is an interactive game; the recipe separately captures a `.txt` transcript |
| Weird control characters in text report | Normal ANSI colors from terminal output |
| Transcript was saved but can't be found | Use the exact path printed by the recipe and the `find` command |
| Need to preserve many playthroughs | Recipe uses unique filenames; keep the outputs in your private workspace |

## 🧪 Verification, safety and license

The tool's three answers, retry behavior, animations, hidden letter and absence of CLI flags were confirmed by inspecting [its actual Python source](../../tools/rosie_catch_me_chaos.py). The recipe contains a reproducible offline smoke test, but it **has not been executed end-to-end in your Ubuntu environment** during this documentation update.

No credentials, login sessions or external accounts are involved. The hex letter is not cryptographically secure. Follow the repository's [security guidance](../../SECURITY.md) and [custom source-available license](../../LICENSE-NOTICE.md).

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Official homepage](../../README.md)
