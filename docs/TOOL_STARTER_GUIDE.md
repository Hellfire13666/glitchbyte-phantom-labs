# 🌹 Phantom Labs: Find, Build, Run & Read Tools

GlitchByte Phantom Labs is a collection of **independent** Python and Go projects. Each creation keeps its own name, folder and reports. A remake or upgrade happens **only when explicitly requested**.

> **Build & verify before publishing.** This is the workshop's mandatory *release checklist*, not a command magically enforced on every historical script. Some Python projects are standalone scripts and need syntax checking rather than compilation.

## 1. Find a tool

Clone the repository or open its `tools/` directory on GitHub:

```bash
git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
cd glitchbyte-phantom-labs
find tools -type f \( -name '*.py' -o -name 'go.mod' -o -name 'README.md' \) | sort
```

The original Python scripts sit directly under `tools/`; standalone Go projects may live under `tools/go/<unique-project-name>/`.

Example Python tool:

```bash
python3 tools/glitchbyte_log_constellation.py --help
```

Example Go project:

```bash
cd tools/go/voidlantern-go
go test ./...
go vet ./...
go build -o voidlantern .
./voidlantern -h
./voidlantern -url https://example.com -out reports/example.json
```

### Running a Python tool

```bash
cd glitchbyte-phantom-labs
python3 --version
python3 tools/rose_crawler.py --help
```

If a tool documents dependencies, create a separate environment and install only its documented requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

**Don't assume** every script accepts the same flags. Read its help output or its project README first. `requirements.txt` is in the repository root: run the command from there or supply the full path.

## 2. Find reports and clickable links

From the directory where you ran a tool, paste this exact command into your Ubuntu/Linux terminal:

```bash
find . -type f \( -name "*.html" -o -name "*.json" -o -name "*.csv" \)
```

This **lists report paths**, not profile URLs, and may also find files that are not scan results. If it prints nothing, check whether the run completed, which working directory you used, and whether the tool wrote a report. For wider search, run from the repository root or your chosen output folder.

To open an HTML dashboard, use the actual path printed by `find`:

```bash
xdg-open ./reports/example.html
```

The path above is illustrative. To read structured JSON:

```bash
python3 -m json.tool ./reports/example.json | less
```

To inspect CSV in a terminal:

```bash
head -n 10 ./reports/example.csv
```

For live status, use unbuffered Python output when supported:

```bash
python3 -u path/to/your_tool.py --help
```

`-u` turns off Python output buffering but **does not add** live progress if the program does not implement it. New network tools should print completion counters, result states, links when appropriate, and heartbeat messages on long waits; preserve findings on interruption when practical.

## 3. Mandatory new-tool release checks

Before proposing any new tool or publishing an upgrade:

1. Choose unique **project name**, source filename, folder, executable, report directory and report filenames. Do not replace an existing tool by accident.
2. Provide `README.md` with prerequisites, exact installation steps, `--help` usage, example commands, supported sources, known limits, sample **clearly labeled** output, and report locations.
3. Include useful offline tests, validate syntax/build, and report which live checks were and were not performed.
4. Default to free/public sources when relevant, honor authorization, privacy, robots policies and service limits; never claim uncertain results are verified identities.
5. For network tools, prefer live progress as each site completes, distinct `FOUND/POSSIBLE/NOT_FOUND/UNKNOWN/ERROR` outcomes, adjustable timeout/rate/concurrency settings, and resumable reports where practical.
6. Put the change on a **new branch and pull request**. Review checks before merging into `main`.

### Required Python baseline

From the repository root:

```bash
python3 -m compileall -q tools
python3 -m unittest discover -s tests -v
```

For standalone Python tool test suites, run their project-specific instructions as well. These baseline checks do **not** guarantee successful live network requests.

### Required Go baseline

From the directory containing the chosen project's `go.mod`:

```bash
go version
go test ./...
go vet ./...
go build -o unique-executable-name .
```

Do **not** run `go build` from the repository root unless a Go module/workspace is defined there. Validate `go version` against the version required by that tool's `go.mod`.

## 4. Beginner quick reference

| Goal | Command |
| --- | --- |
| See Python tools | `find tools -name '*.py' | sort` |
| Discover Go projects | `find tools -name 'go.mod' | sort` |
| Find HTML/JSON/CSV reports | `find . -type f \\( -name "*.html" -o -name "*.json" -o -name "*.csv" \\)` |
| See a Python tool's help | `python3 path/to/tool.py --help` |
| See Go tool help | `./compiled-tool -h` |
| Test Go module | `go test ./...` |
| Check Python syntax | `python3 -m compileall -q tools` |

**Important:** The `find` report command is intended for a POSIX shell such as Bash on Ubuntu. Copy the full command from section 2; the table is for reference only.

## 5. Share carefully

The repository is visible on GitHub. Never commit credentials, cookies, private reports or personally identifying research. Check the repository's `LICENSE-NOTICE.md`, `SECURITY.md` and `docs/RELEASE_CHECKLIST.md` before distributing or publishing.

**Phantom Labs rule:** One original creation per project. Upgrades and remakes are always explicit. Every new release documents how to **find → build/test → run → read reports**.
