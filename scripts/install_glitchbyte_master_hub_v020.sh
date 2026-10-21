#!/usr/bin/env bash
# GlitchByte Phantom Labs Master Hub v0.2.0 | Official beginner installer
# Uses the published release ZIP, pins its expected SHA-256, never overwrites an installation.
set -euo pipefail

PRODUCT='GlitchByte Phantom Labs Master Hub v0.2.0'
ARCHIVE='glitchbyte-phantom-labs-master-hub-v0.2.0.zip'
FOLDER='glitchbyte-phantom-labs-master-hub-v0_2_0'
EXPECTED_SHA256='e5b1ef241ab8e3058fae593ecb1ea4fe26d95cdfb9eca1a0e84c656a1025fac7'
RELEASE_URL="https://github.com/Hellfire13666/glitchbyte-phantom-labs/releases/download/master-hub-v0.2.0/$ARCHIVE"
ROOT="$HOME/PhantomLabsLaunchers"
HUB="$ROOT/$FOLDER"

say() { printf '\n[GLITCHBYTE] %s\n' "$*"; }
die() { printf '\n[ERROR] %s\n' "$*" >&2; exit 1; }

[[ "$(uname -s)" == Linux ]] || die 'This installer supports desktop Linux only.'
for cmd in python3 unzip sha256sum; do
  command -v "$cmd" >/dev/null 2>&1 || die "Missing $cmd. Install it using your Linux package manager."
done

if [[ -e "$HUB" || -L "$HUB" ]]; then
  [[ -f "$HUB/START_HUB.sh" ]] || die "An existing folder is incomplete: $HUB. Please investigate it; nothing was overwritten."
  say 'Hub is already installed. Preserving all existing files.'
else
  TMP="$(mktemp -d)" || die 'Cannot create temporary folder.'
  trap 'rm -rf -- "$TMP"' EXIT
  if [[ -n "${GLITCHBYTE_HUB_SOURCE_ZIP:-}" ]]; then
    [[ -f "$GLITCHBYTE_HUB_SOURCE_ZIP" ]] || die 'Local archive does not exist.'
    cp -- "$GLITCHBYTE_HUB_SOURCE_ZIP" "$TMP/$ARCHIVE"
    say 'Using a local archive (for offline checks).'
  else
    command -v curl >/dev/null 2>&1 || die 'curl is required to download the release.'
    say "Downloading official release $ARCHIVE"
    if ! curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 --connect-timeout 20 --max-time 120 --retry 2 --retry-delay 3 "$RELEASE_URL" --output "$TMP/$ARCHIVE"; then
      die "Download unavailable. Confirm that master-hub-v0.2.0 has been published with its ZIP asset: https://github.com/Hellfire13666/glitchbyte-phantom-labs/releases"
    fi
  fi
  printf '%s  %s\n' "$EXPECTED_SHA256" "$TMP/$ARCHIVE" | sha256sum --check --status || die 'SHA-256 mismatch! Archive rejected; nothing installed.'
  say "PASS: expected SHA-256 verified ($EXPECTED_SHA256)"

  # Explicitly forbid archive paths outside the versioned hub directory and symlinks.
  python3 - "$TMP/$ARCHIVE" "$FOLDER" <<'PY'
import pathlib, stat, sys, zipfile
source, folder = sys.argv[1:]
with zipfile.ZipFile(source) as zf:
    infos = zf.infolist()
    if not infos: raise SystemExit('Archive is empty')
    for info in infos:
        p = pathlib.PurePosixPath(info.filename)
        if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] != folder:
            raise SystemExit('Unsafe archive path: ' + info.filename)
        if stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK:
            raise SystemExit('Symlink not allowed: ' + info.filename)
    bad = zf.testzip()
    if bad: raise SystemExit('Corrupt member: ' + bad)
print('[PASS] ZIP content and safe paths checked')
PY
  mkdir -p -- "$ROOT"
  [[ ! -e "$HUB" && ! -L "$HUB" ]] || die 'Target folder appeared during install; not overwriting.'
  unzip -q -- "$TMP/$ARCHIVE" -d "$ROOT"
  [[ -f "$HUB/START_HUB.sh" && -f "$HUB/assets/hub-icon.svg" ]] || die 'Hub extraction is incomplete; please inspect it.'
  say "Installed in $HUB"
fi

# Create new user-level menu shortcut, only if absent.
MENU="$HOME/.local/share/applications/glitchbyte-phantom-labs-switchboard-v2.desktop"
if [[ ! -e "$MENU" && ! -L "$MENU" ]]; then
  bash "$HUB/OPTIONAL_ADD_APP_MENU_SHORTCUT.sh"
else
  say 'App-menu launcher already exists. Preserved.'
fi

# Create a separate desktop shortcut; do not touch older pins or desktop entries.
DESKTOP_DIR=''
if command -v xdg-user-dir >/dev/null 2>&1; then DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; fi
if [[ -z "$DESKTOP_DIR" || "$DESKTOP_DIR" == "$HOME" ]]; then DESKTOP_DIR="$HOME/Desktop"; fi
DESKTOP="$DESKTOP_DIR/GlitchByte-Phantom-Labs-Switchboard-v2.desktop"
mkdir -p -- "$DESKTOP_DIR"
if [[ ! -e "$DESKTOP" && ! -L "$DESKTOP" ]]; then
  cat > "$DESKTOP" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GlitchByte Phantom Labs Switchboard v2
Comment=Rosie Phantom Master Hub and beginner tool recipes
Exec=/bin/bash "$HUB/START_HUB.sh"
Icon=$HUB/assets/hub-icon.svg
Terminal=false
Categories=Development;Utility;
EOF
  chmod 755 "$DESKTOP"
  if command -v gio >/dev/null 2>&1; then gio set "$DESKTOP" metadata::trusted true 2>/dev/null || true; fi
  say "Desktop shortcut created: $DESKTOP"
else
  say 'Desktop shortcut already exists. Preserved.'
fi

say 'DONE: Master Hub is ready. No existing tools were overwritten.'
say 'XFCE: if the icon is hidden, right-click wallpaper > Desktop Settings > Icons > File/launcher icons.'
if [[ "${GLITCHBYTE_HUB_SKIP_OPEN:-0}" == 1 ]]; then
  say 'Open skipped by request (testing mode).'
else
  if command -v xdg-open >/dev/null 2>&1; then
    say 'Opening the hub in your browser.'
    bash "$HUB/START_HUB.sh" || die "Could not open the hub. Try: bash '$HUB/START_HUB.sh'"
  else
    say "Install xdg-utils, then open: $HUB/index.html"
  fi
fi