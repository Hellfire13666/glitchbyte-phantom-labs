# GlitchByte Phantom Labs · Public Privacy Release Standard

This checklist applies to every public tool, recipe, artwork and release across the Labs.

## Before publishing
- [ ] Use **Linux** or **Debian-based Linux** in public instructions; do not publish the developer's personal workstation details.
- [ ] Use relative project paths and neutral placeholders instead of personal computer names, local account names, or absolute filesystem paths. Shell-internal environment variables may remain where required for correct operation.
- [ ] Review README, shell installers, Python/Go source, launchers, demos, and screenshots for accidental identifying information.
- [ ] Check archives, HTML reports, text outputs, metadata and example files before distribution.
- [ ] Keep access credentials in local configuration, never in public source or examples.
- [ ] Validate examples and one-paste commands on the supported Linux environment.
- [ ] Preserve tools and avoid destructive bulk replacements.

## Review previous releases
Check historical commits, tags, downloadable archives and older projects separately. Editing a file today does not remove copies in history. If account credentials are ever accidentally published, invalidate them promptly.

## Audit status
Current file searches and selected direct reads have been completed for the main Lab and several active tool repositories. Archived binaries, older Git history and legacy projects remain under review. No blanket security certification is implied.
