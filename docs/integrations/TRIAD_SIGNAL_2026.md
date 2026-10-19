# 🌹⚡ Triad Signal 2026 | Fast feedback and safe time budgets

**GlitchByte Phantom Labs · Standalone companion for the local Triad Forge installation**

[← Tool Vault](../TOOL_VAULT.md) · [HQ](../../README.md) · [Beginner Runtime Recipes](../BEGINNER_RUNTIME_RECIPES.md) · [Easy Save for Every Tool](../EASY_SAVE_ALL_TOOLS.md) · [Cultivation Room](../CULTIVATION_ROOM.md)

## Observed Ubuntu results (October 19, 2026)

The user found the original Triad Forge workshop installation at
`$HOME/PhantomLabsLaunchers/glitchbyte_triad_forge_2026`, the ZIP
`$HOME/Downloads/glitchbyte_triad_forge_2026.zip`, and
`verify_triad.sh`. The workshop ZIP contains `build_01_amass_v4.sh`,
`build_02_gau.sh`, `build_03_waybackurls.sh`, `install_all.sh`,
`verify_triad.sh` and supporting files.

The user then confirmed all three installed executables. An independent
**45-second live sample** against `example.com` yielded:

| Installed utility | Real user-side result | Interpretation |
|---|---|---|
| Amass passive | 45-second timeout | Installed; full live result **not yet proven** |
| GAU | 45-second timeout and missing `~/.gau.toml` warning | Installed; config warning is **nonfatal** per upstream; complete live retrieval **not yet proven** |
| Waybackurls | **Completed**, printed **20 URL lines** (15 shown on screen) | Live archive collection **passed** |

Two timeouts are not evidence of broken binaries. The script that limited output to 15 visible lines hid useful counts on timeout; these must not be mistaken for zero. Archive URLs may be historic, incomplete or stale and **do not** prove current service availability.

## ✅ Companion's actual Ubuntu run (October 19, 2026)

The standalone, CI-tested `triad_signal_2026.py` companion was run by the user against `example.com` with `--amass-seconds 65 --gau-seconds 50 --wayback-seconds 25 --color always -o "$HOME/triad_check2.txt"`:

| Module | Reported result | Notes |
|---|---|---|
| Amass | `timeout / 0 candidates` at 65.03s | Printed out-of-target NS relationship notices involving Cloudflare, not normalized `example.com` subdomain candidates |
| GAU | `timeout / 0 candidates` at 50.01s | Warned of missing optional `~/.gau.toml`, used defaults |
| Waybackurls | `complete-no-results / 0 candidates` at 0.87s | Exit 0 but zero URLs in this run, in contrast to the earlier independent 20-line run |

**`[SAVED] TXT /home/deadwoodrosie/triad_check2.txt | 0 candidate lines`** verifies explicit save-file creation, not populated results. The script produced accurate module-level status, returned to the shell, and did not modify the original local Triad Forge installer ZIP. **Installed commands, launcher feedback, timeout handling and optional save are verified on Ubuntu.** Complete live collection from Amass/GAU and consistent archive results are **not** verified. Provider availability and this demonstration domain can affect results; do not treat zero candidates as proof that a domain lacks hosts or archived URLs.

## 🔐 Saved-TXT privacy patch (October 19, 2026)

A live Ubuntu privacy check found `600 ~/findomain_results.txt` (owner-only) but `664 ~/triad_check2.txt` (group-readable and world-readable where directories permit). The original Triad Signal companion inherited the shell's permissive file-creation mask. New `-o` / `--o` TXT results now use **exclusive file creation with explicit 0600 permissions** regardless of the shell umask; neither the user's original ZIP nor existing saved files are silently changed. An offline test simulates `umask 000` and verifies new output permissions. The user subsequently ran `chmod 600 ~/triad_check2.txt`, and the follow-up `stat` confirmed owner-only **0600**. To receive the patch locally, download the updated companion **to a separate filename** in the same folder, then use that filename on subsequent runs. No network scans are required to verify permissions.

## ✅ Local follow-up: old report secured, patched companion downloaded

The user confirmed `chmod 600 ~/triad_check2.txt` worked: the old report's mode changed from **0664** to **0600**. They successfully downloaded the fixed [main-branch companion](../../scripts/triad_signal_2026.py) under the separate local filename `triad_signal_private_2026.py` and its `--help` displayed `-o, --o`. The published source and offline test verify new file creation at mode `0600`, including a permissive umask. **A new real opted-in report from the patched local companion has not been created yet**, so distinguish local help check from a local real-file-permission retest. The original installer ZIP and earlier scripts were left intact.

## What this companion does

[**Open the real Triad Signal Python source**](../../scripts/triad_signal_2026.py).

It runs the **already-installed** Amass, GAU and Waybackurls with independent, capped time budgets, concurrently rather than making the user wait for three sequential timeouts. Each process prints color-coded actual discovered names/URLs and short warnings, and keeps partial findings on timeout. GAU uses a single Wayback provider for this bounded check rather than aggregating four different provider endpoints. Amass uses documented passive mode, **not active enumeration or port scans**.

