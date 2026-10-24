# GLITCHBYTE ART VAULT CONVERTER · MX Linux

[![Approved Rosie neon Art Vault Converter v2 poster](../../creative-utilities-showcase-v1.0.3/02-ART-VAULT-CONVERTER/assets/ART-VAULT-CONVERTER-ROSIE-NEON-v2.png)](../../creative-utilities-showcase-v1.0.3/02-ART-VAULT-CONVERTER/assets/ART-VAULT-CONVERTER-ROSIE-NEON-v2.png)

**🎨 Official visual:** the owner-approved `convert3.png` Rosie artwork in the [Creative Utilities v1.0.3 showcase](../../docs/creative-utilities-showcase-v1.0.3/README.md). The poster illustrates the workflow; use the actual commands and safety notes in this README to operate the v2 program. Do not reinstall a working v2 shortcut merely to view the artwork.

**One tool, three working pieces.** This is the original GlitchByte Phantom Labs offline image converter built for the Hangout's 1 MiB artwork upload limit. Published here as an independent tool; no website/database changes.

| Piece | Purpose | Files |
| --- | --- | --- |
| 1 · Compression engine | Convert PNG/JPG/WebP and other still images into privacy-conscious WebP copies, normally at or below 900 KiB | `GLITCHBYTE-ART-VAULT-BATCH-OPTIMIZER-v1.py` |
| 2 · One-click Desktop shortcut | Install the familiar MX Linux XFCE shortcut; choose Execute/Allow Launching if prompted | `INSTALL_GLITCHBYTE_CONVERTER.sh` |
| 3 · New-only upgrade | Remember completed images outside the output folder, avoiding duplicate conversions after deleting uploaded WebPs | `glitchbyte_art_new_only_v2.py` and `INSTALL_NEW_ONLY_v2.sh` |

**Recommended for current installations:** v2. If yesterday's Desktop shortcut is already working, **do not reinstall** just to use the GitHub copy. These files are source preservation and optional reinstall recipes.

## MX Linux: first-time v2 install

1. Download the four files in this directory to **one local folder** on MX Linux.
2. In a terminal in that folder, run `sudo apt install python3-pil` only if Pillow is not installed.
3. Run `bash INSTALL_NEW_ONLY_v2.sh` **once**. The installer saves the program under `~/.local/share/glitchbyte-phantom-labs/art-vault-new-only-v2/` and creates **GlitchByte Art Vault Converter** on your Desktop.

The first v2 installation intentionally **remembers pictures already in the source directory as handled** without converting them, so only images added afterward are processed. Existing output copies are not deleted.

## Everyday recipe

1. Put **new originals** in `~/Desktop/GlitchByte-To-Upload`.
2. Double-click **GlitchByte Art Vault Converter** (select Execute / Launch in Terminal).
3. Find compressed WebP copies in `~/Desktop/GlitchByte-Upload-Ready`.
4. Upload the COPIES at <https://glitchbyte.alwaysdata.net/crew/gallery>. Delete uploaded copies from **Upload-Ready** if desired; the saved history prevents identical originals from reappearing.

Safe command-line alternative:

```bash
python3 glitchbyte_art_new_only_v2.py \
  --source "$HOME/Desktop/GlitchByte-To-Upload" \
  --dest "$HOME/Desktop/GlitchByte-Upload-Ready"
```

The saved history is normally `~/.local/state/glitchbyte-phantom-labs/art-vault-new-only-v2-history.json`. **Do not delete it** unless you deliberately want previously handled images to become eligible again. The converter preserves original artwork and strips most source image metadata from its newly encoded WebPs.

## Legacy v1

```bash
python3 GLITCHBYTE-ART-VAULT-BATCH-OPTIMIZER-v1.py \
  --source "$HOME/Desktop/GlitchByte-To-Upload" \
  --dest "$HOME/Desktop/GlitchByte-Upload-Ready"
```

The historical installer `INSTALL_GLITCHBYTE_CONVERTER.sh` installs a v1 shortcut. Use **v2**, not v1, if you want "new only" history, and do not run both installers in succession as each targets the same Desktop shortcut.

**Requirements:** Linux, Python 3, Pillow (Debian/MX Linux package `python3-pil`). Completely offline processing; nothing is uploaded to GitHub or Hangout by this tool. No member information, passwords, or live backups are included in this repository.
