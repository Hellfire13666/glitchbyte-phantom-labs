#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROGRAM="$HERE/glitchbyte_art_new_only_v2.py"
[[ -f "$PROGRAM" ]] || { echo '[STOP] Program missing from package.'; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo '[STOP] Python 3 is missing.'; exit 1; }
APP="$HOME/.local/share/glitchbyte-phantom-labs/art-vault-new-only-v2"
BIN="$APP/RUN_GLITCHBYTE_NEW_ONLY.sh"
DESKTOP="$HOME/Desktop"
if command -v xdg-user-dir >/dev/null 2>&1; then
  candidate="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
  if [[ -n "$candidate" && "$candidate" != "$HOME" && -d "$candidate" ]]; then DESKTOP="$candidate"; fi
fi
mkdir -p "$APP/backups" "$DESKTOP" "$HOME/.local/share/applications"
cp "$PROGRAM" "$APP/converter.py"
SOURCE="$DESKTOP/GlitchByte-To-Upload"
DEST="$DESKTOP/GlitchByte-Upload-Ready"
mkdir -p "$SOURCE" "$DEST"
# Remember existing input on first install so previous photos are not reconverted.
if [[ ! -f "$HOME/.local/state/glitchbyte-phantom-labs/art-vault-new-only-v2-history.json" && -z "${XDG_STATE_HOME:-}" ]]; then
  echo '[SETUP] Remembering existing pictures without re-converting them.'
  python3 "$APP/converter.py" --source "$SOURCE" --dest "$DEST" --remember-existing
elif [[ -n "${XDG_STATE_HOME:-}" && ! -f "$XDG_STATE_HOME/glitchbyte-phantom-labs/art-vault-new-only-v2-history.json" ]]; then
  python3 "$APP/converter.py" --source "$SOURCE" --dest "$DEST" --remember-existing
fi
cat > "$BIN" <<'EOF'
#!/usr/bin/env bash
set -u
source_dir="$HOME/Desktop/GlitchByte-To-Upload"
dest_dir="$HOME/Desktop/GlitchByte-Upload-Ready"
if command -v xdg-user-dir >/dev/null 2>&1; then
  candidate="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
  if [[ -n "$candidate" && "$candidate" != "$HOME" && -d "$candidate" ]]; then
    source_dir="$candidate/GlitchByte-To-Upload"
    dest_dir="$candidate/GlitchByte-Upload-Ready"
  fi
fi
python3 "$HOME/.local/share/glitchbyte-phantom-labs/art-vault-new-only-v2/converter.py" \
  --source "$source_dir" --dest "$dest_dir"
status=$?
if [[ "$status" -eq 0 && -d "$dest_dir" ]] && command -v xdg-open >/dev/null 2>&1; then
  (xdg-open "$dest_dir" >/dev/null 2>&1 < /dev/null &)
fi
printf '\n[SAFE] Originals untouched. Only newly added images become WebP files.\n'
if [[ -t 0 ]]; then read -r -p 'Press Enter to close this window...' _ || true; fi
exit "$status"
EOF
chmod 755 "$BIN"
SHORTCUT="$DESKTOP/GlitchByte Art Vault Converter.desktop"
if [[ -f "$SHORTCUT" ]]; then
  cp "$SHORTCUT" "$APP/backups/GlitchByte Art Vault Converter.previous.desktop"
fi
cat > "$SHORTCUT" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GlitchByte Art Vault Converter
Comment=Only NEW artwork to WebP; originals safe; keeps processing history
Exec=/bin/bash "${BIN}"
Icon=image-x-generic
Terminal=true
Categories=Graphics;
StartupNotify=false
EOF
chmod 755 "$SHORTCUT"
cp "$SHORTCUT" "$HOME/.local/share/applications/glitchbyte-art-vault-converter.desktop"
printf '\n[PASS] GLITCHBYTE NEW-ONLY CONVERTER v2 INSTALLED\n'
printf '[DESKTOP] %s\n' "$SHORTCUT"
printf '[READY]   %s\n' "$DEST"
printf '[HISTORY] %s\n' "$HOME/.local/state/glitchbyte-phantom-labs/art-vault-new-only-v2-history.json"
echo '[RULE] Existing pictures were remembered on first install. Only NEW pictures added afterward convert.'
echo '[NEXT] Copy NEW pictures into GlitchByte-To-Upload and double-click the familiar converter icon.'
echo '[TIP] On MX Linux XFCE, right-click desktop icon and choose Execute or Allow Launching if asked.'
