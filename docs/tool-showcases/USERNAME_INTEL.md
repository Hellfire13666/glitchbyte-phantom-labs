<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🕵️ ROSIE USERNAME INTEL // PHANTOM TOOL SPOTLIGHT

<!-- GLITCHBYTE-ART-COVER:START -->

![Rosie Username Intel | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/09_username_intel.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**Python 3 · Public username link navigator · JSON report · No third-party libraries**

[🔗 Actual source](../../tools/rosie_username_intel.py) · [🕷️ Tool Vault](../TOOL_VAULT.md) · [📚 Starter guide](../TOOL_STARTER_GUIDE.md)

> **One handle, eight destinations, no identity assumptions.** A matching username on different websites does not establish a relationship between their account owners.

## 🔎 What it really does

The source generates public profile links for **GitHub, GitLab, Codeberg, Reddit, X, Instagram, TikTok, and Twitch**.

- With `--links-only`, it generates links for all eight platforms **without contacting those websites**.
- Without `--links-only`, it makes HTTP requests only to GitHub, GitLab, Codeberg and Reddit, and generates unchecked links for the other four.
- It prints live per-platform updates (`[01/08]`, etc.) and distinguishes **POSSIBLE PROFILE**, **NOT FOUND**, **RESTRICTED / RATE LIMITED**, **NETWORK ERROR**, **UNCERTAIN**, and **LINK ONLY**.
- A successful HTTP 200 response is **not proof of an account or an identity match**.
- Each run writes `rosie_intel_<username>.json` to your current working directory, replacing the same filename on later runs.

A 0.4-second pause follows each checkable site request. Network requests use a 7-second timeout. This is **not** a verification or attribution engine, a login bypass, or a private-account lookup.

## 📋 COPY & PASTE BUILD RECIPE // Ubuntu/Linux Bash

**Install → Build → Test → Run → Find Results → Troubleshoot.**

This first-run recipe uses only `--links-only`. It **does not make any requests to social platforms**, so you can safely inspect its generated links before considering a network check. Paste the entire block into Bash:

```bash
# PHANTOM LABS // ROSIE USERNAME INTEL
set -e

# 1. INSTALL: verify prerequisites
command -v python3 >/dev/null 2>&1 || { echo "Install Python 3 first."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Install Git first."; exit 1; }

WORKSPACE="$HOME/PhantomLabsBuilds/username-intel-station"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

# Clone only if the expected source file is not already present.
if [ ! -f glitchbyte-phantom-labs/tools/rosie_username_intel.py ]; then
  if [ -e glitchbyte-phantom-labs ]; then
    echo "Existing directory found; inspect it manually rather than overwrite."
    exit 1
  fi
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi

# 2. BUILD: standalone Python script, no compilation/pip needed
python3 --version

# 3. TEST: syntax and real CLI help, no platform requests
python3 -m py_compile glitchbyte-phantom-labs/tools/rosie_username_intel.py
python3 glitchbyte-phantom-labs/tools/rosie_username_intel.py --help

# 4. RUN: ask for a public handle and generate OFFLINE links only
read -r -p "Public username (letters/numbers/_/./-; blank skips): " HANDLE
if [ -n "$HANDLE" ]; then
  mkdir -p "$WORKSPACE/reports"
  cd "$WORKSPACE/reports"
  python3 ../glitchbyte-phantom-labs/tools/rosie_username_intel.py \
    "$HANDLE" --links-only

  # 5. FIND RESULTS: report file is written in this directory
  echo "Reports saved under: $PWD"
  find . -maxdepth 1 -type f -name 'rosie_intel_*.json' -print
else
  echo "No username entered: setup and local tests completed."
fi
```

**Valid usernames:** 1–39 letters, numbers, underscores, periods or hyphens. The script removes a leading `@` automatically. The sample recipe prompts for a handle because users must choose what public name they want to investigate. It does not silently query arbitrary people.

## 🌐 Optional live public check

For accounts you own, operate, or have a legitimate reason to research, read the platform rules and use the tool **without** `--links-only`:

```bash
cd "$HOME/PhantomLabsBuilds/username-intel-station/reports"
python3 ../glitchbyte-phantom-labs/tools/rosie_username_intel.py \
  YOUR_PUBLIC_USERNAME
```

Replace `YOUR_PUBLIC_USERNAME` with an actual valid public handle. This makes up to **four HTTP requests**, not eight. The remaining platforms remain link-only; anti-bot pages and redirects can produce misleading responses.

## 📊 Report recipe

From the reports directory, locate JSON files:

```bash
find . -type f -name 'rosie_intel_*.json'
```

Read one by its actual filename:

```bash
python3 -m json.tool rosie_intel_YOUR_PUBLIC_USERNAME.json | less
```

The JSON includes `username`, `checked_at_utc`, a disclaimer, and a `results` array with `platform`, `url`, `result`, `http_status`, and `final_url`. No HTML or CSV is generated by this version.

**Run-to-run preservation:** Results for the **same** username overwrite `rosie_intel_<username>.json` in the chosen directory. Copy or move an earlier report to a new filename before repeating if you need to keep both.

## 🛠️ Troubleshooting

| Situation | What to do |
| --- | --- |
| `python3` or `git` missing | Install with your distribution's package manager |
| Invalid username message | Use 1–39 permitted characters, without spaces |
| Missing report | Run a nonblank valid username, then check `pwd` and search `rosie_intel_*.json` |
| `LINK ONLY (not checked)` | Expected for `--links-only` and for X, Instagram, TikTok, Twitch |
| `RESTRICTED / RATE LIMITED` | Do not retry aggressively or attempt to bypass access restrictions |
| `POSSIBLE PROFILE` | Treat it only as a possible match, not verified ownership |
| Need a new report from the same handle | Save your old JSON first, since reruns overwrite it |
| Terminal colors display oddly | Standard ANSI color sequences may not render in all consoles |

## 🧪 Evidence and safety

The CLI flags and platform list are verified against [the actual Python source](../../tools/rosie_username_intel.py). This documentation update **does not claim** a real platform was queried or that the full recipe was tested end to end on Ubuntu. Python syntax checking is a local validation step, not a guarantee of live results.

Follow [SECURITY.md](../../SECURITY.md), the [custom source-available license](../../LICENSE-NOTICE.md), applicable platform terms and privacy protections. **Never treat a shared handle as proof that accounts belong to the same person.**

[← PHANTOM TOOL VAULT](../TOOL_VAULT.md) · [← GitHub homepage](../../README.md)

## 💾 Easy Save: `-o name.txt` or `--o name.txt`

Install the shared [Phantom Easy Save runner](../EASY_SAVE_ALL_TOOLS.md) first. It captures **actual printed terminal output** without rewriting this legacy tool. Both `-o` and `--o` work **on the runner**, before the `--` separator:

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
# From your HQ repository checkout root:
python3 "$SAVER" --o username_intel_help.txt -- python3 -u tools/rosie_username_intel.py --help
```

This safe first example saves **help text**, not real Intel; replace `--help` / `-h` after the separator with the genuine run command and documented arguments from this page to save its printed findings. Choose a fresh filename for each run; existing TXT files are not overwritten. The runner does **not** disable this tool's own report exports or save native JSON/CSV/HTML; use the native export commands listed above for those. Interactive programs or browser-only interfaces may need native export instead. New tools are expected to support `-o` and `--o` natively after tests pass.

