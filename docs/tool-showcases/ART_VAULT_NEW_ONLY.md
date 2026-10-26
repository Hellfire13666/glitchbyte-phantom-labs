# Art Vault New-Only Converter

**Offline new-image processing**

[Python source](../../tools/glitchbyte-art-vault-converter/glitchbyte_art_new_only_v2.py) · [Tool Vault](../TOOL_VAULT.md)

## COPY & PASTE BUILD RECIPE

Install or update a local Git checkout and use these offline, non-destructive tests. The script is not run during the syntax check.

```bash
# INSTALL: clone into a new working directory if needed
git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
cd glitchbyte-phantom-labs

# BUILD / TEST: syntax only, with no image or website processing
python3 -B -m py_compile tools/glitchbyte-art-vault-converter/glitchbyte_art_new_only_v2.py

# RUN: inspect this source's actual supported command-line options first
python3 -B -c 'from pathlib import Path; p=Path("tools/glitchbyte-art-vault-converter/glitchbyte_art_new_only_v2.py"); print("Source:", p, "exists:", p.is_file())'
```

## Run and find output

Consult [the original tool documentation](../../tools/glitchbyte-art-vault-converter/README.md) for executable usage, prerequisites, destination directories and files. This page does not assume a particular CLI flag or claim a real conversion or remote fetch was tested. Work on copies of pictures where relevant.

## Troubleshoot

If the syntax check fails, confirm the checkout is complete and `python3` is available. Review the specific script's help and usage before running any operation. No credentials are required for this offline syntax-only recipe.
