# 🌹 GlitchByte Phantom Labs | Build → Run → Publish → Vault Standard

**Applies to every new creation and every explicitly requested tool upgrade**, whether it is OSINT/public-domain research, a local file utility, a creative script, a learning game, a Python/Go project, or a Firefox-based interface.

The purpose is to make every release **beautiful, useful, discoverable, runnable by beginners, and recoverable**. This is a *publication checklist*, not a claim that all legacy projects have already been upgraded.

## 1. Keep the creation unique

- Use a distinctive project name, code filenames, package/folder names, launcher names, artwork identity, and any future report names.
- Keep the original tool and Git history intact. Do not overwrite unrelated existing files, change established paths, or silently replace a working build.
- Different tools can have different aesthetics, not always Rosie's portrait. Rotate legible Glitch HEX color palettes.
- Ship working source and instructions, not just a marketing illustration. Label artwork or sample output as illustrative when appropriate.

## 2. Show meaningful results **as the tool runs**

New and updated tools should have real-time, colorful terminal feedback appropriate to what they do:

- Startup banner, version, selected mode, source/target/file scope, and settings.
- Per-step progress and useful **actual** output, not merely a spinner or a final empty summary.
- Clear `FOUND`, `POSSIBLE`, `NOT_FOUND`, `UNKNOWN`, `PARTIAL`, `RATE-LIMITED`, `TIMEOUT`, `ERROR`, and `DONE` semantics where those states apply.
- Honest provider feedback, measured totals, elapsed time and a summary; stream/flush output where feasible.
- On slow internet, bounded waits, retry/cooldown feedback and partial results. Never fake findings, invent API responses, or promise a precise runtime.
- For offline projects, show real progress for their actual workload. Do not pretend an offline puzzle or palette generator performs online scans.
- Accessibility: useful non-color text labels; support non-ANSI terminals.

For network research, passive public-source lookups are distinct from direct DNS, HTTP, port, template or other active probes. Active tests must have an authorized scope. Respect provider rate limits and protect private data.

## 3. Firefox and files: delightful **but honest**

- Keep Firefox integration for tools that *actually support* a local HTML app/report or appropriate browser interface. The browser is a companion to the running terminal where possible.
- Do not invent a dashboard or treat promotional artwork as a working UI. Never activate third-party cloud dashboards or upload results without explicit intent.
- **Default for new live terminal tools: print to screen; do not persist report files unless the person selects a save/export option.** Document the *actual supported* save command, output format and path.
- Some existing legacy scripts write HTML/JSON/CSV/TXT automatically, and some Firefox experiences require local generated files. Until those programs are explicitly updated and verified, their documentation must accurately say they save files. `--no-open` is **not** the same as `--no-save`.
- Never claim that every tool accepts `--save`, `--live`, `--simple`, `--medium`, `--extra`, or Firefox flags. Always verify `--help` and the code.

### 💾 Easy opt-in saving standard for new builds

For future terminal-first tools, prefer a short, beginner-friendly **`-o name.txt`** option to save human-readable output **only when requested**. Continue to print results live and preserve colorful status on screen. Clearly document what TXT contains (e.g., one deduplicated candidate hostname per line) and avoid overwriting older reports. If a tool supports structured export, document its actual `--json`, `--csv`, or other flags separately. Do **not** assume all existing tools already recognize `-o`: update the actual program, test it, and then add an example to that project's Simple/Medium/Extra recipe. Distinguish any older `--out` output-folder option from the new `-o filename.txt` convention.


**New easy-save rule:** every *future* noninteractive terminal tool must implement both native `-o name.txt` and `--o name.txt` when a plaintext result makes sense, create no TXT file unless requested, never overwrite previous results, and continue to print live feedback. The output must contain meaningful tool results, not merely a log transcript. Where special UI or file exports are needed, document those instead. [Universal easy-save instructions for existing tools](EASY_SAVE_ALL_TOOLS.md) provide a shared runner; the runner does not automatically add native flags or turn off legacy exports.

## 4. Every tool gets beginner **SIMPLE · MEDIUM · EXTRA** recipes

