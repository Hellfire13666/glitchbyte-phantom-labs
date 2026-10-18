<!-- GLITCHBYTE-UPLOAD-DOOR:START -->
<div align="right"><a href="https://github.com/Hellfire13666/glitchbyte-phantom-labs/upload/main"><img alt="UPLOAD FILES" src="https://img.shields.io/badge/UPLOAD-FILES-FF8B1F?style=flat-square&logo=github&logoColor=white"></a></div>
<!-- GLITCHBYTE-UPLOAD-DOOR:END -->

# 👻 VOIDLANTERN

**GlitchByte Phantom Labs | Go Website Diagnostics | v1.0.0**

A lightweight, standard-library-only Go CLI for inspecting websites you own or are authorized to assess. Checks HTTP status, elapsed time, redirects, response server header, TLS certificate issuer/expiry, and six common HTTP security headers. Writes a JSON report.

## Requirements

- Go 1.21 or newer for building
- Linux, macOS, or Windows
- No external Go dependencies

## Build and test

```bash
go version
go test ./...
go vet ./...
go build -o voidlantern .
```

## Run

```bash
./voidlantern -url https://example.com -out reports/example.json
./voidlantern -url https://example.com -timeout 20 -out reports/example.json
```

Use `./voidlantern -h` for flags. `-timeout` accepts 1–60 seconds. A failed request still writes an error JSON report and exits nonzero. Avoid committing generated reports because URLs and headers may contain sensitive information.

## JSON fields

`url`, `final_url`, `status`, `duration_ms`, `server`, `redirects`, `tls_issuer`, `tls_expiry`, `tls_days_remaining`, `security_headers`, `missing_headers`, `error`, `checked_at`.

## Scope and limitations

- A single HTTP(S) request, following at most five redirects; not a crawler.
- Redirects can lead to other hosts. Only run against authorized destinations and review redirect behavior.
- Missing security headers are diagnostic signals, not proof of a vulnerability.
- Certificate errors are reported rather than bypassed.
- Does not scan ports, guess credentials, bypass authentication, or collect private content.

## Repository placement

Place this directory under `tools/go/voidlantern-go/` in your Phantom Labs repository. Its unique package folder and executable name avoid collisions with Python projects.

## License

No license has been selected yet. Before inviting public reuse, choose and add a license you are authorized to apply.
