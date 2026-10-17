# 🕷️ PHANTOM TOOL SHOWCASE TEMPLATE

> **Template only. Not a published tool.** Create a *new uniquely named* Markdown file for each existing tool and link it from the Tool Vault. Never overwrite tool source or reuse another tool's identity.

# [EXACT TOOL NAME] // [DISTINCT PERSONALITY]

**Language and version · What it actually does · Output types**

Replace these placeholders with **verified Markdown links** when creating a tool page: `../../tools/PATH_TO_EXISTING_SOURCE`, `../../tools/PATH_TO_TESTS`, and `../../tools/PATH_TO_README`. Do not leave dead placeholder links in a published spotlight.

## What it does
Describe verified functionality from source, not concepts shown in screenshots. Explain key limitations and the permission model.

## 📋 COPY & PASTE BUILD RECIPE (mandatory for EVERY tool)

A tool page is **not showcase-complete** until it contains a single copy-ready Bash block and individual sections for the six stages below. Confirm every command from the actual source, test the happy path where possible, and mark untested steps honestly. Do not print non-working placeholder commands in the final showcase.

### 1. Install

State platform, version requirements and **exact dependencies**. Show how to get the repository and use a dedicated virtual environment for Python projects where needed. Do not install dependencies that the particular tool does not need.

### 2. Build

Give real steps for the language: `go build` for Go; Python syntax or packaging steps where applicable. Do **not** pretend standalone Python scripts require compilation.

### 3. Test

Provide genuine commands and their expected scope: Go `go test ./...` and `go vet ./...` from the module, Python `compileall`, project-specific unit tests, etc. Distinguish a passed test from an unexecuted recommendation.

### 4. Run

Use actual CLI flags. For network tools, prompt for a **permitted** target or require explicit replacement of a placeholder; do not silently test unrelated third-party domains.

### 5. Find and read results

Show the real output filename or flag and one or more applicable commands:

```bash
find . -type f \( -name '*.html' -o -name '*.json' -o -name '*.csv' \)
```

For example, display actual JSON with `python3 -m json.tool <actual-file>`, open HTML using `xdg-open <actual-file>`, or inspect CSV with `head`. Include only formats that the actual tool produces.

### 6. Troubleshoot

List concrete errors (wrong directory, interpreter/Go version, dependencies, permissions, network timeout, empty report) and practical checks.

### 📦 One-block Bash recipe

Include a final fenced `bash` code block users can **copy and paste**, covering steps 1–5 in order, with a sensible stop-on-error behavior, safe paths, and a clear final result location. Test the actual copy/paste flow before labeling it tested.

Keep other tool pages independently named. A template must never pretend a new tool already exists.

## Reports and example output

State output types, default filename/path, and clearly mark any illustrative report fields as *examples, not real scan results*.

## Safety, permissions and licensing
Link to [license](../../LICENSE-NOTICE.md), [security](../../SECURITY.md) and relevant known limitations. No sensitive data or speculative identification.

## Identity
Use a distinctive icon, palette, project voice and terminology; keep Rosie consistent with [official visual standards](../ROSIE_VISUAL_STANDARD.md) without requiring her portrait on every tool.

[← Tool Vault](../TOOL_VAULT.md)
