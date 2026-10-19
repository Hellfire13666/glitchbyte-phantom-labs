<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 💌 GHOST IN MY HEART // PHANTOM TOOL SHOWCASE

<!-- GLITCHBYTE-ART-COVER:START -->

![Ghost in My Heart | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/23_ghost_in_my_heart.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · Five-chapter offline romance riddle · Hex-decoded love letter · No external dependencies**

[🐍 Actual Python source](../../tools/rosie_ghost_heart.py) · [🕷️ Phantom Tool Vault](../TOOL_VAULT.md) · [📚 Tool Starter Guide](../TOOL_STARTER_GUIDE.md)

> A midnight terminal, five puzzles, one hidden letter. This is a **fictional interactive romance game**, not a web scanner or a cryptographic messaging application.

## What the existing script actually does

The Python source is a **single-file terminal game** with five gates. Players solve a spoken-word riddle, a four-byte hexadecimal flower clue, a keyboard riddle, a reversed word and a final word about affection. After all correct answers, the game decodes a UTF-8 love letter from hex and prints it.

- **Interactive play:** `python3 tools/rosie_ghost_heart.py` from the repository root.
- **Quick display:** `python3 tools/rosie_ghost_heart.py --fast` disables typewriter delays. The source detects the `--fast` text directly in `sys.argv`; it does **not** use `argparse`, so **`--help` is not a supported help option**.
- **No internet connection, API token, file input or third-party Python packages**.
- The letter is encoded as plain UTF-8 **hex**, which anyone can decode. It is not secret-key encryption and does not provide confidentiality.
- The original game **does not save JSON, CSV, HTML or a log file**. You can optionally capture its terminal output to a text file using Bash, without modifying the game.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu / Linux Bash

**Install → Build → Test → Run → Find/Read Output → Troubleshoot**

The complete first-run block sets up a safe local workspace, checks that the exact existing game source parses, feeds the five known correct answers automatically, checks that the story reached its finale, and saves the transcript to a **unique** text filename. It makes **no network requests beyond an initial Git clone if needed**.

```bash
# PHANTOM LABS // GHOST IN MY HEART first-run recipe
set -e

# 1. INSTALL: check Python 3 and Git. No pip packages required.
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/ghost-heart-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/rosie_ghost_heart.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Repository folder exists but expected file is missing. Inspect it; nothing overwritten."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: this is interpreted Python, so no compiler is needed.
python3 --version
GAME="$WORKSPACE/glitchbyte-phantom-labs/tools/rosie_ghost_heart.py"

# 3. TEST: parse exact source without generating files in the repository.
python3 - "$GAME" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
compile(p.read_bytes(), str(p), "exec")
print("PASS: Ghost In My Heart Python syntax parsed.")
PY

# 4. RUN: a scripted playthrough of the five puzzle gates.
# The original game does not write reports, so capture stdout here.
mkdir -p "$WORKSPACE/transcripts"
TRANSCRIPT=$(mktemp "$WORKSPACE/transcripts/ghost_heart_XXXXXXXX.txt")
printf '%s\n' echo rose keyboard heart love | python3 "$GAME" --fast > "$TRANSCRIPT"

# Check the actual game ending (works even with ANSI color sequences).
python3 - "$TRANSCRIPT" <<'PY'
import pathlib, sys
txt = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
assert "ONE HEART WAS FOUND" in txt, "The final chapter was not reached."
assert "RosieGlitchbyte <3" in txt, "The full letter was not revealed."
print("PASS: All five gates completed and the letter was revealed.")
PY

# 5. FIND / READ OUTPUT: view the exact saved transcript.
echo "Transcript saved: $TRANSCRIPT"
sed -n '1,18p' "$TRANSCRIPT"
echo "See other runs:"
find "$WORKSPACE/transcripts" -maxdepth 1 -type f -name 'ghost_heart_*.txt' -print
```

**Result:** A saved `ghost_heart_XXXXXXXX.txt` terminal transcript inside `~/PhantomLabsBuilds/ghost-heart-station/transcripts/`. The `mktemp` command chooses a unique filename and avoids overwriting your earlier captures. ANSI escape sequences from the game's neon terminal output may be visible in text editors; this is expected.

**Important distinction:** The transcript is created by the **shell redirection in this recipe**, not by any built-in file export option in the Python game.

## 🎮 Play the game yourself, interactively

After running the first-run block, launch the game in your terminal:

```bash
python3 "$HOME/PhantomLabsBuilds/ghost-heart-station/glitchbyte-phantom-labs/tools/rosie_ghost_heart.py"
```

Or skip character-by-character animation:

```bash
python3 "$HOME/PhantomLabsBuilds/ghost-heart-station/glitchbyte-phantom-labs/tools/rosie_ghost_heart.py" --fast
```

Type answers at the `[YOUR REPLY]` prompt. Incorrect guesses show hints after repeated attempts. Press Ctrl+C or send end-of-file to leave the game.

## 🛠️ Troubleshooting

| Problem | Actual fix |
| --- | --- |
| `python3` / `git` missing | Install via your distribution's package manager |
| Clone folder exists but game not found | Check the directory, `pwd` and your clone; recipe refuses to overwrite a folder |
| `--help` starts the game | Expected: this script does **not** implement an argparse help option |
| Terminal pauses between letters | Normal typewriter animation; pass `--fast` |
| Automated story ends early | Verify the exact five newline-separated answers or play interactively |
| No JSON/CSV/HTML results | Expected: this is a terminal game; capture stdout to a `.txt` transcript if desired |
| Odd escape characters in the saved text | ANSI color codes are present in the source's terminal output |
| Want to keep multiple playthroughs | Save with separate transcript filenames; the example uses `mktemp` |
| No letter displayed | Solve all five gates; the story only reveals the letter at the end |

## 🧪 Verification and responsible use

The five puzzle gates, `--fast` behavior, hex decoding, lack of export flags and absence of network activity were confirmed by inspecting [the original Python source](../../tools/rosie_ghost_heart.py). The copy-and-paste workflow was **source-reviewed**, but not executed on the user's Ubuntu machine in this documentation update. The final chapter assertions in the recipe act as a reproducible local smoke test.

The game is fictional and intended for consenting adult readers as a creative surprise, not a way to conceal private messages or collect credentials. Follow the repository's [security policy](../../SECURITY.md) and [custom source-available license](../../LICENSE-NOTICE.md).

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← GitHub homepage](../../README.md)

## 💾 Easy Save: `-o name.txt` or `--o name.txt`

First install the common [Phantom Easy Save runner](../EASY_SAVE_ALL_TOOLS.md). It saves **printed terminal output** while leaving the original interactive program and its own exports untouched. The runner understands both `-o` and `--o` before the `--` separator.

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
# From the main HQ repository checkout root:
python3 "$SAVER" --o ghost_in_my_heart_help.txt -- python3 -u tools/rosie_ghost_heart.py --help
```

This example saves **help output only**, not the game's results. To save an actual run, replace the `--help` after the separator with the documented command/arguments. **Note:** interactive prompts, games and full-screen terminal UI may not work the same through a pipe, so for these projects a native export or copy-from-terminal approach is safer. The shared wrapper never pretends to save game state or browser-only results. Existing filenames aren't overwritten; other reports produced by the legacy game may still be created. Our new-build standard calls for native `-o` / `--o` export where it makes sense.

