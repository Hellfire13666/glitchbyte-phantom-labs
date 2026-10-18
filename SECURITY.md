<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right">
  <a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main" title="UPLOAD FILES to glitchbyte-phantom-labs"><img alt="📤 UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF1493?style=flat-square&logo=github&logoColor=white"></a>
</div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# Security policy

This is a collection of educational, public-information and local research tools. Use them only where authorized and in accordance with applicable laws and platform terms.

**Never commit** API tokens, passwords, browser cookies, session files, private research data, or identifying information about third parties. Keep output reports outside the repository.

## Known release-review item

`tools/rosie_ip_shadow_scraper.py` currently creates a default verifying TLS context and explicitly sets `check_hostname=True` and `verify_mode=ssl.CERT_REQUIRED`. It connects by **IP address** and passes that address as `server_hostname`, so certificate validation requires a trusted certificate valid for that IP. A typical certificate issued for a DNS hostname may fail this check. Failed handshakes are recorded as errors, not as verified fingerprints.

**Verification scope:** the Phase 24 offline regression test uses mocked TLS connections to confirm these settings and the certificate-failure behavior. It does **not** test a live HTTPS server, guarantee system trust-store configuration, or establish that all networking paths are secure. Authorized live integration review is still required before claiming security-sensitive production readiness.

**Known release limitations:** Phase 25 corrected the IP Shadow Scraper's optional artwork lookup to point to the existing repository `artwork/rosie_ip_shadow_art.png`. It also added collision-resistant microsecond/UUID report filenames to IP Shadow Scraper and Rose Crawler. These changes have offline regression coverage; other tools may still have fixed report filenames or timestamp collisions. Neither the artwork fix nor report naming establishes live-network security.

Other tools may require further testing of networking behavior, rate limits, terms-of-service compliance and error handling. No external penetration testing or live integration testing has been performed as part of this release candidate.

For sensitive reports, contact the repository maintainer privately rather than opening a public issue with credentials.
