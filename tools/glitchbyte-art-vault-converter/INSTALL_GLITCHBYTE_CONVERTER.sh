#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$HERE/GLITCHBYTE-ART-VAULT-BATCH-OPTIMIZER-v1.py"
if [[ ! -f "$SOURCE" ]]; then echo '[STOP] Converter program missing.'; exit 1; fi
if ! command -v python3 >/dev/null 2>&1; then echo '[STOP] Python 3 not found.'; exit 1; fi
APP="$HOME/.local/share/glitchbyte-phantom-labs/art-vault-converter-v1"
BIN="$APP/RUN_GLITCHBYTE_CONVERTER.sh"
DESKTOP_DIR="$HOME/Desktop"
if command -v xdg-user-dir >/dev/null 2>&1; then
  CANDIDATE="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
  if [[ -n "$CANDIDATE" && "$CANDIDATE" != "$HOME" && -d "$CANDIDATE" ]]; then DESKTOP_DIR="$CANDIDATE"; fi
fi
mkdir -p "$APP" "$DESKTOP_DIR" "$HOME/.local/share/applications"
cp "$SOURCE" "$APP/converter.py"
cat > "$BIN" <<'RUNNER'
#!/usr/bin/env bash
set -u
PINK='\033[1;35m'
CYAN='\033[1;36m'
RESET='\033[0m'
SOURCE="$HOME/Desktop/GlitchByte-To-Upload"
DEST="$HOME/Desktop/GlitchByte-Upload-Ready"
if command -v xdg-user-dir >/dev/null 2>&1; then
  D="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
  if [[ -n "$D" && "$D" != "$HOME" && -d "$D" ]]; then
    SOURCE="$D/GlitchByte-To-Upload"
    DEST="$D/GlitchByte-Upload-Ready"
  fi
fi
printf "${PINK}GLITCHBYTE PHANTOM LABS // ART VAULT CONVERTER${RESET}\n"
printf "${CYAN}================================================${RESET}\n"
echo '1) Originals folder: GlitchByte-To-Upload'
printf '2) Smaller copies: GlitchByte-Upload-Ready\n\n'
mkdir -p "$SOURCE"
if ! command -v python3 >/dev/null 2>&1; then
  echo '[STOP] Python 3 is not installed.'
  code=1
else
  python3 "$HOME/.local/share/glitchbyte-phantom-labs/art-vault-converter-v1/converter.py" \
    --source "$SOURCE" --dest "$DEST"
  code=$?
fi
if [[ "$code" == 0 && -d "$DEST" ]]; then
  echo '[DONE] Open the GlitchByte-Upload-Ready folder and upload copies from there.'
  if command -v xdg-open >/dev/null 2>&1; then (xdg-open "$DEST" >/dev/null 2>&1 < /dev/null &); fi
elif [[ "$code" != 0 ]]; then
  echo '[HELP] If Pillow is missing: sudo apt install python3-pil'
fi
printf '\n[SAFE] Your original images are never modified.\n'
if [[ -t 0 ]]; then read -r -p 'Press Enter to close this window...' _ || true; fi
exit "$code"
RUNNER
chmod 755 "$BIN"
DESKTOP_FILE="$DESKTOP_DIR/GlitchByte Art Vault Converter.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GlitchByte Art Vault Converter
Comment=Create smaller copies of GlitchByte artwork for upload
Exec=/bin/bash "${BIN}"
Icon=image-x-generic
Terminal=true
Categories=Graphics;
StartupNotify=false
EOF
chmod 755 "$DESKTOP_FILE"
cp "$DESKTOP_FILE" "$HOME/.local/share/applications/glitchbyte-art-vault-converter.desktop"
mkdir -p "$DESKTOP_DIR/GlitchByte-To-Upload"
printf '\n[PASS] ONE-CLICK CONVERTER INSTALLED\n'
echo '[SHORTCUT] Desktop launcher created'
echo '[INPUT] GlitchByte-To-Upload'
echo '[OUTPUT] GlitchByte-Upload-Ready'
echo '[NEXT] Copy your pictures into input and double-click the desktop shortcut.'
