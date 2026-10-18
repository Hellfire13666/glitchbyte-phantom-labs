<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# ✦ SCREAMFRAME // Pixel Autopsy Studio

**An original GlitchByte Phantom Labs tool** · Python 3.10+ · Ubuntu/Linux · offline screenshot triage.

Palette: midnight charcoal `#090C0E`, radioactive lime `#D2FF37`, signal orange `#FF713E`. The dashboard has its own original CSS aesthetic, independent from other lab tools.

SCREAMFRAME examines local PNG, JPEG, WebP, GIF, BMP and TIFF images. It compares **SHA-256** for exact duplicates, calculates **64-bit dHash** distances for *approximate visual echoes*, spots file extension/decoded-format mismatches, records image dimensions and limited EXIF capture timestamps, and saves a searchable **HTML gallery + JSON report**. Progress prints per decoded image.

**It cannot prove image manipulation, authenticity, attribution, or who made an image.** Similar or simple images can share a perceptual hash; metadata can be edited. No OCR, social-media scraping, network requests, or cloud upload. Source files stay unchanged. Optional `--previews` embeds tiny local thumbnails in HTML; treat those reports as private.

## Install → Test → Run → Read (Ubuntu Bash)

Use a **new, standalone checkout** instead of touching a pre-existing local repository:

```bash
sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip git
STATION="$HOME/PhantomLabsBuilds/screamframe-pixel-studio"
mkdir -p "$STATION"
cd "$STATION"
if [ ! -d glitchbyte-phantom-labs ]; then
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
cd glitchbyte-phantom-labs
python3 -m venv "$STATION/.screamframe-venv"
"$STATION/.screamframe-venv/bin/python" -m pip install -r tools/screamframe-pixel-autopsy/requirements.txt
SCRIPT="$STATION/glitchbyte-phantom-labs/tools/screamframe-pixel-autopsy/screamframe_pixel_autopsy.py"
"$STATION/.screamframe-venv/bin/python" -m py_compile "$SCRIPT"
"$STATION/.screamframe-venv/bin/python" -m unittest discover -s tools/screamframe-pixel-autopsy/tests -v
"$STATION/.screamframe-venv/bin/python" "$SCRIPT" --demo --out "$STATION/screamframe-reports" --open-browser
```

The final line inspects **synthetic** example screenshots, writes timestamped `.html`/`.json`, and opens the HTML in your default browser where a graphical browser is available. Check for `[REPORT]` and `[JSON]` even if the browser does not open.

### Inspect your own screenshots

```bash
SCRIPT="$HOME/PhantomLabsBuilds/screamframe-pixel-studio/glitchbyte-phantom-labs/tools/screamframe-pixel-autopsy/screamframe_pixel_autopsy.py"
PY="$HOME/PhantomLabsBuilds/screamframe-pixel-studio/.screamframe-venv/bin/python"
"$PY" "$SCRIPT" --folder "$HOME/Pictures/Screenshots" --out "$HOME/ScreamframeEchoReports" --previews --open-browser
```

Change the folder to an existing directory you own. To keep **image pixels out of report HTML**, omit `--previews`. By default, reports contain only hashes, dimensions, relative file names and limited metadata, but even those could be sensitive.

## CLI switches

| Flag | What it does |
|---|---|
| `--demo` | Generate four harmless local images for an offline example |
| `--folder PATH` | Inspect this local image folder recursively, read-only |
| `--out PATH` | Report folder, default `~/ScreamframeEchoReports` |
| `--max-images N` | Cap successfully decoded images, default `300` |
| `--max-mb N` | Skip a file larger than N MiB, default `20` |
| `--distance N` | Maximum 64-bit dHash Hamming distance, default `5`; `0` is strictest |
| `--previews` | Embed private thumbnails inside local HTML |
| `--open-browser` | Open the dashboard locally in your default browser |
| `--help` | Show real supported arguments |

## Real demo results (synthetic input)

The four generated sample images include an exact PNG copy, a near-identical edit, and a file called `pretend_jpeg.jpg` that actually contains PNG image bytes. On Pillow 12.3.0 with the default distance threshold, testing observed:

- 4 inspected files
- 1 exact duplicate group
- 2 approximate visual echo pairs (the edited file compared with both copies)
- 1 format/extension discrepancy
- 0 skipped files

A platform/Pillow update may change perceptual similarity outputs; the test suite checks this behavior. See [`examples/screamframe_synthetic_fixture.json`](examples/screamframe_synthetic_fixture.json) for sample-only summary.

## Output and safety

Reports use unique `screamframe_echo_YYYYMMDDTHHMMSSffffffZ` names so repeated runs do not overwrite results. Scan ignores symlinks and its own report folder, if nested within the scanned folder. Scans are not a forensic chain of custody. The tool limits image decoding to 55 million pixels; damaged, oversized or unreadable files appear in `skipped` with a reason. JSON omits image previews even if `--previews` is enabled.

Install Pillow only from trusted package indexes. There is no network activity inside SCREAMFRAME; `apt`, `git clone`, and `pip install` do access package/repository servers during setup.

If Firefox does not launch, open the printed `[REPORT]` path using `firefox "/full/report/path.html"`. If `python3 -m venv` fails, install `python3-venv`. If Pillow is missing, rerun the requirements installation using the project virtual environment.

Source-available under the repository's [`LICENSE-NOTICE.md`](../../LICENSE-NOTICE.md) and [`SECURITY.md`](../../SECURITY.md).