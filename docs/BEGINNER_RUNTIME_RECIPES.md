# 🌈 GlitchByte Phantom Labs | Beginner Runtime Recipes

**Simple · Medium · Extra** — choose how much to run, see real feedback, and understand the output.

**This is a documentation standard, not a new flag implemented by every tool.** A recipe must use the *actual command-line options* from its linked source/README. `--simple`, `--medium`, `--extra`, `--save`, and `--live` are not universal flags. Do not invent them.

**Publishing this everywhere:** Our [Build → Run → Publish → Vault standard](BUILD_PUBLICATION_STANDARD.md) explains how every new tool gets unique artwork/source, these three verified recipes, colorful live results, accurate save/Firefox notes, and links through HQ, Cultivation, Tool Vault, and verified Backup HQ.

## What each recipe must show

| Level | Who it is for | How it should behave |
|---|---|---|
| 🌱 **SIMPLE** | First-time Ubuntu user | Small, safe first run; copy/paste command; understandable output |
| ⚡ **MEDIUM** | Curious beginner | Real public-source findings or broader local analysis, visible progress and clear limits |
| 🔥 **EXTRA** | Experienced beginner | Additional *documented* modules or a longer/broader workload; explicit scope, rate limits and authorization for active checks |

For **each individual tool's** `README.md` or build recipe, include:

1. **Prerequisites and install location**, with a real download/build step or a link to one.
2. Three **copy-and-paste Ubuntu examples** using verified options, marked SIMPLE / MEDIUM / EXTRA.
3. **Expected screen feedback** (for example START, SOURCE OK, FOUND, PARTIAL, TIMEOUT, SUMMARY), clearly distinguishing illustrative examples from live findings.
4. **What the results mean**: evidence source, counts, deduplication, false positives and unknown/unavailable status. A discovered hostname does not prove that a service is online or who owns it.
5. **Output behavior**: whether this *version* saves files automatically, where they go, and how to opt in/out if supported. **Preferred for new and updated live terminal tools: display immediately; save only on request.** Never claim existing tools already implement this if they don't.
6. **Firefox behavior**, if an actual HTML interface exists. Firefox and terminal are complementary. Don't describe a cloud dashboard or an illustrated promo image as a local live UI.
7. **Slow-internet behavior**: what happens on timeouts/429s, how partial results are handled, and how to stop with Ctrl+C.
8. **Safety**: passive public-data discovery may be used for public-domain research; active network checks only on targets you own or are explicitly authorized to test. Don't upload private findings, tokens or credentials.

**Runtime is not a guaranteed number of seconds.** Providers vary, can throttle requests, and some operations finish with partial results. Describe expected relative workload rather than promise exact durations.

---

## 🌐 Verified external Findomain recipes

For **Findomain**, an already-installed third-party tool, use our [Simple / Medium / Extra copy-and-paste terminal guide](tool-showcases/FINDOMAIN_LIVE_CHECK.md). The user's `findomain -t facebook.com` public-source run completed in 23 seconds. No file export was requested. The guide also explains optional `tee` saving, the broken lower-priority `/usr/bin/findomain` text placeholder, and safe boundaries for direct network checks.

---

## ⚡ Example A: ROSIERIOT OVERDRIVE (installed Ubuntu tools)

