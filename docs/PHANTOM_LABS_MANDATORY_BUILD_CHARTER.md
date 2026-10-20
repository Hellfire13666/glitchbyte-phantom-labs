<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-B6FF00?style=flat-square&logo=github&logoColor=black"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹⚡ GlitchByte Phantom Labs | Mandatory Build Charter

**Workshop owner/creative identity:** RosieGlitchByte · **Official GitHub account:** [Hellfire13666](https://github.com/Hellfire13666) · **Platform:** Python 3 and Ubuntu/Linux, with Go and Firefox where a tool genuinely requires them.

This is the **persistent checklist for every future standalone tool**, upgrade and tool publication. It records the user's stated requirements and complements the [Build → Run → Publish → Vault Standard](BUILD_PUBLICATION_STANDARD.md), the [Beginner Runtime Recipes](BEGINNER_RUNTIME_RECIPES.md), the [Release Checklist](RELEASE_CHECKLIST.md) and the [Tool Vault](TOOL_VAULT.md). It does **not** certify that all older tools already meet these requirements.

## 🧭 Exactly three lab identities, plus supporting infrastructure

1. **[GlitchByte Phantom Labs HQ](../README.md)**: the main creative, coding and tool hub; official workshop mascot identity and index.
2. **[Cultivation Room](CULTIVATION_ROOM.md)**: foundations, seeds, prototypes, fixes and tests, following **SEED → CULTIVATE → TEST → LAUNCH**. It is a room/page within HQ, **not an invented fourth lab or a required new repository**.
3. **[RosieRiot Overdrive](https://github.com/Hellfire13666/rosieriot-overdrive-2026)**: its own high-powered workstation and tool repository, with its own releases and artwork.

**[Phantom Backup HQ](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases)** is **supporting public backup/release infrastructure**, not a fourth creative lab. **[Tool Vault](TOOL_VAULT.md)** and the [Ecosystem](ECOSYSTEM.md) are the navigational directory. The public Vault must **never** receive private sources, secrets, research reports or backup bundles simply because a tool's source repository exists.

## 🛠️ Non-negotiable checklist for each **independently publishable new tool**

### A. Real, original, separate working tool
- [ ] **Distinctive project name, unique repository slug, unique package/folder, Python filename, launcher/entry point, output basename/report folder and ZIP name.** Check for prior names before using them; never overwrite unrelated working tools or release archives.
- [ ] Actual functional source, not a mockup. Build for **Python 3 on Ubuntu/Linux** by default; document verified dependencies and optional third-party binaries. Include copy-and-paste install/run commands and an unambiguous `--help`.
- [ ] A **separate dedicated GitHub repository for each independent tool when it is approved for publication**, with its **own README/landing page and an individual setup/showcase page in HQ**. A prototype may remain local/private until tested; do not falsely call it uploaded or published.
- [ ] A unique launcher and installer/bootstrap or setup instructions suitable for the actual project; add runnable example input and clearly specified real outputs.
- [ ] Avoid destructive updates, duplicate names and clashes with other tools; preserve previous source versions and document migration when changing compatibility.

### B. Distinctive custom art and Glitch HEX visual identity
- [ ] **Individual visual theme, personalized art/cover or repository image, logo/mascot concept, README visual, palette and terminal presentation**. Artistic treatment should match the actual tool's job, not merely attach a generic hacker portrait.
- [ ] RosieGlitchByte / Anonymiss is the **overall flagship identity**, but **not every tool must show Rosie's face**. Tools may have their own character, mask, animal, abstract symbol, or visual metaphor.
- [ ] When explicitly depicting canonical Rosie: adult woman with long black/dark hair, selective electric-blue highlights and **brown eyes**; respect anatomically believable hands (five fingers), natural proportions and context-specific outfits.
- [ ] Rotate among **hot pink #FF1493 / deep black #080808**, acid-lime #B6FF00, electric cyan #00F5FF, ultraviolet #8A2BE2, rich orange/yellow/red and toned-down/natural palettes. A glitch is an **effect**, not one mandatory color. Vary layouts/backgrounds and use only a few intentional props when appropriate; avoid repeating identical faces and compositions.
- [ ] Keep art distinct from actual screenshots/results, and don't embed trigger/working labels or filler text in artwork unless requested. Create art when the build includes that deliverable; never imply an uncreated image is already in the repository.

### C. Real feedback, examples, and usable operation
- [ ] High-quality, **colorful terminal startup, progress, source/error notices, results, summary and outcome**. Include meaningful accessible plain-text labels, support non-ANSI output, and show **real** findings from real operations, not invented data.
- [ ] An **offline synthetic demo** and deterministic tests wherever sensible; label all demo/sample data clearly. Use a true example command for a safe target or user's local file.
- [ ] **SIMPLE · MEDIUM · EXTRA**: three distinct, tested, copy-and-paste Ubuntu examples in that tool's README/setup page, with requirements, expected outputs, explanation, running time/load and troubleshooting. **Do not invent command flags** to fill tiers; adapt the levels to what the tool really does.
- [ ] For tools with live sources: clearly distinguish passive historical/public data, live DNS/HTTP/other active probes, authorization and provenance; surface partial findings, 429 rate limits, slow internet timeouts and honest uncertainty. Never claim that a username/phone/hostname match proves a real-world identity.
- [ ] Firefox/HTML/dashboard integration only when actually functional. State which exact mode opens the browser, which mode saves local files, and how to stay terminal-only.

### D. Native easy save, output privacy, and safe operation
- [ ] **Terminal-first default: show the results live; save nothing unless requested**, unless a documented project-specific artifact is inherent to the tool. When meaningful, implement **both** native `-o name.txt` and `--o name.txt`; define exactly what the output contains and never overwrite existing reports.
- [ ] For intentionally saved research/identity/phone outputs: owner-only directories **0700**, newly created files **0600**, unique or exclusive-create names, no unapproved cloud upload. Treat symlinks, old permissions, overwrites and errors carefully; test permissive-umask behavior.
- [ ] Keep examples, reports, Git history, keys, tokens, private identifiers and user research out of public source/release artifacts. Respect provider policies and active probing authorization. An offline regression test isn't a complete security audit.
- [ ] Use clear exit statuses, Ctrl+C behavior, bounded network calls and timeout/rate-limit controls that accommodate slow Ubuntu internet. Preserve working output even if one permitted public provider fails.

### E. Test, document, publish and back up each release
- [ ] Syntax/build checks, offline unit/regression tests, real local smoke tests, and relevant integration checks pass; report accurately which are incomplete. Check CLI help and file-permission/collision behavior.
- [ ] **Own GitHub README, individual HQ tool page, source/setup link, three runnable example recipes, original artwork, proper credits/license, requirements, tests, launcher, exact paths and actual supported flags.**
- [ ] Add a **small, color-coded `UPLOAD FILES` link at the top right** of relevant GitHub README/HTML/landing pages and tool documentation (where the platform permits it), pointing to the **correct repository upload door**. Each tool/lab may use a different Glitch HEX badge color. It is a navigation link, not evidence that an upload occurred.
- [ ] Make visible working navigation across HQ, Cultivation Room, RosieRiot when relevant, **Tool Vault**, Ecosystem, individual tool repository and proper Backup HQ entry. Maintain the **Tool Vault index and automated missing/duplicate-entry guards**. Do not create fake destinations.
- [ ] Create a **new, versioned source/release ZIP with README, checksums/manifest, tests and required assets** and run archive/hash verification; retain earlier releases. A tag, GitHub Release, local ZIP and separate backup are **different milestones**.
- [ ] **Confirm public-versus-private visibility before uploading.** Start with private staging when source/privacy review is unfinished. Do not make anything public or move private source to the **public Phantom Backup HQ** without explicit owner approval.
- [ ] Record an actual versioned recovery snapshot in an **appropriate visibility-matched** vault and verify checksum and restore where possible. A local backup is not independent off-device redundancy.

## 🎨 Tool identity checklist for every repository

Each separate tool page should contain its **own**:
- name + short purpose, distinct Glitch HEX visual theme, image/cover/mascot and an appropriate top-right **UPLOAD FILES** link;
- Ubuntu installation steps, working executable paths, launcher, `--help`, **SIMPLE/MEDIUM/EXTRA** examples, realistic expected result snippets and sample data clearly labelled;
- live colorful output notes, supported modes, opt-in/no-save behavior, Firefox notes only if actually implemented;
- tests, privacy/security caveats, known limitations, source/release versions, checksum, recovery and correct HQ/Cultivation/Tool Vault/Overdrive links.

## 🧪 Current verified status and future work | October 19, 2026

| Project | Evidence completed | What remains |
| --- | --- | --- |
| **HEXWRAITH Privacy Edition v1.1.1 RC2** | Separate private [GitHub repository](https://github.com/Hellfire13666/hexwraith-domain-atlas-privacy-2026), tag `v1.1.1-rc2`, 14 passing tests, clean clone matching RC2, verified ZIP and restored Git bundle, GPG encrypted bundle verified by SHA-256 and successful byte-for-byte stream-decryption | **Independent off-device encrypted copy remains pending**; public publication not approved. |
| **VelvetEcho Persona Observatory** | 17 existing local reports secured to `0600`, report directory `0700`; separate privacy-patched launcher and **3/3** offline regression tests | Source-only ZIP/checksum was *requested*, but successful user verification was **not yet reported**; original launcher untouched. No public source/report upload implied. |
| **SUBDOMINATRIX** | Live public-source workshop run reported **151** unique hostname candidates; terminal-only opt-in save works; exclusive output creation found | Future output-permissions hardening of full-report mode, if desired. No need to interrupt known-good launchers now. |
| **Triad Signal** | Earlier `-o` / `--o` and explicit `0600` output checks passed; original Go modules had mixed live provider outcomes | Broader audits are tracked separately; do not call every provider live-verified. |
| **RosieRiot Overdrive** | Real live workstation results were demonstrated, with an existing separate repo | Some original file-writing behavior still warrants targeted future review; not a confirmed new incident. |
| **HEXWAKE Palette Foundry** | Maintained source uses random stems and exclusive creation for palette outputs | No default local output folder existed in final read-only inventory; private-output defaults are not comprehensively certified. |
| **RIFTSEAL Evidence Fingerprint Forge** | New local Python tool computed SHA-256 `b1728a0b480eae045ad289e59a69b3d20fd79e787d81bf4561c9f9428bb800a7` for HEXWRAITH RC2 ZIP (35,711 bytes), matching independently verified checksum; printed `SAVE OFF` | **RIFTSEAL Integrity Gate** companion was drafted but **user-run installation/test results not yet confirmed**. Finish functional compare/verify checks, then full independent tool page, art, three examples and own GitHub repo before calling it published. |
| **RootSignal Cultivator** | Previously planned concept for Cultivation Room: Python 3 idea-seeding/workflow engine | A **planned next new project**, not yet a verified built or published tool. |

**RIFTSEAL v1.0.0 completion note (October 19, 2026):** a source-only kit with custom art, two Python 3 CLI utilities, own README/showcase, three runnable recipes, 16 passing offline tests (including clean extraction), release manifest and ZIP SHA-256 `c2ce1ad5f8a9a2101b9664664c273a14a0e7b59cbaf5677a7696fe1d9a845a13` has been produced. Dedicated GitHub repository, account-side Ubuntu installation and backup remain **pending**, not falsely reported as complete. See [RIFTSEAL page](tool-showcases/RIFTSEAL.md). Resume with the owner-approved publication step, then RootSignal Cultivator; respect the requested clean-chat break.

**Focus:** close scoped output-audit phase without claiming a general security certification; return to **new functional builds**. Immediate build sequence: **(1)** validate RIFTSEAL's Integrity Gate companion and create its distinct art/page/SIMPLE–EXTRA examples; **(2)** develop **RootSignal Cultivator** as a separate, genuinely new Cultivation Room tool; **(3)** publish each independent tool through its own reviewed repository and appropriate linked index/backup gates. Keep older release/backup work tracked rather than repeating it unnecessarily.

---

**Principle:** *One real tool. One distinctive identity. One reliable set of examples. One discoverable page and dedicated repository when released. One verified recovery path. No overwritten originals, fake results or invented publication claims.*
