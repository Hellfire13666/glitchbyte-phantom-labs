<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES / HQ" src="https://img.shields.io/badge/UPLOAD-FILES-E8B448?style=flat-square&logo=github&logoColor=black"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 🌹⚡ RIFTSEAL | Evidence Fingerprint Forge v1.0.0

**Status (October 19, 2026): Installed and tested on Ubuntu; source committed to its [own dedicated private GitHub repository](https://github.com/Hellfire13666/riftseal-evidence-forge-2026).** The owner verified the release ZIP SHA-256 and all **16/16** Ubuntu tests. GitHub confirms `visibility: private`, branch `main`; only authorized GitHub accounts can access the private source. This HQ page is a public setup guide, not a mirror of the private source.

## The actual RIFTSEAL tools

- `riftseal_evidence_forge_v1_0.py`: SHA-256 fingerprinting of local regular files, up to 25 inputs, colorful CLI, synthetic `--demo`, no save by default, opt-in `-o` / `--o` TXT output or `--save` JSON, exclusive mode-`0600` output and private mode-`0700` default JSON report directory.
- `riftseal_integrity_gate_v1_0.py`: `--file PATH --expect SHA256` comparison against a trusted SHA-256, or `--compare FIRST SECOND`; exit `0` match, `2` mismatch, `1` local input error. No network, no saved files.
- `riftseal_core_v1_0.py`: SHA-256 streaming, final-component symlink rejection, many concurrent-change checks, private/exclusive exports.
- `art/riftseal_cover.png`: bespoke gold/ruby/electric-cyan crystal seal and rose artwork made for this tool, packaged as an actual asset (not a fake functional screenshot).
- `tests/test_riftseal_release_v1_0.py`: **16 passing offline tests**, including a repeat run from a **fresh ZIP extraction**.

The original Ubuntu prototype `~/PhantomLabsLaunchers/riftseal-evidence-forge-2026/riftseal_evidence_forge.py` was separately reported to compute SHA-256 of HEXWRAITH RC2 ZIP (35,711 bytes), matching the previously trusted fingerprint. The **new package is versioned and separate**, and the new versioned release has now been installed and tested separately on the owner's Ubuntu workstation.

## ZIP and verified release fingerprint

- **Package:** `riftseal-evidence-forge-v1.0.0.zip`
- **SHA-256:** `c2ce1ad5f8a9a2101b9664664c273a14a0e7b59cbaf5677a7696fe1d9a845a13`
- **Verification:** `sha256sum -c`, `unzip -tq`, per-member SHA-256 manifest; independent extracted suite **16 tests, OK**; matching and intentionally mismatching comparison smoke tests passed.
- **Includes:** README with standalone tool artwork, `GITHUB_PUBLISH.md`, source code, examples, scripts, all tests, release and next-chat handoff notes, source-available license, manifest and external ZIP hash sidecar.
- **No user persona research files, private Git bundles or real stored reports are bundled**.

## 🌱 SIMPLE: Synthetic offline demo

```bash
cd "$HOME/PhantomLabsLaunchers/riftseal-evidence-forge-v1_0_0"
python3 -B riftseal_evidence_forge_v1_0.py --demo --color always
```

A labeled synthetic record prints with a genuine SHA-256 of synthetic bytes. Nothing saved.

## ⚡ MEDIUM: Hash a real local file

```bash
cd "$HOME/PhantomLabsLaunchers/riftseal-evidence-forge-v1_0_0"
python3 -B riftseal_evidence_forge_v1_0.py --file examples/sample_evidence.txt --color always
# Opt-in private TXT, no overwrite:
python3 -B riftseal_evidence_forge_v1_0.py --file examples/sample_evidence.txt -o "$HOME/Downloads/riftseal_$(date +%s).txt"
```

For opt-in JSON save, add `--save` and verify `~/RiftSealPrivateReports2026` mode `0700`. TXT/JSON files created exclusively, mode `0600`.

## 🔥 EXTRA: Verify and compare

```bash
cd "$HOME/PhantomLabsLaunchers/riftseal-evidence-forge-v1_0_0"
HASH="$(sha256sum examples/sample_evidence.txt | cut -d' ' -f1)"
python3 -B riftseal_integrity_gate_v1_0.py --file examples/sample_evidence.txt --expect "$HASH"
python3 -B riftseal_integrity_gate_v1_0.py --compare examples/sample_evidence.txt examples/sample_evidence_copy.txt
# Intentional mismatch returns code 2:
python3 -B riftseal_integrity_gate_v1_0.py --compare examples/sample_evidence.txt examples/sample_evidence_changed.txt
```

The local self-derived hash illustrates the CLI, **not independent source authenticity**. To verify the owner's earlier HEXWRAITH RC2 ZIP with its independently recorded SHA-256:

```bash
python3 -B riftseal_integrity_gate_v1_0.py \
  --file "$HOME/Downloads/hexwraith_privacy_edition_v1_1_1_rc2.zip" \
  --expect b1728a0b480eae045ad289e59a69b3d20fd79e787d81bf4561c9f9428bb800a7
```

## Privacy, limitations and required next publication step

The released code runs offline and avoids overwriting reports, but SHA-256 itself **doesn't establish file authorship, source authenticity, legal chain-of-custody, malware safety, or a race-proof snapshot**. Its direct symlink and metadata checks are bounded protections, not a production security certification. Filesystem filename privacy depends on parent directories and deployment context.

**Dedicated private source repository:** [`Hellfire13666/riftseal-evidence-forge-2026`](https://github.com/Hellfire13666/riftseal-evidence-forge-2026) (**GitHub-confirmed private**). The owner's Ubuntu helper created and pushed the initial `main` commit; the README, source, sample files, artwork and tests are accessible with permission. The release ZIP/manifest are frozen pre-publication provenance and may describe the repository as pending; their original checksums must not be silently revised. **Pending:** an independently verified fresh clone, version tag/GitHub Release (if desired) and private off-device recovery backup. Do **not** upload its private source or reports to the public Backup HQ.

**Next project:** RootSignal Cultivator is now in local v1.0.0 release-candidate preparation, derived from its original seedbed. Ubuntu installation and dedicated private repository are separate pending milestones; don't repeat old audits.

Lab navigation: [Headquarters](../../README.md) · [Cultivation Room](../CULTIVATION_ROOM.md) · [Tool Vault](../TOOL_VAULT.md) · [Mandatory Build Charter](../PHANTOM_LABS_MANDATORY_BUILD_CHARTER.md) · [Build Publication Standard](../BUILD_PUBLICATION_STANDARD.md) · [Public Backup HQ](https://github.com/Hellfire13666/glitchbyte-phantom-labs-releases).
