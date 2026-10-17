# 🌹 Official Phantom Labs Visual Kit

This document defines how to finish the **approved Rosie-themed GitHub homepage** without overwriting any tools.

## 1. Official hero illustration

The chosen hero must be an approved GlitchByteRosie creation:

- Brown eyes (when visible)
- Black or very dark hair with electric-blue highlights
- Recognizable Rosie appearance drawn from the user's reference set
- Small or tastefully blended Rosie figure relative to tool navigation
- Glitch accents can rotate, with hot pink, cyan and dark backgrounds as an option
- No unrelated substitute characters

**Pending art upload:** the visual preview made in ChatGPT is not yet a file in this GitHub repository. To display it on GitHub, upload the selected approved PNG as:

`artwork/glitchbyte-phantom-labs-official-hero.png`

Then remove the surrounding HTML comment markers around its image tag in the root `README.md`. The README currently contains the disabled image tag so visitors never see a broken link.

## 2. Banner placement

- Homepage image: below the `ROSIEGLITCHBYTE // CYBER TOOL FORGE` heading
- Tool ecosystem banner: optional image on `docs/TOOL_SHOWCASE.md`
- Starter guide banner: optional image on `docs/TOOL_STARTER_GUIDE.md`
- Keep all text and real project links accessible even if images cannot load
- Use compressed PNG or WebP and descriptive accessible alt text

## 3. Real versus concept features

The image mockups depict navigation panels, search boxes and tool cards. GitHub README pages support Markdown links and images, **not** functioning custom JavaScript apps or interactive tool runners. This repository makeover uses real Markdown links and copy-and-paste terminal commands. A working interactive dashboard needs a separate HTML/JS app or GitHub Pages site.

Do **not** add fictional GitHub star/watch counts, fictitious tests, or label local-only projects as published. Only link to existing repository files. Future tool releases get their own names, folders and documentation.

## 4. Review and publish

1. Preview the README and verify that all links work on the proposal branch.
2. Confirm the official Rosie hero is the exact approved image.
3. Run existing repository CI checks and confirm no tool files were changed.
4. Merge the design pull request after review.
5. If adding GitHub Pages later, design it as a separate, independently named project with its own build/test/release workflow.

## 5. Lab quality standard

Every new tool should include a runnable help command or clear help instructions, explicit setup/build/test directions, real examples, honest search result states, live progress when possible, saved report location, and an individual project identity.