Read the [RosieRiot tool repository](https://github.com/Hellfire13666/rosieriot-overdrive-2026) and run `--help` before using its original engine. The separate v3 passive launcher tested in the workshop may be installed locally but **is not included in the published Overdrive ZIP** at the time of writing.

**SIMPLE — one public-source Subfinder run, live lines, no report file requested**

```bash
export PATH="$HOME/go/bin:$PATH"
subfinder -d example.com -silent
```

Public-source candidates appear as they are returned. `-silent` hides banners, **not** results. Empty output may mean no records or unavailable sources.

**MEDIUM — the workshop's locally installed passive launcher (only if present)**

```bash
LAB="$HOME/PhantomLabsLaunchers/rosieriot_overdrive_2026"
test -f "$LAB/run_rosieriot_live.sh" || echo "LOCAL LIVE LAUNCHER NOT INSTALLED"
# Only run after the launcher is present:
bash "$LAB/run_rosieriot_live.sh" example.com
```

The tested local v3 wrapper displays public-source progress, candidate hostnames and a summary without requesting a report. **This wrapper is a local workshop upgrade**, not a promised executable in the public Overdrive bundle. If absent, use SIMPLE or the published source documented in the Overdrive README.

**EXTRA — opt-in scoped DNS/HTTP modules in the published Python engine**

```bash
LAB="$HOME/PhantomLabsLaunchers/rosieriot_overdrive_2026"
python3 -u "$LAB/rosieriot_overdrive.py" \
  --target YOUR-AUTHORIZED-DOMAIN.example \
  --live --authorized --color always \
  --modules subfinder,dnsx,httpx \
  --max-hosts 20 --timeout 40
```

Replace the placeholder with a domain you own or are explicitly permitted to assess. **Existing original engine behavior:** this code captures module output rather than streaming each finding, then automatically writes a report to `~/RosieRiotReports` unless `--out` is changed. It is not yet the new terminal-first/no-auto-save implementation. `naabu`, `nuclei` and `aquatone` are deliberately excluded from this introductory recipe.

**How to read the output:** A reported `FOUND` or count is a candidate, not necessarily an active website. Providers can finish partially. Check failed sources instead of treating empty results as definitive.

---

## 🌹 Example B: SUBDOMINATRIX (the published source)

Complete setup: [Subdominatrix's tested build recipe](tool-showcases/SUBDOMINATRIX.md). These commands assume that setup is done, with the published source at the path below.

```bash
SCRIPT="$HOME/PhantomLabsBuilds/subdominatrix/glitchbyte-phantom-labs/tools/subdominatrix.py"
python3 "$SCRIPT" --help
```

**SIMPLE — clearly labeled offline preview**

```bash
python3 "$SCRIPT" example.com --offline-demo --no-open
```

Displays the real program's offline demonstration; the domain findings are **synthetic**, not live intelligence.

**MEDIUM — live public passive sources**

```bash
python3 "$SCRIPT" example.com --no-open --max-results 300
```

Collects public-source records and source-by-source feedback, with no DNS or HTTPS verification flags.

**EXTRA — bounded optional checks, authorized targets only**

```bash
python3 "$SCRIPT" YOUR-AUTHORIZED-DOMAIN.example \
  --subfinder --dns-check --http-check \
  --max-verify 20 --max-results 300 --no-open
```

Requires explicit authorization to test the target domain; uses the installed Subfinder if available. The actual supported flags come from the published source.

**Saving caveat:** The current published Subdominatrix script **always generates HTML/JSON/CSV/TXT reports**. `--no-open` only prevents automatic browser launch; it does **not** disable report creation. See its build recipe for output paths and Firefox instructions. No-save-by-default is a goal for future upgrades, not a feature to assume in this version.

---

## 🖥️ A reusable three-level recipe block for future projects

Copy this *Markdown template* into each new tool's documentation and replace placeholders with the **real**, tested commands. **Do not paste the placeholders into Ubuntu.**

```text
### 🌱 SIMPLE | First successful run
Requirements: [minimum installation]
Command: [exact tested command]
Shows: [specific actual terminal feedback]
Files written: [none, or exact location]

### ⚡ MEDIUM | More real findings
Requirements: [any additional dependency]
Command: [exact tested command]
Shows: [progress, sources, findings and summary]
Limits: [timeouts, rate limiting, data coverage]
Files written: [none, or exact location]

### 🔥 EXTRA | Full documented workflow
Requirements: [authorized scope and optional modules]
Command: [exact tested command]
Shows: [additional checked result types]
Limits: [time, concurrency, authorization]
Files written: [none, or exact location; optional save command]

If something fails: [specific next check and --help]
What the results prove: [positive / unknown / unverified]
```

### Terminal-first styling standard for new builds

- Start immediately, and stream findings as they arrive; flush output or use unbuffered Python as appropriate.
- Print status updates during long waits, timeout notices, retry/cooldown feedback, source successes/failures and a final truthful summary.
- Distinguish `FOUND`, `POSSIBLE`, `UNKNOWN`, `NOT_FOUND`, `RATE-LIMITED`, `ERROR`.
- Rotate Glitch HEX palettes while remaining legible without ANSI color.
- Prefer **no report persistence unless explicitly requested** for new live terminal tools. Document exceptions for legacy programs.
- If a tool has a local HTML UI, explain exactly how it opens in Firefox and whether it saves supporting files.

[← Beginner tool starter guide](TOOL_STARTER_GUIDE.md) · [All Tool Doors](TOOL_VAULT.md) · [Quick Open + Firefox](COPY_PASTE_OPEN.md) · [Phantom Labs HQ](../README.md)
