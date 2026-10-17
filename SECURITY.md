# Security policy

This is a collection of educational, public-information and local research tools. Use them only where authorized and in accordance with applicable laws and platform terms.

**Never commit** API tokens, passwords, browser cookies, session files, private research data, or identifying information about third parties. Keep output reports outside the repository.

## Known release-review item

`tools/rosie_ip_shadow_scraper.py` obtains a remote TLS certificate fingerprint while deliberately disabling certificate and hostname verification. **Its TLS result is not authenticated**, is vulnerable to interception, and must not be treated as proof of server identity. This feature requires design review before a public security-sensitive release.

Other tools may require further testing of networking behavior, rate limits, terms-of-service compliance and error handling. No external penetration testing or live integration testing has been performed as part of this release candidate.

For sensitive reports, contact the repository maintainer privately rather than opening a public issue with credentials.
