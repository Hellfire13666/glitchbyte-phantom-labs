<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 👻 VOIDLANTERN // THE FIRST PHANTOM TOOL SPOTLIGHT

<!-- GLITCHBYTE-ART-COVER:START -->

![VOIDLANTERN | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/08_voidlantern.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Go 1.21+ · HTTP(S) website diagnostics · local JSON output · v1.0.0**

> **One lantern. One authorized destination. Clear diagnostic signals.**

[🔗 Source code](../../tools/go/voidlantern-go/main.go) · [📖 Project README](../../tools/go/voidlantern-go/README.md) · [🧪 Offline test file](../../tools/go/voidlantern-go/main_test.go) · [⚙️ CI workflow](../../.github/workflows/voidlantern-go-checks.yml)

## 🔮 What it does

VOIDLANTERN makes **one HTTP(S) GET request** to a specified website, follows at most **five redirects**, and writes a local JSON report. It records:

| Signal | Output keys | Meaning |
| --- | --- | --- |
| Target and destination | `url`, `final_url` | Submitted URL and eventual destination |
| HTTP response | `status`, `server` | Status code and server header (if present) |
| Timing and redirects | `duration_ms`, `redirects` | Elapsed request time and observed redirects |
| TLS certificate | `tls_issuer`, `tls_expiry`, `tls_days_remaining` | Available TLS leaf certificate details |
| Security header inventory | `security_headers`, `missing_headers` | Presence/absence among six configured response headers |
| Run result | `checked_at`, `error` | UTC check timestamp, and error message where applicable |

The six inspected headers are `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, and `X-Frame-Options`.

**Missing headers are not proof of an exploitable vulnerability.** This utility is not a credential guesser, crawler, exploit, or port scanner.

## 📋 COPY & PASTE BUILD RECIPE // Linux (Bash)

**Recipe verified against VOIDLANTERN's documented Go flags and source.** It checks for Go 1.21+, runs local tests and vet, builds the executable, prompts you for **a website you own or have explicit authorization to assess**, and saves a dated JSON report. Paste the whole block into a **Bash terminal** from any directory. Network checks begin only after you enter a target.

```bash
# PHANTOM LABS // VOIDLANTERN complete build recipe
set -e
if ! command -v git >/dev/null 2>&1; then
  echo "Install Git first using your Linux package manager"
  exit 1
fi
if ! command -v go >/dev/null 2>&1; then
  echo "Install Go 1.21+ from https://go.dev/dl/ and re-open your terminal."
  exit 1
fi

# Use an existing clone, or download the repository without replacing it.
if [ ! -d glitchbyte-phantom-labs/.git ]; then
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
cd glitchbyte-phantom-labs/tools/go/voidlantern-go

echo "== Go version =="
go version
echo "== Offline tests =="
go test ./...
echo "== Static checks =="
go vet ./...
echo "== Build =="
go build -o voidlantern .

echo "Only enter a website you own or are authorized to assess."
read -r -p "Authorized http(s) URL: " TARGET_URL
if [ -z "$TARGET_URL" ]; then
  echo "No URL supplied; compiled successfully without contacting a website."
else
  mkdir -p reports
  REPORT="reports/voidlantern_$(date +%Y%m%d_%H%M%S).json"
  ./voidlantern -url "$TARGET_URL" -timeout 12 -out "$REPORT"
  echo "Report saved to: $PWD/$REPORT"
  python3 -m json.tool "$REPORT"
fi
```

**Prerequisites:** Git, Go **1.21 or newer**, and Python 3 only for pretty-printing JSON. The Go project itself has no third-party Go dependencies. On Debian-based Linux, install Git via `sudo apt install git` if missing; install a sufficiently recent Go distribution following your operating system's trusted instructions.

**Important:** This paste-from-anywhere recipe assumes you don't already have a **different directory named `glitchbyte-phantom-labs`** in the current working directory. If you do, `cd` into your actual repo and use the manual steps below instead. It runs the released `main` branch, so this Phase 3 recipe will be visible there only after this PR is merged.

### Copy & paste commands for an existing clone

From the repository root, the shorter alternative is:

```bash
cd tools/go/voidlantern-go
go test ./... && go vet ./... && go build -o voidlantern .
./voidlantern -h
```

Then enter your own approved URL into the command documented in **Run it** below.

### Troubleshoot

| Problem | What to check |
| --- | --- |
| `go: command not found` | Install Go 1.21+; verify `go version` |
| `git: command not found` | Install Git; verify `git --version` |
| `cd: ... No such file or directory` | Check where you cloned the repo and run `pwd` |
| `permission denied` | Run the freshly built `./voidlantern` from its directory; avoid `sudo` for the tool |
| `timeout` or TLS error | Confirm internet access, target authorization, TLS setup, and `-timeout` (1–60 seconds) |
| JSON report missing | Check `-out` path and permissions; the tool writes errors to stderr if unable to save |
| Output needs inspection | `python3 -m json.tool path/to/your_report.json` |

## 🛠️ Install / Build / Test

These commands are for Bash on Linux; builds also support macOS and Windows with Go installed.

From the repository root:

```bash
cd tools/go/voidlantern-go
go version
go test ./...
go vet ./...
go build -o voidlantern .
```

The module has [`go.mod`](../../tools/go/voidlantern-go/go.mod) and **no third-party Go module dependencies**. Run these commands *inside* `tools/go/voidlantern-go/`, not from the Python-oriented repository root.

## ⚡ Run it

```bash
./voidlantern -h
./voidlantern -url https://example.com -out reports/example.json
./voidlantern -url https://example.com -timeout 20 -out reports/example.json
```

The `-timeout` flag is in seconds (valid range: **1 to 60**, default **12**). `-out` defaults to `voidlantern_report.json` and creates parent directories. The program prints a terminal summary and writes JSON. For errors during an assessment, it attempts to save an error report and exits with a nonzero status.

**Use only website addresses you control or have permission to assess.** The example domain here is illustrative. Redirects can leave the original host; verify that redirected destinations are also within your authorization.

## 📁 Find and read the report

From the Go project directory:

```bash
find . -type f -name '*.json'
python3 -m json.tool reports/example.json
```

Replace `reports/example.json` with your actual saved path. This report is **JSON**, not an HTML dashboard or CSV export. It stores URLs, response headers, and details that can be sensitive: don't commit live reports.

### Illustrative JSON shape (not output from a real scan)

```json
{
  "url": "https://example.com",
  "final_url": "https://example.com",
  "status": 200,
  "duration_ms": 123,
  "security_headers": {},
  "missing_headers": ["Content-Security-Policy"],
  "checked_at": "2026-10-17T00:00:00Z"
}
```

Optional fields are omitted by Go's `omitempty` behavior and the actual report depends on the destination. The example above demonstrates the JSON **shape** only. It is not evidence that the host was checked, and does not imply this is the complete set of missing headers.

## 🧪 What has been verified

This spotlight was prepared by inspecting existing `main.go`, `main_test.go`, `go.mod`, `README.md` and the repository's Go GitHub Actions workflow.

- Existing offline tests use `httptest.NewServer` and invalid URL input.
- The existing workflow runs `go test ./...`, `go vet ./...`, and `go build -o voidlantern .` when matching Go paths change.
- These **documentation-only** changes do not themselves trigger that path-filtered Go workflow.
- No live target was scanned as part of writing this showcase.

## 🔐 Safety and licensing

The [repository's custom source-available license](../../LICENSE-NOTICE.md) governs the project. The Go project's original README contains an older "No license has been selected yet" statement; that text predates or conflicts with the repository-wide license notice. **Treat the repository-wide license notice as authoritative**, and do not assume unrestricted modification or redistribution.

Review [SECURITY.md](../../SECURITY.md) before operating network-related tools. Avoid committing private research output, secrets, cookies or session data.

[← Phantom Tool Vault](../TOOL_VAULT.md) · [← Main homepage](../../README.md)

## 💾 Easy Save: `-o name.txt` or `--o name.txt`

Install the shared [Phantom Easy Save runner](../EASY_SAVE_ALL_TOOLS.md) first. It captures **actual printed terminal output** without rewriting this legacy tool. Both `-o` and `--o` work **on the runner**, before the `--` separator:

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
# Build VOIDLANTERN using the steps earlier on this page, then from its build folder:
python3 "$SAVER" --o voidlantern_help.txt -- ./voidlantern -h
```

This safe first example saves **help text**, not real Intel; replace `--help` / `-h` after the separator with the genuine run command and documented arguments from this page to save its printed findings. Choose a fresh filename for each run; existing TXT files are not overwritten. The runner does **not** disable this tool's own report exports or save native JSON/CSV/HTML; use the native export commands listed above for those. Interactive programs or browser-only interfaces may need native export instead. New tools are expected to support `-o` and `--o` natively after tests pass.