Each project README / build page must include **three real, tested copy/paste Ubuntu/Linux examples**:

| Level | Purpose | Show |
|---|---|---|
| 🌱 **SIMPLE** | First working run | prerequisites, exact command, actual output, where to look |
| ⚡ **MEDIUM** | More intelligence or richer features | documented source/module choices, live feedback, sensible limits |
| 🔥 **EXTRA** | Full documented features when available | prerequisites, any authorization/scope checks, how to read more advanced results |

Each recipe includes installation or verified prerequisite paths; input placeholders; what actual findings mean; rough relative run load, timeouts, provider failures; whether outputs are stored; optional file export; Firefox behavior if supported; `--help`; Ctrl+C and troubleshooting. Adjust levels to the project's actual complexity; don't invent extra functionality merely to fill a third tier.

Full guide and Markdown template: **[Beginner Runtime Recipes](BEGINNER_RUNTIME_RECIPES.md)**.

## 5. Publish it through **all relevant hub doors**

A new build or release is only *documented as distributed* after its pages and links have been checked:

1. **[Phantom Labs HQ](../README.md):** new release/featured entry as appropriate, with a working destination link.
2. **[Cultivation Room](CULTIVATION_ROOM.md):** build stage, tests, upgrade status, and link to its release guide.
3. **[Tool Vault](TOOL_VAULT.md):** one distinct source door and one accurate how-to/setup door, without breaking the index/test guard.
4. **[Tool Starter Guide](TOOL_STARTER_GUIDE.md)** and **[Beginner Recipes](BEGINNER_RUNTIME_RECIPES.md):** standard guidance stays linked; add a tool-specific example when it materially helps, not a duplicate of every README.
5. **Dedicated tool repository/README** (when it has one) and **individual build page:** actual commands, examples, supported modules, tests, screenshots/artwork, troubleshooting and cross-links back to all labs.
6. **[RosieRiot Lab](ROSIERIOT_OVERDRIVE_LAB.md)** when a release is an Overdrive feature/companion; do not imply all unrelated tools belong to RosieRiot.
7. **[Phantom Backup HQ](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases)** and its recovery index: link to the *actual verified* new snapshot, once archived. Update allowlists for new standalone repos. Never describe unrun backups as complete.
8. **[Ecosystem index](ECOSYSTEM.md)** and any relevant launch/Firefox pages: add a working link when that project is included.

**Distribution means linked navigation and accurate per-tool instructions, not copying all code and reports onto every page.** Not every hub requires an individual spotlight, but every new published tool should be discoverable from the HQ/Tool Vault/recovery paths appropriate to its release.

**Integration test distinction:** locating external tools and confirming executable binaries is an installation check, not proof of live integration. For Go/Python wrappers with multiple providers, disclose provider-specific status and partial findings (e.g., Amass/GAU timeout versus Waybackurls success), provide bounded timeouts for slow connections, and avoid describing a tool as fully tested until live/real output has been observed. The [Triad Signal example](integrations/TRIAD_SIGNAL_2026.md) documents an honest partial first run and a separate runtime companion.

## 6. Verify before calling it complete

- [ ] Source, independent folder, commands and dependencies exist; no collisions.
- [ ] Syntax/build and offline tests pass; live functionality verified when the release claims it.
- [ ] SIMPLE, MEDIUM and EXTRA examples execute as documented; each accurately explains output and files.
- [ ] Colorful live/intel feedback exists for applicable tools, with partial/failure status.
- [ ] No-save default or legacy saving is described truthfully; Firefox behavior tested or explicitly marked optional.
- [ ] Safe scope, credentials, privacy, service rules, licensing and artwork rights reviewed.
- [ ] All intended hub links resolve to published files on the correct branch; source/guide/indexes updated.
- [ ] Versioned backup ZIP and manifests/checksums are created and verified **after** source changes (only then update Vault recovery entries).
- [ ] The original project and historic backup snapshots remain unchanged.

This policy guides **future work as each tool is built or revisited**. It does *not* silently retrofit all historical programs or automatically republish/rearchive new changes.