The companion itself writes **no reports by default**. Installed tools such as Amass may still create their **own databases or caches**, independently of the companion. It does not change their configuration, install binaries, modify the user's ZIP or launch Firefox.

A native `-o name.txt` or `--o name.txt` saves the union of **actual normalized public-source hostname and URL candidates**, not banners, traceback, provider notices or synthetic data. Existing file names are never overwritten. The same report may contain both hostnames and full URLs, distinguishable by their syntax. Results are limited to the requested domain or its subdomains.

**Source-specific built-in flags differ:** GAU natively uses `--o`; Amass uses `-o`; Waybackurls normally prints URLs. Our companion makes both save spellings consistent without changing original program flags.

### Install the companion once (does not touch your local Triad Forge ZIP)

```bash
LAB="$HOME/PhantomLabsLaunchers/triad_signal_companion_2026"
mkdir -p "$LAB"
curl -fL --retry 1 --connect-timeout 12 --max-time 60 \
  "https://raw.githubusercontent.com/Hellfire13666/glitchbyte-phantom-labs/main/scripts/triad_signal_2026.py" \
  -o "$LAB/triad_signal_2026.py"
python3 -B "$LAB/triad_signal_2026.py" --help
```

Use this download **only after it has been published to main**. A no-install review version remains separate from historical archived binaries. Optional offline unit tests live in `tests/test_triad_signal_2026.py`.

## 🌱 SIMPLE | Confirm the one module already known to work

```bash
LAB="$HOME/PhantomLabsLaunchers/triad_signal_companion_2026"
PATH="$HOME/go/bin:$HOME/.local/bin:$PATH" \
python3 -B -u "$LAB/triad_signal_2026.py" example.com \
  --only waybackurls --wayback-seconds 25 --color always
```

Prints real Waybackurls results immediately. **No file saved.** It is a historical URL look-up, not a current-site health check.

## ⚡ MEDIUM | Investigate GAU with one provider only

```bash
LAB="$HOME/PhantomLabsLaunchers/triad_signal_companion_2026"
PATH="$HOME/go/bin:$HOME/.local/bin:$PATH" \
python3 -B -u "$LAB/triad_signal_2026.py" example.com \
  --only gau --gau-seconds 40 --color always
```

The missing `~/.gau.toml` warning can appear even when GAU works. Any candidate URL observed before the timeout is shown and retained as a **partial timeout**; without a result, it is labeled **timeout**. Neither outcome should be silently treated as success.

## 🔥 EXTRA | Run all three together and opt in to saving

```bash
LAB="$HOME/PhantomLabsLaunchers/triad_signal_companion_2026"
PATH="$HOME/go/bin:$HOME/.local/bin:$PATH" \
python3 -B -u "$LAB/triad_signal_2026.py" example.com \
  --amass-seconds 55 --gau-seconds 40 --wayback-seconds 25 \
  --max-show 15 --color always -o triad_results_2026.txt
```

Because the three utilities are launched concurrently, their independent limits generally make the operation bounded by the slowest one rather than by the sum. Processing/termination can take a little longer than the specified limit. `-o` and `--o` mean the same thing. This command writes only one **explicitly requested** TXT with deduplicated candidate domains/URLs; choose another name if it already exists.

The script returns a nonzero status when a module fails or times out, even if it finds partial results. A saved TXT with some entries doesn't mean every source completed.

## Interpreting the output

- `[AMASS][START]` / `[GAU][START]` / `[WAYBACKURLS][START]`: a real installed command was launched.
- `[MODULE][FOUND]`: a candidate name or URL reported by that program; only values within the target domain are kept.
- `[MODULE][NOTICE]`: tool feedback, such as GAU's optional config file warning.
- `[MODULE][TIMEOUT]` / `[MODULE][PARTIAL-TIMEOUT]`: terminated when its own deadline elapsed. Partial results remain visible and are eligible for saving.
- `[MODULE][COMPLETE]` / `[MODULE][COMPLETE-NO-RESULTS]`: executable returned exit 0, with or without candidates. Neither implies the source returned a complete census.
- `[SAVED] TXT`: an explicit request to save real candidate lines succeeded.
- `[DONE] No companion report saved`: you did not supply `-o` or `--o`.

**Permissions and scope:** use public-source lookups responsibly and follow provider terms/rate limits. This companion intentionally does not perform active DNS checking, HTTP crawling, port scanning or vulnerability testing. Sensitive discoveries should not be published automatically.

## Troubleshooting

Run `type -a amass gau waybackurls` if a command is missing. The companion searches your current `PATH`; it does not download or install tools. Review `gau -h` and `amass enum -h` if your installed versions have different flags. The GAU config-file warning can be ignored if you accept default settings. In very slow environments, run the modules separately with `--only` and small limits; **do not** conclude zero findings means zero infrastructure.

The preserved installer/readme files are local to the user's machine. Their complete source was not published in the linked HQ repository as part of this companion. We cannot claim the original Triad Forge ZIP contains this newer script; update the archive and checksums only after a separately verified snapshot.
