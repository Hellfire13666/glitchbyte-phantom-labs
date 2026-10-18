# 🌹 PHASE 23 // PUBLIC HTTPS CLONE VERIFICATION

**Status: PASS on the GitHub-hosted Ubuntu runner.**

[Successful Phase 23 workflow](https://github.com/Hellfire13666/glitchbyte-phantom-labs/actions/runs/39085770542) · [Actual CI workflow](../.github/workflows/public-clone-verification.yml) · [Phase 22 verification](CLEAN_BUILD_VERIFICATION.md)

## What this checks

Phase 22 ran all 17 first-run recipes in isolated Ubuntu homes, but used a local Git URL mapping for the clone step. This phase specifically closes that remaining **public repository download** gap.

The new GitHub Actions workflow:

1. Checks out the proposed branch for comparison.
2. Performs a real shallow public HTTPS clone of `https://github.com/Hellfire13666/glitchbyte-phantom-labs.git`, with no Git URL rewrite and no supplied token.
3. Checks that the downloaded repository contains `README.md`, `SECURITY.md`, and `LICENSE-NOTICE.md`.
4. Compares SHA-256 hashes of the Python and Go source files in the proposed branch against the downloaded public repository's files, confirming they remain unchanged.
5. Runs the actual **offline Python terminal tests** inside the downloaded repository.
6. Runs `go test ./...`, `go vet ./...`, and `go build` inside the downloaded VOIDLANTERN project.

The successful Ubuntu run is linked above. This workflow is set to run on repository pushes and pull requests after merging Phase 23.

## Verification matrix

| Concern | Evidence |
| --- | --- |
| Public network clone | HTTPS Git clone passed in Ubuntu Actions |
| Original source preservation | Source SHA-256 comparison passed |
| Python execution | Offline terminal verification passed on downloaded main |
| Go | VOIDLANTERN tests, static checks and build passed on downloaded main |
| Existing individual build recipes | Phase 22 verified 17/17 first-run Bash blocks in isolated Ubuntu workspaces |

## What remains unverified

- Paid and permission-dependent X API endpoints.
- Live public-profile queries or authorized website, TLS, and IP connectivity checks.
- Successful results for arbitrary real-world networks or accounts.
- Full security audit and all possible inputs.
- All optional command examples beyond the first-run build blocks.
- Public cloning from every user's network or on every Linux distribution.

This phase does **not** change tool source code, Go code, the custom license, SECURITY.md, approved Rosie artwork, or Git history. It verifies build delivery, not real-world investigation outcomes.

[← Official homepage](../README.md) · [← Tool Vault](TOOL_VAULT.md)
