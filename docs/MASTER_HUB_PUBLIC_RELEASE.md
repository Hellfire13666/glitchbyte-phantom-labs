# 🌐 Master Hub v0.2.0: public release gate

Release must include **exact** matching files, unchanged from the locally verified archive:

- `glitchbyte-phantom-labs-master-hub-v0.2.0.zip`
- `glitchbyte-phantom-labs-master-hub-v0.2.0.sha256`

Correct expected SHA-256:

```
e5b1ef241ab8e3058fae593ecb1ea4fe26d95cdfb9eca1a0e84c656a1025fac7  glitchbyte-phantom-labs-master-hub-v0.2.0.zip
```

1. Review all packaged files including artwork reuse/redistribution permissions, license, and absence of private data. The repository uses a custom source-available license, not an OSI-approved license.
2. In `Hellfire13666/glitchbyte-phantom-labs`, open **Releases → Draft a new release**, use tag **`master-hub-v0.2.0`** and title **`GlitchByte Phantom Labs Master Hub v0.2.0`**.
3. Attach the exact `.zip` and `.sha256` above, not a browser-generated ZIP snapshot. Document Debian 13 Trixie and pending Ubuntu testing. Publish when the safety and license checks pass.
4. Confirm both files open in an incognito browser. Check `sha256sum -c` and `unzip -tq` against the GitHub-downloaded files, not just local copies.
5. Run the [single-paste install](MASTER_HUB_PUBLIC_INSTALL.md) on a clean Debian desktop account. Check real `START_HUB.sh`, `index.html`, HEXBAZAAR recipe/manual links, PHANTOM SPINE/RIFTSEAL recipes, card status and the XFCE desktop icon.
6. Only then promote the README's install button / release note from **candidate** to **verified public install**. Update the dedicated tool index whenever adding a new tool; the Installed Page Finder detects HTML pages but does **not** auto-create unique brand cards.

**No secrets, reports, generated `catalog.js`, or home-folder paths should be uploaded.** Do not claim GitHub public release or web hosting until the release actually exists.