# ✦ SCREAMFRAME // PIXEL AUTOPSY STUDIO

**New, independent GlitchByte Phantom Labs offline image-investigation workstation.**

[Python 3 source](../../tools/screamframe-pixel-autopsy/screamframe_pixel_autopsy.py) · [Project README and tested Ubuntu recipe](../../tools/screamframe-pixel-autopsy/README.md) · [Offline tests](../../tools/screamframe-pixel-autopsy/tests/test_screamframe_pixel_autopsy.py) · [Synthetic sample](../../tools/screamframe-pixel-autopsy/examples/screamframe_synthetic_fixture.json)

## What it does

Collects metadata for your **own local image files** without sending their pixels anywhere: original dimensions, file type detected from image bytes, SHA-256 digests, limited EXIF timestamp, 64-bit difference hashes, and extension mismatches. Finds byte-for-byte duplicates and approximate visual echo pairs at an adjustable threshold. Exports a locally searchable HTML dashboard and machine-readable JSON. Any reported similarity is **a screening clue, not proof**.

The original dark-and-lime HTML identity uses midnight charcoal, radioactive lime, signal orange, restrained terminal typography and visual thumbnail cards. No external stylesheet, tracking pixel, remote font, or hosted javascript.

## 📋 COPY & PASTE BUILD RECIPE // UBUNTU/LINUX

This builds an independent folder, never resets or merges an existing project. `apt`, `git clone`, and `pip install` are the only setup steps requiring network access.

```bash
sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip git
STATION="$HOME/PhantomLabsBuilds/screamframe-pixel-studio"
mkdir -p "$STATION"
cd "$STATION"
if [ ! -d glitchbyte-phantom-labs ]; then git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git; fi
cd glitchbyte-phantom-labs
python3 -m venv "$STATION/.screamframe-venv"
"$STATION/.screamframe-venv/bin/python" -m pip install -r tools/screamframe-pixel-autopsy/requirements.txt
SCRIPT="$STATION/glitchbyte-phantom-labs/tools/screamframe-pixel-autopsy/screamframe_pixel_autopsy.py"
"$STATION/.screamframe-venv/bin/python" -m py_compile "$SCRIPT"
"$STATION/.screamframe-venv/bin/python" -m unittest discover -s tools/screamframe-pixel-autopsy/tests -v
"$STATION/.screamframe-venv/bin/python" "$SCRIPT" --demo --out "$STATION/screamframe-reports" --open-browser
```

The demo creates four **synthetic** images, computes real image hashes, detects duplicates/similarities/format discrepancy, and prints the local report paths. If no graphical browser is present, open the printed `[REPORT]` manually.

## Analyze screenshots from a chosen folder

```bash
PY="$HOME/PhantomLabsBuilds/screamframe-pixel-studio/.screamframe-venv/bin/python"
SCRIPT="$HOME/PhantomLabsBuilds/screamframe-pixel-studio/glitchbyte-phantom-labs/tools/screamframe-pixel-autopsy/screamframe_pixel_autopsy.py"
"$PY" "$SCRIPT" --folder "$HOME/Pictures/Screenshots" --previews --open-browser
```

That sample location must exist on your device; replace it with a folder you own. Omit `--previews` to avoid embedding private image pixels into the HTML report.

## Verify the real reports

The demo should print a fresh `screamframe_echo_*.html` and matching `.json` file. From a shell:

```bash
find "$HOME/PhantomLabsBuilds/screamframe-pixel-studio/screamframe-reports" -maxdepth 1 -type f \( -name 'screamframe_echo_*.html' -o -name 'screamframe_echo_*.json' \)
```

Tested locally with Python 3 and Pillow 12.3.0: 8 dedicated unit tests passed, compilation succeeded, and the synthetic demo produced 4 inspected images / 1 identical set / 2 visual pairs / 1 format mismatch / 0 skips. GitHub Actions / Ubuntu CI, external screenshot quality, and long-running scans have not been separately certified by those local tests.

**Boundaries:** no networking, no OCR, no file modification or deletion, no proof of forgery, limited metadata extraction. EXIF fields are untrusted. Scan avoids symlinks, limits size and pixel count, caps total files, and skips its report folder. Reports still contain filenames, hashes, timestamps and optionally thumbnails, so keep them private.

## Troubleshoot

- **Pillow missing:** Activate the project venv and install `requirements.txt`.
- **Folder not found:** Replace the screenshot path with a real folder that your user can read.
- **Firefox did not open:** Open the `[REPORT]` path shown in the terminal manually.
- **No near matches:** dHash is an approximate visual signal; increase `--distance` cautiously, knowing false positives can rise.
- **Reports contain private filenames or previews:** Keep reports local, and omit `--previews` to avoid embedding pixels.

[License notice](../../LICENSE-NOTICE.md) · [Security guide](../../SECURITY.md)