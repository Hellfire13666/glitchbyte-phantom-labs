<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹 VELVETECHO // PERSONA OBSERVATORY

<!-- GLITCHBYTE-ART-COVER:START -->

![VELVETECHO | GlitchByte Phantom Labs official artwork](../../artwork/tool-covers/10_velvetecho.png)

<!-- GLITCHBYTE-ART-COVER:END -->

**GlitchByte Phantom Labs, Velvet Signal Division.** New original Python 3 offline-first public username and phone-format observatory. Distinct from cupidcr4wl and the existing Rosie Username Intel link generator: VELVETECHO adds user-defined public site catalogs, conservative opt-in username HTTP observation with robots policy, 5-handle batching, bounded pacing, optional phone-format checks, color-coded terminal outcomes, and a searchable noir-rose dashboard.

[Actual Python source](../../tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py) · [Full README](../../tools/velvetecho-persona-observatory/README.md) · [Custom catalog example](../../tools/velvetecho-persona-observatory/catalog.example.json) · [Offline tests](../../tests/test_velvetecho_persona_observatory.py) · [Tool Vault](../TOOL_VAULT.md)

## 📋 COPY & PASTE BUILD RECIPE // LINUX

**Install → Build → Test → Run → Read reports → Troubleshoot.** Zero pip dependencies; requires Git and Python 3.9+. Independent install station so you do not merge or reset your existing project:

```bash
mkdir -p "$HOME/PhantomLabsBuilds/velvetecho-station"
cd "$HOME/PhantomLabsBuilds/velvetecho-station"
if [ ! -d glitchbyte-phantom-labs ]; then
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
cd glitchbyte-phantom-labs
SCRIPT="tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py"
python3 -m py_compile "$SCRIPT"
python3 -m unittest discover -s tests -p 'test_velvetecho_persona_observatory.py' -v
python3 "$SCRIPT" --demo --color always --out "$HOME/VelvetEchoReports" --open-browser
```

The **synthetic demo** performs zero network requests, creates four fictional username result rows and four synthetic phone-format checks, and saves uniquely named `velvetecho_signals_*.html`, `.json`, and `.csv` inside `~/VelvetEchoReports`. Open the HTML path printed as `[REPORT]` with Firefox. Any displayed statuses in the demo are invented examples, not live site findings.

## Use real public username links (no network)

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --usernames 'rosieglitchbyte' --out "$HOME/VelvetEchoReports" --open-browser
```

## Local phone number scanner and colorful outcome display

No network calls are made for phone numbers. The phone module scans syntax, standardizes 10-digit North American numbers, recognizes selected international calling codes, flags invalid/unknown formats, de-duplicates numbers and masks digits by default. Its `FORMAT_OK` label is **not verification of an active number, carrier, owner, or website account**. A separate `_phones.csv` is saved when phones are supplied.

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --phones '+1 202 555 0117,+44 20 7946 0958,123' \
  --color always --out "$HOME/VelvetEchoReports" --open-browser
```

For mixed input, include `--usernames 'your_handle'`. You can also provide a private list through `--phones-file '$HOME/my-authorized-numbers.txt'` (one number per line; max 25) rather than placing numbers in shell history. To **explicitly include full phone digits in output**, add `--reveal-phone`; default reports mask them. The optional `--phone-research-links --authorized` switch only creates quoted-number search engine hyperlinks for manual opening. Opening these links discloses the number to the search provider. Do not use it for profiling or harassment.

Color readout: `--color auto` for terminal detection, `--color always` to force ANSI pink/cyan/green/red/yellow, `--color never` for plain logs. Terminal prints progress, each result category and final outcome counts.

## Optional verified permission-based live run

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --usernames 'your_own_public_handle' --live --authorized --max-sites 5 --delay 2
```

`--authorized` is an explicit user confirmation, not actual authorization verification. Live checks use public HTTPS URLs only, conservative `robots.txt`, one second minimum pacing, 2–15 second timeouts, at most 20 sites/handle, no redirects and bounded response bodies. If access is blocked, reports say `UNKNOWN`, not absent. Any `POSSIBLE` is **not** proof that an account exists or belongs to any specific person. Phone-format analysis is always local and does not query accounts; no adult content site bulk search is included; for specialized publicly accessible sites you administer, you may create a custom JSON catalog with explicit `--catalog`.

## Status meanings and saved feedback

Phone format statuses are `FORMAT_OK`, `INVALID`, and `UNKNOWN`. These make no claims about identity or account presence.

- `CANDIDATE`: offline URL suggestion, unverified
- `POSSIBLE`: HTTP 200 HTML page, manually inspect
- `NOT_FOUND`: HTTP 404/410 from a checked profile URL
- `UNKNOWN`: robots blocked, rate-limited, redirected, or inconclusive
- `ERROR`: DNS/network validation or connection failure

## Troubleshoot

- **No Python 3 / Git:** Install packages from your Linux distribution; no extra pip packages.
- **Live run rejected:** Supply `--authorized` and ensure the usernames are your own or you have permission.
- **Empty/blocked results:** Robots policies, bot blocking, login gates, and site changes can prevent conclusive outcomes; never assume absence.
- **Firefox missing:** Use the printed HTML `[REPORT]` path with `xdg-open` or another desktop browser.
- **Invalid custom site:** Each entry needs a public HTTPS URL template with one `{username}` placeholder, without URL credentials or custom ports.
- **Privacy:** Reports contain submitted handles, timestamps and links. Do not post private output in public issues.

**Verification:** Synthetic demo and 21 local offline unit tests exercise core functionality. Public network service responses and production authorization have **not** been tested or certified. No older GlitchByte tool is overwritten.

[Tool Vault](../TOOL_VAULT.md) · [Release policy](../../SECURITY.md) · [License](../../LICENSE-NOTICE.md)

## 💾 Easy Save: `-o name.txt` or `--o name.txt`

Install the shared [Phantom Easy Save runner](../EASY_SAVE_ALL_TOOLS.md) first. It captures **actual printed terminal output** without rewriting this legacy tool. Both `-o` and `--o` work **on the runner**, before the `--` separator:

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
# From your HQ repository checkout root:
python3 "$SAVER" --o velvetecho_help.txt -- python3 -u tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py --help
```

This safe first example saves **help text**, not real Intel; replace `--help` / `-h` after the separator with the genuine run command and documented arguments from this page to save its printed findings. Choose a fresh filename for each run; existing TXT files are not overwritten. The runner does **not** disable this tool's own report exports or save native JSON/CSV/HTML; use the native export commands listed above for those. Interactive programs or browser-only interfaces may need native export instead. New tools are expected to support `-o` and `--o` natively after tests pass.

