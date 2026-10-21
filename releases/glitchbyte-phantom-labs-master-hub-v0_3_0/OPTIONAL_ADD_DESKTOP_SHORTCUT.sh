#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
if ! command -v xdg-user-dir >/dev/null 2>&1; then DESK="$HOME/Desktop"; else DESK="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; fi
if [ -z "$DESK" ] || [ "$DESK" = "$HOME" ]; then DESK="$HOME/Desktop"; fi
mkdir -p "$DESK"
FILE="$DESK/GlitchByte-Phantom-Labs-Switchboard-v3.desktop"
if [ -e "$FILE" ] || [ -L "$FILE" ]; then
 echo '[NOTICE] v3 desktop shortcut exists; preserved unchanged.'; exit 0
fi
cat > "$FILE" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=GlitchByte Phantom Labs Master Hub v3
Comment=Open verified local guides and installed tool pages
Exec=/bin/bash "$HERE/START_HUB.sh"
Icon=$HERE/assets/hub-icon.svg
Terminal=false
Categories=Development;Utility;
EOF
chmod 755 "$FILE"
if command -v gio >/dev/null 2>&1; then gio set "$FILE" metadata::trusted true 2>/dev/null || true; fi
printf '[PASS] Created new v3 desktop shortcut: %s\n' "$FILE"
