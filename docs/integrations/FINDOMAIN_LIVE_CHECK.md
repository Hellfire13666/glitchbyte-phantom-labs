# 🌹⚡ FINDOMAIN | Live public-source discovery on Linux

**GlitchByte Phantom Labs · Checklist #2 · Verified user-side live run on October 19, 2026**

[← Tool Vault](../TOOL_VAULT.md) · [Simple / Medium / Extra recipes](../BEGINNER_RUNTIME_RECIPES.md) · [RosieRiot Lab](../ROSIERIOT_OVERDRIVE_LAB.md) · [Build & distribution standard](../BUILD_PUBLICATION_STANDARD.md)

> **Findomain is an externally maintained tool, not a GlitchByte-authored binary.** Our lab verified an already installed copy and documents how to run it; we do not bundle or silently replace its executable. [Official Findomain upstream](https://github.com/Findomain/Findomain) and [installation/usage guide](https://github.com/Findomain/Findomain/blob/master/docs/INSTALLATION.md).

## ✅ What was checked on Linux

- The command `findomain -t facebook.com` produced live hostname observations, visibly querying CertSpotter, crt.sh, Sublist3r, Threatcrowd, AnubisDB, urlscan.io, and Threatminer. The recorded run took **23 seconds** and finished normally. This verifies the already-installed executable's live public-source mode **for that test**, not the freshness or reachability of every hostname.
- Shell resolution showed a working candidate at `$HOME/.local/bin/findomain`, selected before `/usr/bin/findomain`.
- The old `/usr/bin/findomain` was a **9-byte text file containing `Not Found`**, not an ELF executable, and `dpkg -S` did not recognize it. The working user-local installation takes precedence. **Do not overwrite or delete system binaries blindly**; if PATH order changes, inspect `type -a findomain` again.
- Findomain's basic `-t` run printed output without specifying a report filename. No saved report was requested in that command.
- The installed Findomain build's complete `--help` output and advanced flags have **not yet been inspected**. Check local `findomain --help` before using advanced features documented upstream.

## 🌱 SIMPLE | Discover public candidate subdomains, no report

```bash
export PATH="$HOME/.local/bin:$PATH"
findomain -t example.com
```

Use a public domain of interest. The tool prints public-source results on screen. **Candidate hostnames are not proof of current DNS resolution, reachability, control or vulnerabilities.**

## ⚡ MEDIUM | Compare two passive public discovery engines

Both installed tools run sequentially; output remains visible and **neither command requests a saved report**.

```bash
export PATH="$HOME/.local/bin:$HOME/go/bin:$PATH"
TARGET="example.com"
printf '\033[95m◆ FINDOMAIN :: PUBLIC SOURCES\033[0m\n'
findomain -t "$TARGET"
printf '\033[96m◆ SUBFINDER :: ADDITIONAL PUBLIC SOURCES\033[0m\n'
subfinder -d "$TARGET" -silent
printf '\033[92m◆ BOTH PASSES COMPLETE\033[0m\n'
```

Results from the two programs may overlap. Seeing a hostname twice does **not** mean two independent confirmations of an active service. Slow APIs may return partial coverage.

## 🔥 EXTRA | Bounded additional DNS/HTTP checks, authorized target only

Use **only a domain you own or are explicitly authorized to test**. Findomain provides passive candidates; DNSX and HTTPX perform live resolution/service checks on a very small chosen scope rather than automatically probing the full discovered list:

```bash
export PATH="$HOME/.local/bin:$HOME/go/bin:$PATH"
TARGET="YOUR-AUTHORIZED-DOMAIN.example"
printf '\033[95m◆ FINDOMAIN :: PUBLIC DISCOVERY\033[0m\n'
findomain -t "$TARGET"
printf '\033[96m◆ DNSX :: ROOT + WWW CHECKS\033[0m\n'
printf '%s\n' "$TARGET" "www.$TARGET" | dnsx -silent -retry 1 -t 2
printf '\033[96m◆ HTTPX :: ROOT SERVICE CHECK\033[0m\n'
httpx -u "https://$TARGET" -sc -title -silent -timeout 10 -retries 0
printf '\033[92m◆ CHECKS COMPLETE\033[0m\n'
```

These commands perform only limited checks on the root domain and its `www` hostname; **they do not validate every discovered subdomain**. Advanced Findomain flags, such as upstream `-r` (resolvable names), should be used only after checking your version's `--help` and applicable authorization.

## 💾 Easy Save with both `-o` and `--o`

For a plain-text copy of Findomain's actual terminal output, use our [universal Phantom Easy Save runner](../EASY_SAVE_ALL_TOOLS.md). Findomain itself is an independently installed tool; **the `-o`/`--o` flags in this example belong to the runner**, not a new Findomain option. Install the runner using the linked guide, then run:

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
python3 "$SAVER" --o findomain_names.txt -- findomain -t example.com
```

`-o` is an equivalent shorter spelling. The TXT is a **transcript**, which may contain provider messages or banners alongside hostname candidates; it is not a normalized clean-hostname export. It saves no file without the flag, but Findomain has its own behavior. Choose a fresh filename for subsequent runs; existing files are not overwritten.

## 💾 Save only when deliberately requested

Default examples above do **not** request file export. To explicitly save a text transcript of the screen output:

```bash
findomain -t example.com | tee findomain_example.txt
```

The pipe may change color behavior in some versions. For Findomain's own output flags check your locally installed `findomain --help`. No Firefox dashboard is launched by these terminal commands; a future local HTML visualization would require a separately documented and tested companion tool.

## Troubleshooting / real-world limits

```bash
type -a findomain
command -v findomain
file -L "$(command -v findomain)"
findomain --help
```

- **`Not Found` / bad executable:** Check which binary the shell actually selects. Do not execute or trust a 9-byte `Not Found` placeholder.
- **Slow internet / missing sources:** provider rate limits, downtime, and old data can produce partial results. Use Ctrl+C to interrupt a long run.
- **No hostnames:** means no candidates returned in this pass, **not** proof the domain has no subdomains.
- **Privacy & scope:** consult service terms and rate limits; do not publish private reconnaissance or treat naming conventions as proof of sensitive access.

**Checklist outcome:** Findomain's basic live public-source discovery **PASSED** in the recorded Linux test in 23 seconds. Cleaning the invalid lower-priority `/usr/bin/findomain` is optional maintenance and not needed for the currently working executable. No custom Python code or verified backup archive was created by this documentation step.
