<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹 VELVETECHO // Persona Observatory

**GLITCHBYTE PHANTOM LABS · RosieGlitchbyte / Velvet Signal Division**

One handle. Many echoes. Colorful signals. Local phone analysis.

**What it is:** A brand-new original Python 3/Linux username-profile research companion, inspired by the *category + URL + status report* workflow of cupidcr4wl, but built from scratch with a unique GlitchByte design. It is **not** a fork or a copy of the original website database or source code.

## Capabilities

- Ten built-in public profile templates for development, creative, community and creator accounts. `--list-sites` prints them.
- Up to five supplied usernames; searches are **offline link-building by default**, with no remote requests.
- Optional consent-based live checks using `--live --authorized`. Respect `robots.txt`, keep one second minimum between sites, cap downloads/timeouts, validate public HTTPS hostnames, do not follow redirects, and never bypass authentication or anti-bot restrictions.
- Four fictional username outcomes plus four synthetic phone-format samples in demo mode. Never represent them as live findings.
- A colorful status-by-status **ANSI terminal readout**, final outcome counters, and uniquely named **HTML, JSON and CSV reports**. The searchable neon/velvet dashboard includes phone signal cards, category listings and summary metrics; it has no remote CSS or JavaScript dependencies.
- Custom catalog: supply a `sites` array of `{name, category, url}` with **one** `{username}` in each public HTTPS template. Example: `catalog.example.json`. Do not point it to private services.
- Honest result labels: `CANDIDATE`, `POSSIBLE`, `NOT_FOUND`, `UNKNOWN`, `ERROR`. An accessible page or matching username never confirms that multiple accounts belong to the same person.

**Phone number modules:** `--phones` or `--phones-file` checks up to 25 inputs locally: normalization (10-digit NANP or explicit international +code), plausible structural format, limited calling-code country hints, de-duplication, masked default output and separate phone CSV. Optional `--phone-research-links --authorized` only generates clickable quoted-number Google search links for **manual** review; it never fetches them. The tool cannot determine number ownership, real line activation, carrier, account registration, or phone identity. This is a **format scanner**, not subscriber lookups.

**Intentional exclusions:** No automated adult-platform phone lookups, no registration/account enumeration by telephone, no SMS/calls, no login/cookie harvesting, no profile scraping to recover personal details, no image downloads, and no identity inference. Custom-site research must be legal, publicly accessible and consent-based. Never use this to harass, expose, or track anyone.

## 📋 COPY & PASTE BUILD RECIPE // UBUNTU/LINUX

**INSTALL → BUILD → TEST → RUN → FIND REPORTS → TROUBLESHOOT**

Requirements: Ubuntu/Linux, Git, Python 3.9+ (3.11 CI); **no pip dependencies**. Keep the existing Phantom Labs checkout intact:

```bash
mkdir -p "$HOME/PhantomLabsBuilds/velvetecho-rosie"
cd "$HOME/PhantomLabsBuilds/velvetecho-rosie"
if [ ! -d glitchbyte-phantom-labs ]; then
  git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
fi
cd glitchbyte-phantom-labs
TOOL="tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py"
python3 -m py_compile "$TOOL"
python3 -m unittest discover -s tests -p 'test_velvetecho_persona_observatory.py' -v
python3 "$TOOL" --demo --color always --out "$HOME/VelvetEchoReports" --open-browser
```

**Use your own public handle, offline:**

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --usernames "rosieglitchbyte" --out "$HOME/VelvetEchoReports" --open-browser
```

**Scan phone formats from numbers you own or are authorized to inspect (always offline):**

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --phones '+1 202 555 0117,+44 20 7946 0958' \
  --color always --out "$HOME/VelvetEchoReports" --open-browser
```

Numbers are **masked by default** in terminal, HTML, JSON and CSV. `--reveal-phone` explicitly saves full phone digits; keep these reports private. To create manual external research links, pass `--phone-research-links --authorized` with permission. Such links contain the full digits and may reveal them to your search provider when opened. No automatic phone-number network requests are sent.

**Read an authorized list without exposing it in shell history:**

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --phones-file "$HOME/my-authorized-numbers.txt" --color always --open-browser
```

Supply one telephone input per line or a comma-separated list, max 25, UTF-8, max 4 KiB. Full digits are masked by default in terminal and reports.

**Run usernames and phone formats together:**

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --usernames 'rosieglitchbyte' --phones '+1 202 555 0117' \
  --color always --open-browser
```

**Phone outcome meanings:** `FORMAT_OK` = structurally plausible only, **not** active; `INVALID` = unsupported syntax/implausible format; `UNKNOWN` = missing or unlisted country code. The country hint is intentionally small, not comprehensive national-number-plan validation.

**Opt-in live checks only on handles you control or are authorized to research:**

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --usernames "your_own_public_handle" --live --authorized \
  --max-sites 8 --timeout 5 --delay 2 --out "$HOME/VelvetEchoReports"
```

**Custom public catalog:**

```bash
python3 tools/velvetecho-persona-observatory/velvetecho_persona_observatory.py \
  --usernames "your_handle" \
  --catalog tools/velvetecho-persona-observatory/catalog.example.json --open-browser
```

**Find / open saved reports:** Every run prints `[REPORT] /full/path`. No generated reports belong in GitHub. If a graphical browser is unavailable, copy the printed `.html` path to Firefox, or run `firefox '/path/to/report.html'`. Reports include usernames and URLs and should be kept private.

## Tests and limitations

- 21 fully offline regression tests verify site validation, private-IP blocking, robots opt-out, conservative status results, escaping, unique output filenames, and no accidental live checks.
- Original project [cupidcr4wl-sexy](https://github.com/Hellfire13666/cupidcr4wl-sexy) is an inspiration for the workflow, not a runtime dependency. No adult-specific or phone databases were carried over.
- Live requests are deliberately slow and fail closed when `robots.txt` cannot be checked. Results may be incomplete because sites change layouts, rate limit, block automation, or require authentication.
- DNS validation is not an adversarial network sandbox. **Run this only on a machine/network you trust.** HTTPS proxies and DNS rebinding can change network behavior; don't use catalogs containing untrusted URLs. No live third-party platform integrations have been certified.
- A 404 is a result about a URL at one moment, not definitive proof that an account does not exist; 200 is only `POSSIBLE`.

[Tool Vault](../../docs/TOOL_VAULT.md) · [Dedicated Ubuntu showcase](../../docs/tool-showcases/VELVETECHO.md) · [Security policy](../../SECURITY.md) · [License notice](../../LICENSE-NOTICE.md)
