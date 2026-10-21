# 🌈 GlitchByte Phantom Labs | Beginner Runtime Recipes

**Simple · Medium · Extra** — choose how much to run, see real feedback, and understand the output.

**This is a documentation standard, not a new flag implemented by every tool.** A recipe must use the *actual command-line options* from its linked source/README. `--simple`, `--medium`, `--extra`, `--save`, and `--live` are not universal flags. Do not invent them.

**Publishing this everywhere:** Our [Build → Run → Publish → Vault standard](BUILD_PUBLICATION_STANDARD.md) explains how every new tool gets unique artwork/source, these three verified recipes, colorful live results, accurate save/Firefox notes, and links through HQ, Cultivation, Tool Vault, and verified Backup HQ.

**✅ Tested in the lab:** `python3 "$SAVER" --o findomain_results.txt -- findomain -t facebook.com` displayed Findomain's public-source results and a saved TXT transcript in Ubuntu after 21 seconds. Public data can be incomplete; this output contains both findings and provider messages, not a normalized hostname-only export. [Full guide](EASY_SAVE_ALL_TOOLS.md).

## 💾 Universal `-o` / `--o` saver instructions

**[Open Easy Save for Every Tool](EASY_SAVE_ALL_TOOLS.md).** New builds should natively support both spellings for opt-in plain-text results. Existing tools without native support can use [the shared Python save runner](../scripts/phantom_easy_save.py): `python3 "$SAVER" --o results.txt -- python3 -u <real tool and arguments>`. This runner saves the **printed terminal transcript**, not native JSON/CSV/HTML, and does not prevent legacy tools from saving their own files. SUBDOMINATRIX natively exports deduplicated hostname candidates via either `-o` or `--o`.

## 🌹 Triad Forge: bounded Simple / Medium / Extra commands

[Read the real Triad Signal integration guide](integrations/TRIAD_SIGNAL_2026.md). All three Go tools were located on Ubuntu; **Waybackurls passed live**, printing 20 URL lines. The earlier passive Amass and GAU runs each timed out at 45 seconds; a GAU missing `~/.gau.toml` message is nonfatal. The new companion runs independently bounded source checks concurrently, prints real `FOUND`/`TIMEOUT`/`PARTIAL-TIMEOUT` labels and supports opt-in native `-o`/`--o` clean candidate TXT. Its separate CI/offline verification and Ubuntu end-to-end test must be distinguished from the original tools' checks.

## 💾 Easy save convention for updated tools

Where implemented, use **`-o name.txt`** to keep plain-text results while still displaying real-time intelligence in the terminal. If omitted from terminal-only tools, nothing is saved. For SUBDOMINATRIX's updated source, `-o` creates only the requested hostname TXT and never overwrites an existing file:

```bash
SCRIPT="$HOME/PhantomLabsLaunchers/subdominatrix_live_signal_2026/subdominatrix_live_signal_2026.py"
python3 -u "$SCRIPT" example.com --terminal-only --color always -o names.txt
```

The legacy `--out DIRECTORY` option is **not** the same as `-o filename.txt`. Each future tool needs its own tested CLI support; this is not a universal preexisting flag. See [SUBDOMINATRIX's guide](tool-showcases/SUBDOMINATRIX.md).


## Permanent real-world example requirement

For future network research tools, the [LIVE OPSEC / OSINT release gate](LIVE_OSINT_REAL_OUTPUT_STANDARD.md) requires **two tested, real public-domain query examples** with exact commands, live source/provider status and observed outputs. For example, `facebook.com` can be a public-source domain for passive DNS, certificate or registration records. Name the actual date/version of any recorded result, and warn that results, rate limits and source availability vary. Never present a canned demo, placeholder profile, mocked response or decorative screenshot as live research. Keep useful offline demos for regression tests and teaching, with clear labels. Only use active network checks on authorized scopes.

Local hashing/forensics tools must show actual file results instead; they need no invented internet component.

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

## 🌹 SUBDOMINATRIX Live Signal recipes (published)

**Updated SUBDOMINATRIX Findomain recipe:** use `--terminal-only --findomain --timeout 8 --cli-timeout 60` to separate source and CLI limits, show live findings, and avoid saved report files. See [the complete revised tool guide](tool-showcases/SUBDOMINATRIX.md) for tested syntax, provider errors, and the offline/Firefox distinction. CI and the user's Ubuntu live retest passed: 151 unique candidate hostnames, with only the user-requested TXT saved.



The updated [SUBDOMINATRIX build page](tool-showcases/SUBDOMINATRIX.md) now supports `--terminal-only --color always` for real public-source discoveries with **no saved report files**, while keeping the original automatic Firefox/HTML export behavior when that flag is omitted. The three updated runnable examples are in its guide. Remember: this flag belongs to SUBDOMINATRIX and is not available in all tools.

## 🌐 Verified external Findomain recipes

For **Findomain**, an already-installed third-party tool, use our [Simple / Medium / Extra copy-and-paste terminal guide](integrations/FINDOMAIN_LIVE_CHECK.md). The user's `findomain -t facebook.com` public-source run completed in 23 seconds. No file export was requested. The guide also explains optional `tee` saving, the broken lower-priority `/usr/bin/findomain` text placeholder, and safe boundaries for direct network checks.

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
