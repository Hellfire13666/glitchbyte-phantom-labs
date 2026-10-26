# 🔧 NODE-2026-001 // MXHX Shed Node.js 22 repair

**GlitchByte Phantom Labs Repair Shop · verified user field report · October 21, 2026**

![Node Repair neon workshop badge](node22-repair-logo.svg)

[← Repair Shop](README.md) · [← Phantom Tool Vault](../TOOL_VAULT.md) · [MXHX Shed upstream repository](https://github.com/masterxhackerx420-oss/mxhx-shed)

## When to use this repair

A Linux computer can obtain the MXHX Shed project but an npm installation fails and running the dev server ends in a syntax error at a modern JavaScript import in scripts/with-app-env.mjs.

**Observed system:** Debian-based Linux / Debian Trixie, nvm 0.39.1. The active runtime was **Node.js v0.10.48 with npm v2.15.1**, while MXHX Shed's published README requires **Node.js 22**.

### Error fingerprints

~~~text
fatal: destination path 'mxhx-shed' already exists and is not an empty directory.
npm ERR! code ENOTDIR
npm ERR! path .../mxhx-shed/node_modules/@types/pg/package.json
import { spawn } from "node:child_process";
^^^^^^
SyntaxError: Unexpected reserved word
~~~

The existing folder message means clone should not be repeated over the existing checkout; it was not the startup blocker. Node 0.10 cannot parse this modern ES module import and npm 2 is far too old for the current dependency graph.

## SIMPLE // Repair only the Node version

Run in an ordinary user terminal, **not sudo**:

~~~bash
nvm --version
nvm install 22
nvm use 22
node -v
npm -v
~~~

Expected: Node reports v22.x and npm a supported modern version. If nvm is not available, **stop and install or locate the appropriate version manager before continuing**. Do not delete the old Node binaries or rewrite system-level alternatives to attempt this fix.

Optional: make Node 22 the default for future nvm-managed shells:

~~~bash
nvm alias default 22
~~~

This setting may not affect shells where another startup script expressly selects a different Node version; check with node -v when reopening a shell.

## MEDIUM // Reinstall only this project's dependencies

Check the project folder exists and verify the active version first:

~~~bash
cd "$HOME/mxhx-shed"
node -v
npm ci
~~~

npm ci uses the checked-in npm lockfile and **replaces the project's node_modules directory**. It does not remove the repository source or unrelated Phantom Labs projects. Run only after confirming this is the correct project path, and only when package-lock.json exists and matches the package manifest. If npm ci reports lockfile mismatch, inspect the repo and ask the maintainer before changing dependency versions.

## EXTRA // Start and verify the local dev server

~~~bash
cd "$HOME/mxhx-shed"
nvm use 22
npm run dev
~~~

Vite prints a local address when startup succeeds. For the observed release, it was **http://localhost:8080/**. Open it on the same machine in Firefox, and keep the terminal session active.

**Network caution:** MXHX Shed's dev command uses --host 0.0.0.0, which listens on network interfaces. Only run on a trusted network behind appropriate firewall controls; do not forward port 8080 to the public internet.

## Field results from October 21, 2026

| Check | Observed outcome |
| --- | --- |
| nvm | 0.39.1 |
| Installed and active Node | v22.23.4 |
| Active npm | v10.9.9 |
| npm ci | 429 packages added; 430 audited |
| npm audit at installation | 0 vulnerabilities reported (**time-specific**, not a permanent guarantee) |
| Dev server | Vite v8.3.4 READY, shown at 781ms then 540ms in later screenshot |
| Browser connection | Vite HMR WebSocket connected in terminal log |
| Browser functionality | **Not exhaustively verified** |

The installation also printed deprecation warnings for Recharts and ESLint. These did not prevent installation. There was a notice about npm 12, but upgrading npm was not required for this repair.

## Triage if the issue returns

| Symptom | Next check |
| --- | --- |
| Unexpected reserved word on import | Run node -v and command -v node; verify nvm use 22 |
| Old npm error / ENOTDIR | Check npm -v, then run npm ci from the **correct project root** |
| Already-existing clone destination | cd into the directory; never delete it just to reclone |
| npm ci fails on lockfile | Check package-lock.json; coordinate with upstream maintainer instead of blindly rewriting |
| Port 8080 in use | Stop the competing process you own, or consult the project's dev script before changing ports |
| Vite ready, tool buttons fail | Inspect Firefox developer console and the project backend/integration requirements; server startup alone is not proof of tool operation |

## Scope

Repair validated in a Debian-based Linux environment for the publicly documented MXHX Shed project. It did **not** alter the upstream repository, globally uninstall old Node runtimes, or prove unrelated tools work. No GitHub clone was repeated and no system-wide Node replacement was needed.

**Ticket state: Node version, dependencies and dev-server boot passed; app feature verification remains a separate task.**
