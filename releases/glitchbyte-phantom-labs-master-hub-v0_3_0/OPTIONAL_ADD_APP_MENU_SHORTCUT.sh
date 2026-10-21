#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$HOME/.local/share/applications"
FILE="$HOME/.local/share/applications/glitchbyte-phantom-labs-switchboard-v3.desktop"
if [[ -e "$FILE" ]]; then
  echo '[NOTICE] App launcher already exists. Nothing overwritten.'
  exit 1
fi
cat > "$FILE" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=GlitchByte Phantom Labs Switchboard v3
Comment=Open local tool and recipe pages
Exec=/bin/bash "$HERE/START_HUB.sh"
Icon=$HERE/assets/hub-icon.svg
Terminal=false
Categories=Development;Utility;
EOF
chmod 644 "$FILE"
echo "[PASS] Menu launcher created: $FILE"
