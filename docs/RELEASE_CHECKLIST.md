# RosieGlitchByte public release checklist

- [x] Preserve source and artwork in a downloadable archive
- [ ] Decide whether to remove the preserved nested workshop directory before public release
- [x] Verify Python source syntax and offline repository tests
- [x] Add `.gitignore`, security policy and CI workflow
- [x] Confirm the IP Shadow Scraper source requests certificate and IP-hostname verification, with offline mocked regression coverage (Phase 24)
- [ ] Validate IP-address TLS and certificate errors against an explicitly authorized live HTTPS endpoint
- [x] Run all 17 first-run Bash recipes in isolated Ubuntu CI workspaces (Phase 22; local Git remapping)
- [x] Confirm a real public HTTPS Git clone and offline Python/Go checks on Ubuntu (Phase 23)
- [ ] Perform tool-by-tool **live** functional, authorization, and platform compliance tests
- [ ] Review all file contents and Git history for secrets and private data
- [x] Adopt a custom source-available license permitting unmodified use
- [ ] Confirm redistribution rights for all assets
- [x] Upload release candidate to private GitHub repository and verify GitHub Actions
- [x] Create and verify an independent local release backup

## Additional unresolved release gates

- [ ] Resolve the optional IP Shadow Scraper artwork path discrepancy without overwriting approved artwork
- [ ] Review report filename collision / overwrite behavior under repeated same-second runs
- [ ] Review dotted-handle filename handling in Rose Crawler before calling every output name stable
- [ ] Review dependencies, automation permissions, network redirects and output privacy for production deployment

Offline tests do not establish live platform compliance, full security auditing, credential safety across Git history, or permission to scan a third-party target. See [Phase 24 readiness findings](RELEASE_READINESS_REVIEW.md).
