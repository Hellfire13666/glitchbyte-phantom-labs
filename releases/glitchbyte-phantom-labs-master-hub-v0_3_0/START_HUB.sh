#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python3 -B "$HERE/scripts/refresh_catalog.py"
xdg-open "$HERE/index.html"
