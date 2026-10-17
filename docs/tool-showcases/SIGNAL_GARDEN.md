# 🌱 ROSIE SIGNAL GARDEN // PHANTOM TOOL SPOTLIGHT

**Python 3 · Entirely offline research organizer · HTML, JSON and CSV reports · Standard library only**

[🐍 Verified source](../../tools/rosie_signal_garden.py) · [🕷️ Tool Vault](../TOOL_VAULT.md) · [📚 Starter Guide](../TOOL_STARTER_GUIDE.md)

> Plant locally stored notes, harvest links and timelines. This is a research **organizer**, not a website scraper: URLs are extracted from your files but **never fetched or verified**.

## What the existing script does

The current CLI accepts `--folder`, `--output`, `--keyword` and `--demo`. It scans the **immediate files** in one folder with extensions `.txt`, `.md`, `.csv`, `.json` and `.log`, skipping files larger than 5,000,000 bytes. It extracts HTTP(S) links and domains, date-looking strings and optional keyword matches, plus SHA-256 hashes of the original files.

Its reports are created together in the requested output directory:

| Filename | Contents |
| --- | --- |
| `signal_garden.html` | Local searchable dashboard with domain map, links, timeline, keyword hits and source fingerprints |
| `signal_garden.json` | Structured research results |
| `signal_links.csv` | Extracted link, domain and source columns |
| `signal_timeline.csv` | Extracted date, source, line and note columns |

**These four fixed filenames are replaced every time you run the tool in the same output folder.** Use a different `--output` location for separate runs. Input notes remain your files, except `--demo` writes or replaces `demo_notes.txt` inside the chosen input directory.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

**Install → Build → Test → Run → Find Results → Troubleshoot.**

This first-run recipe processes **only locally generated, harmless demo notes**, without network access beyond the initial Git clone. The demonstration uses a dedicated input and output folder under your home directory. Paste into Bash:

```bash
# PHANTOM LABS // SIGNAL GARDEN first-run recipe
set -e

# 1. INSTALL
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git is required."; exit 1; }
WORKSPACE="$HOME/PhantomLabsBuilds/signal-garden-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"
if [ ! -f glitchbyte-phantom-labs/tools/rosie_signal_garden.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Existing folder found; inspect it instead of overwriting it."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: this is a standalone Python script without extra packages.
python3 --version

# 3. TEST: validate syntax and actual supported CLI options.
python3 -m py_compile glitchbyte-phantom-labs/tools/rosie_signal_garden.py
python3 glitchbyte-phantom-labs/tools/rosie_signal_garden.py --help

# 4. RUN: create separate safe sample inputs and reports.
mkdir -p "$WORKSPACE/sample-input" "$WORKSPACE/sample-reports"
python3 glitchbyte-phantom-labs/tools/rosie_signal_garden.py \
  --demo \
  --folder "$WORKSPACE/sample-input" \
  --output "$WORKSPACE/sample-reports" \
  --keyword phantom

# 5. FIND RESULTS
echo "Your Signal Garden reports:"
find "$WORKSPACE/sample-reports" -maxdepth 1 -type f \
  \( -name '*.html' -o -name '*.json' -o -name '*.csv' \) -print
python3 -m json.tool "$WORKSPACE/sample-reports/signal_garden.json" >/dev/null
echo "JSON parsed successfully."
echo "Open HTML: $WORKSPACE/sample-reports/signal_garden.html"
echo 'On a graphical Ubuntu desktop, run: xdg-open "$HOME/PhantomLabsBuilds/signal-garden-station/sample-reports/signal_garden.html"'
```

**Why no pip or Go install?** The current source uses only Python's standard library, reads local files, and does not need a compiler or API credentials.

## Run on your own notes

The following example has *placeholder* paths. Replace them with a directory containing text notes you own or are permitted to analyze:

```bash
python3 "$HOME/PhantomLabsBuilds/signal-garden-station/glitchbyte-phantom-labs/tools/rosie_signal_garden.py" \
  --folder "$HOME/path-to-your-notes" \
  --output "$HOME/PhantomLabsBuilds/signal-garden-station/my-reports" \
  --keyword "your chosen keyword"
```

No web requests are made by the analyzer. It does **not** recursively inspect nested directories, follow extracted links, or validate that a mention of a domain indicates ownership or a relationship.

## 📊 Open and read reports

```bash
find "$HOME/PhantomLabsBuilds/signal-garden-station/sample-reports" -type f \
  \( -name '*.html' -o -name '*.json' -o -name '*.csv' \)
python3 -m json.tool "$HOME/PhantomLabsBuilds/signal-garden-station/sample-reports/signal_garden.json" | less
head -n 10 "$HOME/PhantomLabsBuilds/signal-garden-station/sample-reports/signal_links.csv"
xdg-open "$HOME/PhantomLabsBuilds/signal-garden-station/sample-reports/signal_garden.html"
```

The browser command requires a Linux graphical desktop. For headless systems, inspect JSON/CSV locally or transfer the HTML **privately** to a trusted computer.

## 🛠️ Troubleshooting

| Symptom | What to do |
| --- | --- |
| `python3` or `git` missing | Install the required package with your distribution's package manager |
| Clone folder exists but source is missing | Inspect the existing folder; the recipe refuses to overwrite it |
| `[EMPTY]` printed | Put supported file types in the chosen folder, or use `--demo` |
| Expected link missing | Only text matching HTTP(S) patterns is extracted; links aren't opened |
| Files skipped | Check file extension and size; source ignores files larger than 5 MB |
| Output disappeared after another run | Fixed report filenames were overwritten: use different `--output` folders |
| Keyword match absent | It is a case-insensitive text match, not an AI interpretation |
| HTML won't open | Use `xdg-open` on a desktop or read `signal_garden.json` locally |
| File contains secrets or identifying data | Do not share generated reports; the dashboard contains excerpts of local notes |

## 🧪 Verification and safety

The flags, file filters, four output filenames and demo behavior were checked by inspecting [the actual Python source](../../tools/rosie_signal_garden.py). **The full paste-ready recipe has not been executed end-to-end in the user's Ubuntu environment.** The demo is illustrative until you run it locally.

The generated report may reproduce local notes, dates, URLs, and file hashes. Do not publish it without review. Read the repository's [security policy](../../SECURITY.md) and [custom source-available license](../../LICENSE-NOTICE.md).

[← PHANTOM TOOL VAULT](../TOOL_VAULT.md) · [← GitHub homepage](../../README.md)
