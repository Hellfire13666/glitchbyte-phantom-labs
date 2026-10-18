# 🗝️ PHANTOM CIPHERBOX // OFFLINE PUZZLE STUDIO

**Standalone Python 3 · Real reversible coding puzzles · Markdown, HTML and JSON · Private answer key · Zero external services**

[Original source](../../tools/phantom_cipherbox.py) · [Offline regression tests](../../tests/test_phantom_cipherbox.py) · [Tool Vault](../TOOL_VAULT.md)

> Turn an original message into a layered codebreaking adventure. Every step is actually reversible, including Unicode text and emoji. This is creative encoding **not** cryptographic encryption, and must not be used to protect confidential data.

## Real operations and options

| Flag | Function |
| --- | --- |
| `--message 'My message'` | Encode a short message from a shell argument |
| `--message-file message.txt` | Read local UTF-8 text instead, avoiding message text in command history |
| `--seed 404` | Reproducibly select an encoding sequence (default 404) |
| `--stages 3` | Choose 2, 3 or 4 reversible transformations (default 3) |
| `--out PATH` | Export to PATH, default `~/PhantomCipherboxReports` |
| `--verify puzzle.json` | Read a puzzle and check an answer |
| `--guess 'answer'` | Explicit answer for noninteractive verification; omit to enter via a concealed prompt |
| `--help` | Print the actual argument documentation |

Encodings include **hexadecimal UTF-8**, **Base64 UTF-8**, **ROT13**, and **character reversal**. The chosen operations are embedded in the puzzle as ordered *decoding clues*, making every puzzle solvable. The HTML and Markdown puzzle files contain **no plaintext answer**. The `.answer.txt` export **does contain the entire original message** and intermediate stages, so keep it private.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

Six-stage **Install → Build → Test → Run → Find/Read Outputs → Troubleshoot**.

Paste this complete block. The initial `git clone` contacts GitHub if a checkout is missing. All Cipherbox execution after that is completely offline, with no pip requirements, accounts or API keys.

```bash
# PHANTOM CIPHERBOX // FIRST RUN
set -e

# 1. INSTALL Python 3 and Git.
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first"; exit 1; }
WORKSPACE="$HOME/PhantomLabsBuilds/cipherbox-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/phantom_cipherbox.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Unexpected existing checkout; preserving its contents."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
SCRIPT="$WORKSPACE/glitchbyte-phantom-labs/tools/phantom_cipherbox.py"

# 2. BUILD: standalone interpreted Python 3 code.
python3 --version

# 3. TEST: genuine Python syntax and supported CLI flags.
python3 - "$SCRIPT" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
compile(p.read_bytes(), str(p), "exec")
print("PASS: PHANTOM CIPHERBOX syntax")
PY
python3 "$SCRIPT" --help

# 4. RUN: fictional, harmless, local-only encoded message.
REPORT_DIR="$WORKSPACE/exports"
mkdir -p "$REPORT_DIR"
python3 "$SCRIPT" --message "The rose survived the static" \
  --seed 404 --stages 3 --out "$REPORT_DIR"

# 5. FIND / READ: four real outputs, validate decoded round trip.
find "$REPORT_DIR" -maxdepth 1 -type f \
  \( -name '*.json' -o -name '*.md' -o -name '*.html' -o -name '*.answer.txt' \) -print
python3 - "$REPORT_DIR" "$SCRIPT" <<'PY'
import importlib.util, json, pathlib, sys
folder, script = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
items = list(folder.glob("cipherbox_404_*.json"))
assert items, "Puzzle JSON not found"
puzzle = json.loads(items[-1].read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("cipherbox", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.recover(puzzle) == "The rose survived the static"
for ext in (".md", ".html", ".answer.txt"):
    assert pathlib.Path(str(items[-1])[:-5] + ext).exists(), ext
print("PASS: real puzzle round trip and all four file formats")
PY
PUZZLE=$(find "$REPORT_DIR" -maxdepth 1 -type f -name 'cipherbox_404_*.json' -print -quit)
python3 "$SCRIPT" --verify "$PUZZLE" --guess "The rose survived the static"
echo "View the real HTML/Markdown puzzle files above."
echo "KEEP the .answer.txt file private."
```

## Create your own coded transmission

For private creative messages, a local input file avoids recording the message directly in your shell command history:

```bash
nano "$HOME/my_private_message.txt"
python3 "$HOME/PhantomLabsBuilds/cipherbox-station/glitchbyte-phantom-labs/tools/phantom_cipherbox.py" \
  --message-file "$HOME/my_private_message.txt" \
  --seed 216 --stages 4 \
  --out "$HOME/PhantomLabsBuilds/cipherbox-station/private-exports"
```

Never share the `.answer.txt` file if you want someone else to solve the puzzle. Remember: the shared puzzle is **trivially reversible by design**, so do not include passwords, secrets or sensitive information even if the answer file stays private.

## 🛠️ Troubleshooting

| Issue | Fix |
| --- | --- |
| Git or Python 3 missing | Install them with Ubuntu's package manager |
| Clone failed | Check the repository URL and connectivity |
| An existing folder blocks installation | Inspect it; the recipe refuses to overwrite files |
| `--message` is empty | Supply non-whitespace text or an appropriate UTF-8 message file |
| `--stages` rejected | Use only 2, 3 or 4 |
| `--verify` says NO MATCH | Decode every clue in order; exact case, punctuation and whitespace matter |
| Report files not found | Inspect the `--out` folder and printed `[SAVED]` paths |
| Puzzle reveals the answer | The `.answer.txt` file intentionally shows the solution; do not share it |
| HTML won't open on an Ubuntu server | Open the saved HTML on a graphical desktop or inspect Markdown |

## Testing and boundaries

The [real Python tests](../../tests/test_phantom_cipherbox.py) exercise all stage lengths, Unicode and emoji, reproducibility, separate answer key output, duplicate-safe files, negative verification and invalid CLI combinations. GitHub Actions provides the final execution result. This does not scrape, research usernames, connect to a network or offer secret encryption.

[License](../../LICENSE-NOTICE.md) · [Security policy](../../SECURITY.md) · [← Tool Vault](../TOOL_VAULT.md)
