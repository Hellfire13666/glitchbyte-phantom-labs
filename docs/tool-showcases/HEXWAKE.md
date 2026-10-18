<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# ⚡ HEXWAKE // GLITCH HEX PALETTE FOUNDRY

**⚡ NO-DOWNLOAD-ATTACHMENT QUICK START:** [Copy one terminal command, generate HTML and open Firefox](../COPY_PASTE_OPEN.md). No Git pull, merge or rebase. The command is hosted in our GitHub lab and uses its own safe home folder.

**⚡ HOW TO TRIGGER THIS TOOL:** Clicking GitHub's source link only displays code. To **run the program and open Firefox**, [open the one-paste launcher instructions](../COPY_PASTE_OPEN.md#-how-visitors-actually-trigger-a-tool), copy the complete Bash command for this tool, paste it into an **Ubuntu/Linux Terminal**, and press **Enter**. Wait for the local `[REPORT]` HTML path. Firefox opens automatically if installed; otherwise open that saved HTML path manually. These are not one-click GitHub apps, and typing a tool name alone is not a shell command.


**Original offline Python 3 design tool · Reproducible Glitch HEX palettes · JSON, CSS and HTML**

[Actual source](../../tools/hexwake_palette_foundry.py) · [Offline tests](../../tests/test_hexwake_palette_foundry.py) · [Phantom Tool Vault](../TOOL_VAULT.md)

A separate color-design station with its own identity, not an upgrade to an existing tool. Create varied high-contrast glitch palettes for artwork and software themes, with real RGB-shift and scanline design parameters. Never contacts an external website or requires tokens.

## Real features

- `--seed 404` chooses a reproducible palette seed, default 404.
- `--count 4` creates 1–12 palettes, default 4.
- `--base '#FF1493'` replaces the first palette's color anchor.
- `--out PATH` controls output; default `~/HexwakePaletteReports`.
- Each palette has **void, primary, secondary, pulse and signal** roles and contrast-based text color suggestions, plus glitch effect parameters.
- Generated filenames use unique suffixes and preserve previous exports.

The HTML report displays a responsive gallery of swatches. The CSS exports selectors `.hexwake-1` etc. with reusable `--hx-primary`, `--hx-rgb-shift` and related variables. Contrast suggestions do not replace an accessibility review.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

**Install → Build → Test → Run → Find/Read Reports → Troubleshoot**

Paste the complete block. Only a first Git clone requires Internet; the tool's color generation is 100% offline and Python standard-library only.

```bash
# HEXWAKE // FIRST-RUN RECIPE
set -e

# 1. INSTALL: Python 3 and Git, no pip dependencies.
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git required"; exit 1; }
WORKSPACE="$HOME/PhantomLabsBuilds/hexwake-foundry"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/hexwake_palette_foundry.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Existing unexpected checkout; refusing overwrite"
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
SCRIPT="$WORKSPACE/glitchbyte-phantom-labs/tools/hexwake_palette_foundry.py"

# 2. BUILD: an interpreted Python 3 tool.
python3 --version

# 3. TEST: syntax and actual command help, without network access.
python3 - "$SCRIPT" <<'PY'
import pathlib, sys
src = pathlib.Path(sys.argv[1])
compile(src.read_bytes(), str(src), "exec")
print("PASS: source syntax")
PY
python3 "$SCRIPT" --help

# 4. RUN: reproducible offline palettes (no network requests).
REPORT_DIR="$WORKSPACE/exports"
mkdir -p "$REPORT_DIR"
python3 "$SCRIPT" --seed 404 --count 4 --base '#FF1493' --out "$REPORT_DIR"

# 5. FIND/READ: verify JSON, CSS and HTML exist.
find "$REPORT_DIR" -maxdepth 1 -type f \
  \( -name '*.json' -o -name '*.css' -o -name '*.html' \) -print
python3 - "$REPORT_DIR" <<'PY'
import json, pathlib, sys
folder = pathlib.Path(sys.argv[1])
reports = list(folder.glob("hexwake_404_*.json"))
assert reports, "No HEXWAKE JSON output"
data = json.loads(reports[-1].read_text(encoding="utf-8"))
assert data["seed"] == 404 and len(data["palettes"]) == 4
assert data["palettes"][0]["colors"][1]["hex"] == "#FF1493"
assert list(folder.glob("hexwake_404_*.css"))
assert list(folder.glob("hexwake_404_*.html"))
print("PASS: real JSON/CSS/HTML outputs with 4 palettes")
PY
echo "Open an HTML file above using xdg-open on a graphical Linux desktop."
```

## Create a completely different color direction

```bash
python3 "$HOME/PhantomLabsBuilds/hexwake-foundry/glitchbyte-phantom-labs/tools/hexwake_palette_foundry.py" \
  --seed 7831 --count 6 --base '#B6FF00' \
  --out "$HOME/PhantomLabsBuilds/hexwake-foundry/lime-exports"
```

## Reports

The actual output folder contains `hexwake_<seed>_<random>.json`, a matching `.css`, and a matching `.html`. Each JSON report records the seed, base choice and palette definitions. CSS/HTML share the same underlying swatch values. All files are local.

## 🛠️ Troubleshoot

| Issue | Check |
| --- | --- |
| Missing Git or Python | Install Python 3 and Git using your Ubuntu package manager |
| Repository directory already exists | Recipe refuses to overwrite another checkout |
| Invalid color | Supply a quoted six-digit hex, e.g. `'#FF1493'` |
| Invalid count | Choose an integer from 1 to 12 |
| Can't find output | Read printed `[SAVED]` paths and the `--out` folder |
| HTML won't open on server | Use Firefox on desktop or view the JSON/CSS |
| Need another style | Change `--seed` or `--base` |
| Actual UI contrast too low | Treat suggested text colors as design guidance, not WCAG certification |

## Safety and verification

[Tool-specific offline tests](../../tests/test_hexwake_palette_foundry.py) cover reproducibility, valid colors, unique output files, actual format generation and invalid inputs. Check GitHub CI before treating tests as executed successfully. No login, external API or web content is involved. Original workshop tools are not replaced.

[License notice](../../LICENSE-NOTICE.md) · [Security](../../SECURITY.md) · [← Tool Vault](../TOOL_VAULT.md)
