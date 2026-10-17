package main

import (
	"context"
	"crypto/tls"
	"encoding/json"
	"flag"
	"fmt"
	"net"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"
)

type Result struct {
	URL              string            `json:"url"`
	FinalURL         string            `json:"final_url,omitempty"`
	Status           int               `json:"status,omitempty"`
	DurationMS       int64             `json:"duration_ms"`
	Server           string            `json:"server,omitempty"`
	Redirects        []string          `json:"redirects,omitempty"`
	TLSIssuer        string            `json:"tls_issuer,omitempty"`
	TLSExpiry        string            `json:"tls_expiry,omitempty"`
	TLSDaysRemaining int               `json:"tls_days_remaining,omitempty"`
	SecurityHeaders  map[string]string `json:"security_headers"`
	MissingHeaders   []string          `json:"missing_headers,omitempty"`
	Error            string            `json:"error,omitempty"`
	CheckedAt        string            `json:"checked_at"`
}

func inspect(target string, timeout time.Duration) Result {
	r := Result{URL: target, CheckedAt: time.Now().UTC().Format(time.RFC3339), SecurityHeaders: map[string]string{}}
	u, err := url.Parse(target)
	if err != nil || (u.Scheme != "https" && u.Scheme != "http") || u.Hostname() == "" || u.User != nil {
		r.Error = "Provide an http(s) URL with a hostname and no credentials"
		return r
	}
	// This tool is intended for sites the operator owns or has authorization to assess.
	redirects := []string{}
	client := &http.Client{Timeout: timeout, Transport: &http.Transport{Proxy: http.ProxyFromEnvironment, TLSClientConfig: &tls.Config{MinVersion: tls.VersionTLS12}, DialContext: (&net.Dialer{Timeout: timeout}).DialContext}, CheckRedirect: func(req *http.Request, via []*http.Request) error {
		if len(via) >= 5 {
			return fmt.Errorf("redirect limit reached")
		}
		redirects = append(redirects, req.URL.String())
		return nil
	}}
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, target, nil)
	if err != nil {
		r.Error = err.Error()
		return r
	}
	req.Header.Set("User-Agent", "GlitchByte-VoidLantern/1.0 (+authorized website diagnostics)")
	start := time.Now()
	resp, err := client.Do(req)
	r.DurationMS = time.Since(start).Milliseconds()
	r.Redirects = redirects
	if err != nil {
		r.Error = err.Error()
		return r
	}
	defer resp.Body.Close()
	r.FinalURL = resp.Request.URL.String()
	r.Status = resp.StatusCode
	r.Server = resp.Header.Get("Server")
	names := []string{"Strict-Transport-Security", "Content-Security-Policy", "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy", "X-Frame-Options"}
	for _, n := range names {
		v := resp.Header.Get(n)
		if v == "" {
			r.MissingHeaders = append(r.MissingHeaders, n)
		} else {
			r.SecurityHeaders[n] = v
		}
	}
	if resp.TLS != nil && len(resp.TLS.PeerCertificates) > 0 {
		c := resp.TLS.PeerCertificates[0]
		r.TLSIssuer = c.Issuer.CommonName
		r.TLSExpiry = c.NotAfter.UTC().Format(time.RFC3339)
		r.TLSDaysRemaining = int(time.Until(c.NotAfter).Hours() / 24)
	}
	return r
}
func main() {
	target := flag.String("url", "", "Website URL, e.g. https://example.com")
	out := flag.String("out", "voidlantern_report.json", "Path to JSON report")
	timeout := flag.Int("timeout", 12, "Request timeout in seconds (1-60)")
	flag.Parse()
	fmt.Println("\033[36m╔══════════════════════════════════════════╗\n║  GLITCHBYTE // VOIDLANTERN v1.0          ║\n║  STATUS • TLS • HEADERS • REDIRECTS      ║\n╚══════════════════════════════════════════╝\033[0m")
	if *target == "" {
		fmt.Fprintln(os.Stderr, "Usage: voidlantern -url https://example.com [-out report.json] [-timeout 12]")
		os.Exit(2)
	}
	if *timeout < 1 || *timeout > 60 {
		fmt.Fprintln(os.Stderr, "timeout must be between 1 and 60")
		os.Exit(2)
	}
	r := inspect(*target, time.Duration(*timeout)*time.Second)
	data, err := json.MarshalIndent(r, "", "  ")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if dir := filepath.Dir(*out); dir != "." {
		if err = os.MkdirAll(dir, 0755); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
	if err = os.WriteFile(*out, append(data, '\n'), 0644); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("\nTarget: %s\nStatus: %d\nTime: %d ms\nTLS expires: %s\nMissing security headers: %s\nReport: %s\n", r.URL, r.Status, r.DurationMS, r.TLSExpiry, strings.Join(r.MissingHeaders, ", "), *out)
	if r.Error != "" {
		fmt.Fprintln(os.Stderr, "Check error:", r.Error)
		os.Exit(1)
	}
}
