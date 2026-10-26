# Share Card Doctor

**Read-only public link-preview inspection**

[Python source](../../tools/glitchbyte-share-card-doctor/share_card_doctor.py) · [Tool Vault](../TOOL_VAULT.md)

## COPY & PASTE BUILD RECIPE

Install or update a local Git checkout and use these offline, non-destructive tests. The script is not run during the syntax check.

```bash
# INSTALL: clone into a new working directory if needed
git clone https://github.com/Hellfire13666/glitchbyte-phantom-labs.git
cd glitchbyte-phantom-labs

# BUILD / TEST: syntax only, with no image or website processing
python3 -B -m py_compile tools/glitchbyte-share-card-doctor/share_card_doctor.py

# RUN: inspect this source's actual supported command-line options first
python3 -B -c 'from pathlib import Path; p=Path("tools/glitchbyte-share-card-doctor/share_card_doctor.py"); print("Source:", p, "exists:", p.is_file())'
```

## Run and find output

Consult [the original tool documentation](../../tools/glitchbyte-share-card-doctor/README.md) for executable usage, prerequisites, destination directories and files. This page does not assume a particular CLI flag or claim a real conversion or remote fetch was tested. Work on copies of pictures where relevant.

## Troubleshoot

If the syntax check fails, confirm the checkout is complete and `python3` is available. Review the specific script's help and usage before running any operation. No credentials are required for this offline syntax-only recipe.

## Easy-save terminal output

The optional [Phantom Easy Save guide](../EASY_SAVE_ALL_TOOLS.md) explains how to save program output. Its wrapper accepts `-o` or `--o` **before** the `--` separator. These options belong to the wrapper, not necessarily to this tool. For example, with the documented runner installed:

```bash
SAVER="$HOME/PhantomLabsLaunchers/easy-save/phantom_easy_save.py"
python3 "$SAVER" --o share_card_doctor_syntax.txt -- python3 -B -m py_compile tools/glitchbyte-share-card-doctor/share_card_doctor.py
```

Syntax checks normally print nothing on success. For a meaningful saved report, consult the original tool's supported usage and pass its actual command after `--`. The wrapper cannot create images or structured reports that the tool itself does not output.
